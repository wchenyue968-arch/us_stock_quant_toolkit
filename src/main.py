from pathlib import Path

import pandas as pd

from asset_universe import (
    MULTI_ASSET_ALLOCATION,
    MULTI_ASSET_TICKERS,
    MULTI_STOCK_COMPARISON,
    MULTI_STOCK_TICKERS,
    SECTOR_ETF_COMPARISON,
    SECTOR_ETF_TICKERS,
    SINGLE_ASSET_STRATEGY_BACKTEST,
    SINGLE_ASSET_TICKER,
)
from backtester import apply_strategy_returns, build_monthly_returns, build_trade_log
from data_loader import get_data_path, update_data
from indicators import build_indicators
from metrics import calculate_metrics
from multi_asset_analysis import (
    build_equal_weight_portfolio,
    calculate_cumulative_returns,
    calculate_drawdowns,
    calculate_return_metrics,
    run_asset_comparison,
)
from pdf_report_generator import generate_all_v7_pdfs
from plots import (
    plot_correlation_heatmap,
    plot_cumulative,
    plot_drawdown,
    plot_metric_ranking,
    plot_multi_cumulative_returns,
    plot_multi_drawdown,
    plot_rolling_risk,
)
from report_generator import write_asset_comparison_reports, write_v7_markdown_reports
from strategies import build_strategy_signals


PROJECT_ROOT = Path(__file__).resolve().parents[1]
START_DATE = "2018-01-01"
DEFAULT_TICKER = SINGLE_ASSET_TICKER
TRANSACTION_COST = 0.001
TRAIN_END_DATE = "2021-12-31"
DEFAULT_TRAIN_TEST_SPLIT_DATE = "2022-01-01"

# Change this value to run another research mode.
# Options:
# - single_asset_strategy_backtest
# - multi_stock_comparison
# - sector_etf_comparison
# - multi_asset_allocation
RESEARCH_MODE = SINGLE_ASSET_STRATEGY_BACKTEST


def save_outputs(
    ticker: str,
    price_data: pd.DataFrame,
    indicators: pd.DataFrame,
    signals: pd.DataFrame,
    strategy_data: pd.DataFrame,
    trade_log: pd.DataFrame,
    monthly_returns: pd.DataFrame,
    full_metrics: pd.DataFrame,
    train_test_metrics: pd.DataFrame,
) -> dict[str, Path]:
    """Save all v7 output files."""
    data_dir = PROJECT_ROOT / "data"
    outputs_dir = PROJECT_ROOT / "outputs"
    data_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)

    paths = {
        "raw_data": data_dir / f"{ticker}_raw_price_data.csv",
        "indicators": outputs_dir / f"{ticker}_indicators.csv",
        "signals": outputs_dir / f"{ticker}_strategy_signals.csv",
        "trade_log": outputs_dir / f"{ticker}_trade_log.csv",
        "monthly_returns": outputs_dir / f"{ticker}_monthly_returns.csv",
        "strategy_returns": outputs_dir / "v7_strategy_returns.csv",
        "full_metrics": outputs_dir / "v7_full_strategy_metrics.csv",
        "train_test_metrics": outputs_dir / "v7_train_test_metrics.csv",
    }

    price_data.to_csv(paths["raw_data"], index_label="date")
    indicators.to_csv(paths["indicators"], index_label="date")
    signals.to_csv(paths["signals"], index_label="date")
    trade_log.to_csv(paths["trade_log"], index=False)
    monthly_returns.to_csv(paths["monthly_returns"], index_label="date")
    strategy_data.to_csv(paths["strategy_returns"], index_label="date")
    full_metrics.to_csv(paths["full_metrics"], index=False)
    train_test_metrics.to_csv(paths["train_test_metrics"], index=False)
    return paths


