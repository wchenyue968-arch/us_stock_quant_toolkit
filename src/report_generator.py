from pathlib import Path

import pandas as pd


DISCLAIMER = "This project is for educational and research purposes only and does not constitute investment advice."


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def get_key_findings(full_metrics: pd.DataFrame, train_test_metrics: pd.DataFrame) -> dict[str, str]:
    best_return = full_metrics.sort_values("Cumulative Return", ascending=False).iloc[0]
    lowest_drawdown = full_metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]
    best_sharpe = full_metrics.sort_values("Sharpe Ratio", ascending=False).iloc[0]

    test_metrics = train_test_metrics[train_test_metrics["Period"] == "Test"]
    best_test = test_metrics.sort_values("Sharpe Ratio", ascending=False).iloc[0]

    full_best_strategy = best_return["Strategy"]
    test_same_as_full = "yes" if best_test["Strategy"] == full_best_strategy else "no"

    return {
        "best_return_strategy": str(best_return["Strategy"]),
        "best_return_value": format_percent(float(best_return["Cumulative Return"])),
        "lowest_drawdown_strategy": str(lowest_drawdown["Strategy"]),
        "lowest_drawdown_value": format_percent(float(lowest_drawdown["Maximum Drawdown"])),
        "best_sharpe_strategy": str(best_sharpe["Strategy"]),
        "best_sharpe_value": f"{float(best_sharpe['Sharpe Ratio']):.2f}",
        "best_test_strategy": str(best_test["Strategy"]),
        "best_test_sharpe": f"{float(best_test['Sharpe Ratio']):.2f}",
        "test_same_as_full": test_same_as_full,
    }


def metrics_to_markdown_table(metrics: pd.DataFrame) -> str:
    display = metrics.copy()
    percent_columns = [
        "Cumulative Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
        "Win Rate",
        "Turnover",
    ]
    for column in percent_columns:
        if column in display.columns:
            display[column] = display[column].map(lambda value: format_percent(float(value)))
    if "Sharpe Ratio" in display.columns:
        display["Sharpe Ratio"] = display["Sharpe Ratio"].map(lambda value: f"{float(value):.2f}")

    return display.to_markdown(index=False)


