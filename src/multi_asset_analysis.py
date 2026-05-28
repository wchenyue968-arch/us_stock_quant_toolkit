"""Reusable analysis helpers for multi-asset research modes."""

from pathlib import Path

import pandas as pd

from data_loader import update_data


TRADING_DAYS_PER_YEAR = 252


def load_asset_data(
    tickers: list[str],
    start_date: str,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> tuple[dict[str, pd.DataFrame], list[str]]:
    """Download or update cached data for many tickers, skipping failed tickers."""
    data_by_ticker = {}
    failed_tickers = []

    for ticker in tickers:
        symbol = ticker.upper().strip()
        if not symbol:
            continue

        try:
            data = update_data(symbol, start_date, end_date=end_date, force_refresh=force_refresh)
        except Exception as error:
            print(f"Warning: skipped {symbol}. Reason: {error}")
            failed_tickers.append(symbol)
            continue

        if data.empty:
            print(f"Warning: skipped {symbol}. Reason: no price data.")
            failed_tickers.append(symbol)
            continue

        data_by_ticker[symbol] = data

    return data_by_ticker, failed_tickers


def build_close_table(data_by_ticker: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create one date-aligned close-price table."""
    close_table = pd.DataFrame()
    for ticker, data in data_by_ticker.items():
        close_table[ticker] = data["close"]

    close_table = close_table.sort_index()
    close_table = close_table.dropna(how="all")
    return close_table


def calculate_daily_returns(close_table: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily percentage returns for each asset."""
    return close_table.pct_change(fill_method=None).dropna(how="all")


def calculate_cumulative_returns(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Convert daily returns into cumulative returns."""
    return (1 + daily_returns.fillna(0)).cumprod() - 1


def calculate_drawdowns(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate drawdown series for each asset."""
    equity = (1 + daily_returns.fillna(0)).cumprod()
    return equity / equity.cummax() - 1


def calculate_return_metrics(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate core return and risk metrics for each return series."""
    rows = []
    clean_returns = daily_returns.dropna(how="all")
    years = len(clean_returns) / TRADING_DAYS_PER_YEAR

    for name in clean_returns.columns:
        returns = clean_returns[name].dropna()
        if returns.empty:
            continue

        cumulative = (1 + returns).cumprod() - 1
        equity = 1 + cumulative
        drawdown = equity / equity.cummax() - 1
        total_return = float(cumulative.iloc[-1])
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0.0
        annualized_volatility = float(returns.std() * (TRADING_DAYS_PER_YEAR**0.5))
        sharpe = 0.0 if annualized_volatility == 0 else float(annualized_return / annualized_volatility)
        max_drawdown = float(drawdown.min())
        calmar = 0.0 if max_drawdown == 0 else float(annualized_return / abs(max_drawdown))

        rows.append(
            {
                "Ticker": name,
                "Cumulative Return": total_return,
                "Annualized Return": annualized_return,
                "Annualized Volatility": annualized_volatility,
                "Sharpe Ratio": sharpe,
                "Maximum Drawdown": max_drawdown,
                "Calmar Ratio": calmar,
            }
        )

    return pd.DataFrame(rows)


def build_equal_weight_portfolio(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Build an equal-weight portfolio from available daily returns."""
    portfolio = pd.DataFrame(index=daily_returns.index)
    portfolio["Equal Weight Portfolio Daily Return"] = daily_returns.mean(axis=1, skipna=True)
    portfolio["Equal Weight Portfolio Cumulative Return"] = (
        1 + portfolio["Equal Weight Portfolio Daily Return"].fillna(0)
    ).cumprod() - 1
    return portfolio


def run_asset_comparison(
    tickers: list[str],
    start_date: str,
    metrics_path: Path,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> dict[str, object]:
    """Run a shared multi-asset comparison and save the metrics table."""
    data_by_ticker, failed_tickers = load_asset_data(
        tickers,
        start_date,
        end_date=end_date,
        force_refresh=force_refresh,
    )
    if not data_by_ticker:
        raise RuntimeError("No valid asset data was available for this research mode.")

    close_table = build_close_table(data_by_ticker)
    daily_returns = calculate_daily_returns(close_table)
    cumulative_returns = calculate_cumulative_returns(daily_returns)
    drawdowns = calculate_drawdowns(daily_returns)
    metrics = calculate_return_metrics(daily_returns)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(metrics_path, index=False)

    return {
        "tickers": list(data_by_ticker.keys()),
        "failed_tickers": failed_tickers,
        "close_table": close_table,
        "daily_returns": daily_returns,
        "cumulative_returns": cumulative_returns,
        "drawdowns": drawdowns,
        "metrics": metrics,
    }