def run_v7_research_backtest(
    ticker: str = DEFAULT_TICKER,
    start_date: str = START_DATE,
    end_date: str | None = None,
    transaction_cost: float = TRANSACTION_COST,
    train_test_split_date: str = DEFAULT_TRAIN_TEST_SPLIT_DATE,
    force_refresh: bool = False,
) -> dict[str, Path]:
    """Run the complete v7 research workflow."""
    ticker = ticker.upper().strip() or DEFAULT_TICKER
    outputs_dir = PROJECT_ROOT / "outputs"
    test_start = pd.Timestamp(train_test_split_date)
    train_end = test_start - pd.Timedelta(days=1)

    price_data = update_data(ticker, start_date, end_date=end_date, force_refresh=force_refresh)
    indicators = build_indicators(price_data)
    signals = build_strategy_signals(indicators)
    strategy_data = apply_strategy_returns(indicators, signals, transaction_cost)
    trade_log = build_trade_log(signals)
    monthly_returns = build_monthly_returns(strategy_data)

    full_metrics = calculate_metrics(strategy_data, "Full")
    train_metrics = calculate_metrics(strategy_data, "Train", end_date=train_end)
    test_metrics = calculate_metrics(strategy_data, "Test", start_date=test_start)
    train_test_metrics = pd.concat([full_metrics, train_metrics, test_metrics], ignore_index=True)

    paths = save_outputs(
        ticker,
        price_data,
        indicators,
        signals,
        strategy_data,
        trade_log,
        monthly_returns,
        full_metrics,
        train_test_metrics,
    )
    paths["cache_data"] = get_data_path(ticker)

    paths["full_chart"] = plot_cumulative(
        strategy_data,
        outputs_dir / "v7_strategy_comparison_full.png",
        "V7 Full-Sample Strategy Cumulative Return",
    )
    paths["test_chart"] = plot_cumulative(
        strategy_data,
        outputs_dir / "v7_strategy_comparison_test.png",
        "V7 Test-Period Strategy Cumulative Return",
        start_date=test_start,
    )
    paths["drawdown_chart"] = plot_drawdown(strategy_data, outputs_dir / "v7_drawdown_comparison.png")
    paths["rolling_risk_chart"] = plot_rolling_risk(strategy_data, outputs_dir / "v7_rolling_risk.png")

    cn_md, en_md = write_v7_markdown_reports(
        PROJECT_ROOT,
        ticker,
        paths["full_metrics"],
        paths["train_test_metrics"],
        data_start=str(price_data.index.min().date()),
        data_end=str(price_data.index.max().date()),
        train_start=start_date,
        train_end=str(train_end.date()),
        test_start=str(test_start.date()),
        test_end=str(price_data.index.max().date()),
    )
    paths["cn_md"] = cn_md
    paths["en_md"] = en_md
    paths.update(generate_all_v7_pdfs(PROJECT_ROOT))
    return paths