def write_v7_markdown_reports(
    project_root: Path,
    ticker: str,
    full_metrics_path: Path,
    train_test_metrics_path: Path,
    data_start: str,
    data_end: str,
    train_start: str,
    train_end: str,
    test_start: str,
    test_end: str,
) -> tuple[Path, Path]:
    full_metrics = pd.read_csv(full_metrics_path)
    train_test_metrics = pd.read_csv(train_test_metrics_path)
    findings = get_key_findings(full_metrics, train_test_metrics)

    cn_path = project_root / "report_v7_cn.md"
    en_path = project_root / "report_v7_en.md"

    full_table = metrics_to_markdown_table(full_metrics)
    train_test_table = metrics_to_markdown_table(train_test_metrics)

    cn_lines = [
        "# US Stock Quant Toolkit：美股量化策略回测研究项目",
        "",
        "## 项目摘要",
        "",
        "这是一个用于学习和研究的 Python 美股量化回测项目。项目可以下载真实市场数据，测试多种策略，并比较收益和风险。",
        "",
        "## 数据来源",
        "",
        f"本项目使用 yfinance 下载 {ticker} 或其他美股 ETF/股票的历史价格数据。",
        "",
        "## 数据时间范围",
        "",
        f"Full period：{data_start} 到 {data_end}。",
        "",
        f"Train period：{train_start} 到 {train_end}。",
        "",
        f"Test period：{test_start} 到 {test_end}。",
        "",
        "## 策略设计",
        "",
        "- Buy and Hold：买入并持有。",
        "- 20/60 Moving Average：20 日均线高于 60 日均线时持有。",
        "- 50/200 Moving Average：50 日均线高于 200 日均线时持有。",
        "- RSI Mean Reversion：RSI 低于 30 时持有，高于 70 时空仓。",
        "- 6-Month Momentum：过去约 126 个交易日收益为正时持有。",
        "",
        "## 回测方法",
        "",
        "- 使用日收益率进行回测。",
        "- 所有交易信号使用 shift(1)，避免未来函数。",
        "- 加入交易成本 transaction_cost = 0.001。",
        "- 分为训练期和测试期。",
        "- 重点分析测试期结果。",
        "",
        "## 指标解释",
        "",
        "- Cumulative Return：累计收益。",
        "- Annualized Return：年化收益率。",
        "- Annualized Volatility：年化波动率。",
        "- Sharpe Ratio：风险调整后收益指标。",
        "- Maximum Drawdown：最大回撤。",
        "- Calmar Ratio：年化收益率除以最大回撤绝对值。",
        "- Win Rate：正收益交易日占比。",
        "- Number of Trades：交易次数。",
        "- Turnover：换手率或仓位变化频率。",
        "",
        "## 回测结果",
        "",
        "### 全样本结果",
        "",
        full_table,
        "",
        "### 训练期 / 测试期结果",
        "",
        train_test_table,
        "",
        "## 图表展示",
        "",
        "- outputs/v7_strategy_comparison_full.png",
        "- outputs/v7_strategy_comparison_test.png",
        "- outputs/v7_drawdown_comparison.png",
        "- outputs/v7_rolling_risk.png",
        "",
        "## 主要结论",
        "",
        f"- 累计收益较高的策略是 {findings['best_return_strategy']}，累计收益为 {findings['best_return_value']}。",
        f"- 回撤较低的策略是 {findings['lowest_drawdown_strategy']}，最大回撤为 {findings['lowest_drawdown_value']}。",
        f"- Sharpe Ratio 较高的策略是 {findings['best_sharpe_strategy']}，Sharpe Ratio 为 {findings['best_sharpe_value']}。",
        f"- 测试期 Sharpe Ratio 较高的策略是 {findings['best_test_strategy']}，Sharpe Ratio 为 {findings['best_test_sharpe']}。",
        f"- 样本外测试期最优策略是否与全样本累计收益最高策略一致：{findings['test_same_as_full']}。",
        "- 本项目已加入交易成本，因此频繁交易策略的表现会受到成本影响。",
        "",
        "## 项目局限性",
        "",
        "- 只使用历史数据。",
        "- 没有预测未来收益。",
        "- 没有考虑滑点、税费、流动性限制。",
        "- 单一资产测试不能代表所有市场环境。",
        "- 回测结果不等于未来表现。",
        "",
        "## 后续改进方向",
        "",
        "- 多资产组合。",
        "- 风险平价组合。",
        "- 参数优化。",
        "- Walk-forward validation。",
        "- Monte Carlo simulation。",
        "- 加入宏观因子或机器学习模型。",
        "",
        "## Disclaimer",
        "",
        DISCLAIMER,
        "",
    ]

    en_lines = [
        "# US Stock Quant Toolkit: A US Equity Quantitative Strategy Backtesting Project",
        "",
        "## Executive Summary",
        "",
        "This project is a Python-based quantitative research and backtesting toolkit. It downloads real market data, evaluates multiple rule-based strategies, and compares return and risk characteristics in a reproducible workflow.",
        "",
        "## Data Source",
        "",
        f"The project uses yfinance to download historical price data for {ticker} or other US-listed equities and ETFs.",
        "",
        "## Data Range",
        "",
        f"Full period: {data_start} to {data_end}.",
        "",
        f"Train period: {train_start} to {train_end}.",
        "",
        f"Test period: {test_start} to {test_end}.",
        "",
        "## Strategy Design",
        "",
        "- Buy and Hold: fully invested throughout the sample.",
        "- 20/60 Moving Average: invested when the 20-day moving average is above the 60-day moving average.",
        "- 50/200 Moving Average: invested when the 50-day moving average is above the 200-day moving average.",
        "- RSI Mean Reversion: invested when RSI is below 30 and out of the market when RSI is above 70.",
        "- 6-Month Momentum: invested when the trailing 126-trading-day return is positive.",
        "",
        "## Backtesting Methodology",
        "",
        "The backtest uses daily returns. All trading signals are shifted by one day with shift(1) to avoid look-ahead bias. Transaction cost is included through transaction_cost = 0.001. The sample is split into training and testing periods, and the testing period is emphasized for out-of-sample evaluation.",
        "",
        "## Transaction Cost Assumption",
        "",
        "A transaction cost of 0.001 is applied when positions change. This penalizes strategies that trade more frequently.",
        "",
        "## Train/Test Evaluation",
        "",
        "The training period is used to review in-sample behavior, while the testing period is used to evaluate whether strategy performance remains stable outside the initial sample.",
        "",
        "## Performance Metrics",
        "",
        "The project reports cumulative return, annualized return, annualized volatility, Sharpe Ratio, maximum drawdown, Calmar Ratio, win rate, number of trades, and turnover.",
        "",
        "## Empirical Results",
        "",
        "### Full Sample Results",
        "",
        full_table,
        "",
        "### Train/Test Results",
        "",
        train_test_table,
        "",
        "## Key Findings",
        "",
        f"- The highest cumulative return strategy is {findings['best_return_strategy']} with {findings['best_return_value']}.",
        f"- The lowest drawdown strategy is {findings['lowest_drawdown_strategy']} with {findings['lowest_drawdown_value']}.",
        f"- The highest Sharpe Ratio strategy is {findings['best_sharpe_strategy']} with a Sharpe Ratio of {findings['best_sharpe_value']}.",
        f"- The best testing-period Sharpe Ratio strategy is {findings['best_test_strategy']} with a Sharpe Ratio of {findings['best_test_sharpe']}.",
        f"- Whether the best testing-period strategy is consistent with the full-sample top return strategy: {findings['test_same_as_full']}.",
        "- Transaction costs reduce the performance of strategies with higher turnover.",
        "",
        "## Limitations",
        "",
        "This project only uses historical data and does not forecast future returns. It does not include slippage, taxes, liquidity constraints, or multi-asset portfolio effects. A single-asset backtest cannot represent all market environments.",
        "",
        "## Future Improvements",
        "",
        "Future work may include multi-asset portfolios, risk parity allocation, parameter optimization, walk-forward validation, Monte Carlo simulation, and macroeconomic or machine learning features.",
        "",
        "## Disclaimer",
        "",
        DISCLAIMER,
        "",
    ]

    cn_path.write_text("\n".join(cn_lines), encoding="utf-8")
    en_path.write_text("\n".join(en_lines), encoding="utf-8")
    return cn_path, en_path


