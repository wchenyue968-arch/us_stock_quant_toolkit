import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_metrics(
    strategy_data: pd.DataFrame,
    period: str,
    start_date: pd.Timestamp | None = None,
    end_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Calculate strategy metrics for full, train, or test period."""
    data = strategy_data.copy()
    if start_date is not None:
        data = data[data.index >= start_date]
    if end_date is not None:
        data = data[data.index <= end_date]

    if data.empty:
        raise ValueError(f"No strategy data available for {period} period.")

    rows = []
    strategies = sorted({column.replace(" Daily Return", "") for column in data.columns if column.endswith(" Daily Return")})
    years = len(data) / TRADING_DAYS_PER_YEAR

    for strategy in strategies:
        daily_returns = data[f"{strategy} Daily Return"]
        cumulative = (1 + daily_returns).cumprod() - 1
        equity = 1 + cumulative
        drawdown = equity / equity.cummax() - 1
        total_return = float(cumulative.iloc[-1])
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        annualized_volatility = float(daily_returns.std() * (TRADING_DAYS_PER_YEAR**0.5))
        sharpe = 0.0 if annualized_volatility == 0 else float(annualized_return / annualized_volatility)
        max_drawdown = float(drawdown.min())
        calmar = 0.0 if max_drawdown == 0 else float(annualized_return / abs(max_drawdown))
        win_rate = float((daily_returns > 0).mean())
        trades = int((data[f"{strategy} Turnover"] > 0).sum())
        turnover = float(data[f"{strategy} Turnover"].sum() / len(data))

        rows.append(
            {
                "Period": period,
                "Strategy": strategy,
                "Cumulative Return": total_return,
                "Annualized Return": annualized_return,
                "Annualized Volatility": annualized_volatility,
                "Sharpe Ratio": sharpe,
                "Maximum Drawdown": max_drawdown,
                "Calmar Ratio": calmar,
                "Win Rate": win_rate,
                "Number of Trades": trades,
                "Turnover": turnover,
            }
        )

    return pd.DataFrame(rows)