def run_multi_stock_comparison(
    tickers: list[str] | None = None,
    start_date: str = START_DATE,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> dict[str, Path | list[str]]:
    """Compare several large US stocks."""
    outputs_dir = PROJECT_ROOT / "outputs"
    paths: dict[str, Path | list[str]] = {}
    tickers = tickers or MULTI_STOCK_TICKERS

    result = run_asset_comparison(
        tickers,
        start_date,
        outputs_dir / "multi_stock_metrics.csv",
        end_date=end_date,
        force_refresh=force_refresh,
    )

    paths["metrics"] = outputs_dir / "multi_stock_metrics.csv"
    paths["cumulative_chart"] = plot_multi_cumulative_returns(
        result["cumulative_returns"],
        outputs_dir / "multi_stock_cumulative_returns.png",
        "Multi-Stock Cumulative Return Comparison",
    )
    paths["drawdown_chart"] = plot_multi_drawdown(
        result["drawdowns"],
        outputs_dir / "multi_stock_drawdown.png",
        "Multi-Stock Drawdown Comparison",
    )
    paths["correlation_chart"] = plot_correlation_heatmap(
        result["daily_returns"],
        outputs_dir / "multi_stock_correlation.png",
        "Multi-Stock Daily Return Correlation",
    )
    cn_md, en_md = write_asset_comparison_reports(
        outputs_dir,
        "multi_stock",
        "多只美股个股对比研究",
        "Multi-Stock Comparison Research",
        "比较多只美股个股的历史收益、风险和相关性表现。",
        "Compare the historical return, risk, and correlation characteristics of several US stocks.",
        result["tickers"],
        result["metrics"],
        [
            "outputs/multi_stock_cumulative_returns.png",
            "outputs/multi_stock_drawdown.png",
            "outputs/multi_stock_correlation.png",
        ],
        result["failed_tickers"],
    )
    paths["cn_report"] = cn_md
    paths["en_report"] = en_md
    paths["failed_tickers"] = result["failed_tickers"]
    return paths


def run_sector_etf_comparison(
    tickers: list[str] | None = None,
    start_date: str = START_DATE,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> dict[str, Path | list[str]]:
    """Compare major US sector ETFs."""
    outputs_dir = PROJECT_ROOT / "outputs"
    paths: dict[str, Path | list[str]] = {}
    tickers = tickers or SECTOR_ETF_TICKERS

    result = run_asset_comparison(
        tickers,
        start_date,
        outputs_dir / "sector_etf_metrics.csv",
        end_date=end_date,
        force_refresh=force_refresh,
    )

    paths["metrics"] = outputs_dir / "sector_etf_metrics.csv"
    paths["cumulative_chart"] = plot_multi_cumulative_returns(
        result["cumulative_returns"],
        outputs_dir / "sector_etf_cumulative_returns.png",
        "Sector ETF Cumulative Return Comparison",
    )
    paths["annual_return_ranking"] = plot_metric_ranking(
        result["metrics"],
        "Annualized Return",
        outputs_dir / "sector_etf_annual_return_ranking.png",
        "Sector ETF Annualized Return Ranking",
    )
    paths["max_drawdown_ranking"] = plot_metric_ranking(
        result["metrics"],
        "Maximum Drawdown",
        outputs_dir / "sector_etf_max_drawdown_ranking.png",
        "Sector ETF Maximum Drawdown Ranking",
        higher_is_better=True,
    )
    paths["sharpe_ranking"] = plot_metric_ranking(
        result["metrics"],
        "Sharpe Ratio",
        outputs_dir / "sector_etf_sharpe_ranking.png",
        "Sector ETF Sharpe Ratio Ranking",
    )
    cn_md, en_md = write_asset_comparison_reports(
        outputs_dir,
        "sector_etf",
        "美国行业 ETF 对比研究",
        "US Sector ETF Comparison Research",
        "比较美国不同行业 ETF 的历史收益、风险和风险调整后表现。",
        "Compare the historical return, risk, and risk-adjusted performance of major US sector ETFs.",
        result["tickers"],
        result["metrics"],
        [
            "outputs/sector_etf_cumulative_returns.png",
            "outputs/sector_etf_annual_return_ranking.png",
            "outputs/sector_etf_max_drawdown_ranking.png",
            "outputs/sector_etf_sharpe_ranking.png",
        ],
        result["failed_tickers"],
    )
    paths["cn_report"] = cn_md
    paths["en_report"] = en_md
    paths["failed_tickers"] = result["failed_tickers"]
    return paths


def run_multi_asset_allocation(
    tickers: list[str] | None = None,
    start_date: str = START_DATE,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> dict[str, Path | list[str]]:
    """Compare multi-asset ETFs and build an equal-weight portfolio."""
    outputs_dir = PROJECT_ROOT / "outputs"
    paths: dict[str, Path | list[str]] = {}
    tickers = tickers or MULTI_ASSET_TICKERS

    result = run_asset_comparison(
        tickers,
        start_date,
        outputs_dir / "multi_asset_metrics.csv",
        end_date=end_date,
        force_refresh=force_refresh,
    )

    portfolio = build_equal_weight_portfolio(result["daily_returns"])
    portfolio_metrics = calculate_return_metrics(portfolio[["Equal Weight Portfolio Daily Return"]].rename(
        columns={"Equal Weight Portfolio Daily Return": "Equal Weight Portfolio"}
    ))
    combined_metrics = pd.concat([result["metrics"], portfolio_metrics], ignore_index=True)
    combined_metrics.to_csv(outputs_dir / "multi_asset_metrics.csv", index=False)

    combined_cumulative = result["cumulative_returns"].copy()
    combined_cumulative["Equal Weight Portfolio"] = portfolio["Equal Weight Portfolio Cumulative Return"]
    combined_returns = result["daily_returns"].copy()
    combined_returns["Equal Weight Portfolio"] = portfolio["Equal Weight Portfolio Daily Return"]

    paths["metrics"] = outputs_dir / "multi_asset_metrics.csv"
    paths["portfolio_returns"] = outputs_dir / "equal_weight_portfolio_returns.csv"
    portfolio.to_csv(paths["portfolio_returns"], index_label="date")
    paths["cumulative_chart"] = plot_multi_cumulative_returns(
        combined_cumulative,
        outputs_dir / "multi_asset_cumulative_returns.png",
        "Multi-Asset Cumulative Return Comparison",
    )
    paths["correlation_chart"] = plot_correlation_heatmap(
        result["daily_returns"],
        outputs_dir / "multi_asset_correlation.png",
        "Multi-Asset Daily Return Correlation",
    )
    cn_md, en_md = write_asset_comparison_reports(
        outputs_dir,
        "multi_asset",
        "多资产 ETF 配置研究",
        "Multi-Asset Allocation Research",
        "比较股票、债券和黄金 ETF 的历史表现，并加入一个简单等权重组合。",
        "Compare stock, bond, and gold ETFs, and include a simple equal-weight portfolio.",
        result["tickers"] + ["Equal Weight Portfolio"],
        combined_metrics,
        [
            "outputs/multi_asset_cumulative_returns.png",
            "outputs/multi_asset_correlation.png",
            "outputs/equal_weight_portfolio_returns.csv",
        ],
        result["failed_tickers"],
    )
    paths["cn_report"] = cn_md
    paths["en_report"] = en_md
    paths["failed_tickers"] = result["failed_tickers"]
    return paths


def main() -> None:
    """Run the selected research workflow."""
    if RESEARCH_MODE == SINGLE_ASSET_STRATEGY_BACKTEST:
        paths = run_v7_research_backtest()
    elif RESEARCH_MODE == MULTI_STOCK_COMPARISON:
        paths = run_multi_stock_comparison()
    elif RESEARCH_MODE == SECTOR_ETF_COMPARISON:
        paths = run_sector_etf_comparison()
    elif RESEARCH_MODE == MULTI_ASSET_ALLOCATION:
        paths = run_multi_asset_allocation()
    else:
        raise ValueError(f"Unknown research mode: {RESEARCH_MODE}")

    print("US Stock Quant Toolkit V7")
    print("-------------------------")
    print(f"Research mode: {RESEARCH_MODE}")
    print(f"Transaction cost: {TRANSACTION_COST}")
    print("Generated files:")
    for name, path in paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