def get_asset_findings(metrics: pd.DataFrame) -> dict[str, str]:
    """Create simple findings from an asset metrics table."""
    best_return = metrics.sort_values("Cumulative Return", ascending=False).iloc[0]
    best_sharpe = metrics.sort_values("Sharpe Ratio", ascending=False).iloc[0]
    lowest_drawdown = metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]

    return {
        "best_return": str(best_return["Ticker"]),
        "best_return_value": format_percent(float(best_return["Cumulative Return"])),
        "best_sharpe": str(best_sharpe["Ticker"]),
        "best_sharpe_value": f"{float(best_sharpe['Sharpe Ratio']):.2f}",
        "lowest_drawdown": str(lowest_drawdown["Ticker"]),
        "lowest_drawdown_value": format_percent(float(lowest_drawdown["Maximum Drawdown"])),
    }


def write_asset_comparison_reports(
    output_dir: Path,
    report_stem: str,
    title_cn: str,
    title_en: str,
    purpose_cn: str,
    purpose_en: str,
    tickers: list[str],
    metrics: pd.DataFrame,
    chart_files: list[str],
    failed_tickers: list[str] | None = None,
) -> tuple[Path, Path]:
    """Write Chinese and English Markdown reports for asset comparison modes."""
    failed_tickers = failed_tickers or []
    output_dir.mkdir(parents=True, exist_ok=True)
    cn_path = output_dir / f"report_{report_stem}_cn.md"
    en_path = output_dir / f"report_{report_stem}_en.md"
    findings = get_asset_findings(metrics)
    table = metrics_to_markdown_table(metrics)

    cn_lines = [
        f"# {title_cn}",
        "",
        "## 项目目标",
        "",
        purpose_cn,
        "",
        "## 数据来源",
        "",
        "本研究使用 yfinance 下载 Yahoo Finance 上的最新可用历史价格数据。本地 CSV 只是缓存，每次运行会尝试补充缺失数据。",
        "",
        "## 分析资产",
        "",
        ", ".join(tickers),
        "",
        "## 指标说明",
        "",
        "- Cumulative Return：从开始到结束的累计收益。",
        "- Annualized Return：把历史收益换算成年化收益。",
        "- Annualized Volatility：年化波动率，用来观察价格波动大小。",
        "- Sharpe Ratio：收益和风险的简单对比指标。",
        "- Maximum Drawdown：从历史高点到低点的最大下跌。",
        "- Calmar Ratio：年化收益和最大回撤的对比。",
        "",
        "## 结果表",
        "",
        table,
        "",
        "## 图表文件",
        "",
        *[f"- {file_name}" for file_name in chart_files],
        "",
        "## 主要发现",
        "",
        f"- 累计收益较高的资产是 {findings['best_return']}，累计收益为 {findings['best_return_value']}。",
        f"- Sharpe Ratio 较高的资产是 {findings['best_sharpe']}，Sharpe Ratio 为 {findings['best_sharpe_value']}。",
        f"- 最大回撤相对较低的资产是 {findings['lowest_drawdown']}，最大回撤为 {findings['lowest_drawdown_value']}。",
        "",
        "## 局限性",
        "",
        "- 本研究只使用历史数据，不能预测未来。",
        "- 不同资产的历史表现不能保证未来继续出现。",
        "- 没有考虑税费、滑点、流动性限制和真实交易执行问题。",
        "",
        "## 下载失败的资产",
        "",
        ", ".join(failed_tickers) if failed_tickers else "无。",
        "",
        "## 免责声明",
        "",
        "本项目只用于学习和研究，不构成投资建议，不连接券商，不自动交易，不下单。",
        "",
        DISCLAIMER,
        "",
    ]

    en_lines = [
        f"# {title_en}",
        "",
        "## Project Objective",
        "",
        purpose_en,
        "",
        "## Data Source",
        "",
        "This study uses yfinance to download the latest available historical price data from Yahoo Finance. Local CSV files are only cache files, and each run attempts to fill missing rows.",
        "",
        "## Analyzed Assets",
        "",
        ", ".join(tickers),
        "",
        "## Metrics",
        "",
        "- Cumulative Return: total return over the sample.",
        "- Annualized Return: return converted into an annualized figure.",
        "- Annualized Volatility: annualized standard deviation of daily returns.",
        "- Sharpe Ratio: a simple return-to-risk measure.",
        "- Maximum Drawdown: the largest decline from a historical peak.",
        "- Calmar Ratio: annualized return divided by the absolute maximum drawdown.",
        "",
        "## Results Table",
        "",
        table,
        "",
        "## Chart Files",
        "",
        *[f"- {file_name}" for file_name in chart_files],
        "",
        "## Key Findings",
        "",
        f"- The highest cumulative return asset is {findings['best_return']} with {findings['best_return_value']}.",
        f"- The highest Sharpe Ratio asset is {findings['best_sharpe']} with a Sharpe Ratio of {findings['best_sharpe_value']}.",
        f"- The relatively lowest drawdown asset is {findings['lowest_drawdown']} with a maximum drawdown of {findings['lowest_drawdown_value']}.",
        "",
        "## Limitations",
        "",
        "- The study only uses historical data and does not forecast future returns.",
        "- Historical asset performance may not persist in the future.",
        "- Taxes, slippage, liquidity constraints, and real execution issues are not included.",
        "",
        "## Failed Downloads",
        "",
        ", ".join(failed_tickers) if failed_tickers else "None.",
        "",
        "## Disclaimer",
        "",
        DISCLAIMER,
        "",
    ]

    cn_path.write_text("\n".join(cn_lines), encoding="utf-8")
    en_path.write_text("\n".join(en_lines), encoding="utf-8")
    return cn_path, en_path
