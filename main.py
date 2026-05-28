from datetime import date
from pathlib import Path
import os

import pandas as pd
import yfinance as yf


# Store matplotlib's cache inside the project folder.
os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).parent / ".matplotlib-cache"))

import matplotlib

# Use a backend that saves images without opening a window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


TRADING_DAYS_PER_YEAR = 252
DEFAULT_TICKERS = ["SPY", "AAPL", "MSFT", "NVDA", "QQQ"]
START_DATE = "2018-01-01"


def format_percent(value: float) -> str:
    """Convert a decimal number into a percentage string."""
    return f"{value * 100:.2f}%"


def get_user_tickers() -> list[str]:
    """Ask the user for one or more stock tickers."""
    prompt = (
        "请输入要分析的美股代码，多个代码用英文逗号分隔，例如：\n"
        "SPY,AAPL,MSFT,NVDA,QQQ\n"
        "直接按回车将使用默认组合 SPY,AAPL,MSFT,NVDA,QQQ："
    )

    # Read the user's input from the terminal.
    user_input = input(prompt).strip()

    # If the user presses Enter, use the default list.
    if not user_input:
        return DEFAULT_TICKERS

    # Split by comma, clean spaces, convert to uppercase, and remove empty values.
    tickers = [ticker.strip().upper() for ticker in user_input.split(",") if ticker.strip()]

    # If the input becomes empty after cleaning, still use the default list.
    if not tickers:
        return DEFAULT_TICKERS

    # Remove duplicate tickers while keeping the user's original order.
    unique_tickers = []
    for ticker in tickers:
        if ticker not in unique_tickers:
            unique_tickers.append(ticker)

    return unique_tickers


def download_price_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Download adjusted historical close prices for one ticker."""
    raw_data = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    # Stop with a clear error if yfinance returns no data.
    if raw_data.empty:
        raise ValueError(f"No price data was downloaded for {ticker}.")

    # Keep only the adjusted close price.
    data = raw_data[["Close"]].copy()
    data.columns = ["close"]

    # Remove any rows with missing prices.
    data = data.dropna()

    return data


def save_price_data(data: pd.DataFrame, output_path: Path) -> Path:
    """Save one ticker's price data to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # If the CSV is open in Excel or WPS, Windows may refuse to overwrite it.
    try:
        data.to_csv(output_path, index_label="date")
    except PermissionError:
        print(f"Warning: Could not overwrite {output_path}.")
        print("Please close this CSV if it is open in Excel/WPS, then run the program again.")

    return output_path


def add_return_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Add daily return, cumulative return, and drawdown columns."""
    result = data.copy()

    # Daily return compares today's close with yesterday's close.
    result["daily_return"] = result["close"].pct_change().fillna(0)

    # Cumulative return shows total growth since the first date.
    result["cumulative_return"] = (1 + result["daily_return"]).cumprod() - 1

    # Drawdown shows how far the strategy has fallen from its past high.
    equity_curve = 1 + result["cumulative_return"]
    result["drawdown"] = equity_curve / equity_curve.cummax() - 1

    return result


def calculate_metrics(ticker: str, data: pd.DataFrame) -> dict[str, float | str]:
    """Calculate key metrics for one ticker."""
    years = len(data) / TRADING_DAYS_PER_YEAR
    total_return = float(data["cumulative_return"].iloc[-1])
    annualized_return = (1 + total_return) ** (1 / years) - 1
    annualized_volatility = float(data["daily_return"].std() * (TRADING_DAYS_PER_YEAR**0.5))
    max_drawdown = float(data["drawdown"].min())

    if annualized_volatility == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = float(annualized_return / annualized_volatility)

    return {
        "ticker": ticker,
        "latest_close": float(data["close"].iloc[-1]),
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe_ratio,
    }


def save_metrics_summary(metrics: list[dict[str, float | str]], output_path: Path) -> pd.DataFrame:
    """Save the multi-stock metrics table to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(metrics)
    summary.to_csv(output_path, index=False)
    return summary


def create_cumulative_return_chart(analyzed_data: dict[str, pd.DataFrame], output_path: Path) -> Path:
    """Create a cumulative return comparison chart."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(15, 8))

    # Plot one cumulative return line for each ticker.
    for ticker, data in analyzed_data.items():
        axis.plot(data.index, data["cumulative_return"] * 100, linewidth=2, label=ticker)

    axis.set_title("V5 Multi-Stock Cumulative Return Comparison", fontsize=16, pad=14)
    axis.set_xlabel("Date")
    axis.set_ylabel("Cumulative Return (%)")
    axis.legend(title="Ticker")
    axis.grid(True, alpha=0.3)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    figure.tight_layout()
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)

    return output_path


def create_report(
    tickers: list[str],
    metrics_summary: pd.DataFrame,
    report_path: Path,
    metrics_path: Path,
    chart_path: Path,
) -> Path:
    """Create a simple Chinese Markdown report for v5."""
    best_total = metrics_summary.sort_values("total_return", ascending=False).iloc[0]
    lowest_drawdown = metrics_summary.sort_values("max_drawdown", ascending=False).iloc[0]

    lines = [
        "# US Stock Quant Toolkit v5 多股票对比报告",
        "",
        "## 1. 项目目标",
        "",
        "本项目用于学习和研究美股多股票对比分析。",
        "",
        "程序会一次分析多只美股，计算每只股票的关键指标，并生成累计收益对比图。",
        "",
        "## 2. 数据来源",
        "",
        "数据来自 Yahoo Finance。",
        "",
        "程序使用 yfinance 从 2018-01-01 下载到今天的最新历史价格数据。",
        "",
        "每次运行都会重新下载数据，不只读取旧 CSV。",
        "",
        "## 3. 分析的股票代码",
        "",
        ", ".join(tickers),
        "",
        "## 4. 每个指标是什么意思",
        "",
        "最新收盘价：数据中最后一个交易日的收盘价格。",
        "",
        "总收益率：从开始日期到结束日期，总共上涨或下跌了多少。",
        "",
        "年化收益率：把总收益换算成平均每年的收益。",
        "",
        "年化波动率：表示价格波动大小。数值越高，波动通常越大。",
        "",
        "最大回撤：表示从历史高点到低点，最大下跌了多少。",
        "",
        "Sharpe Ratio：用来简单比较收益和波动。它越高，说明单位波动带来的收益越高。",
        "",
        "## 5. 多股票对比图怎么看",
        "",
        "图表横轴是日期。",
        "",
        "图表纵轴是累计收益率。",
        "",
        "每一条线代表一只股票。",
        "",
        "线越高，说明这只股票在这段时间里的累计收益越高。",
        "",
        "但收益高不代表风险低，还需要同时看波动率和最大回撤。",
        "",
        "## 6. 主要发现",
        "",
        f"本次分析中，总收益率最高的是 {best_total['ticker']}，总收益率为 {format_percent(best_total['total_return'])}。",
        "",
        f"本次分析中，最大回撤相对较小的是 {lowest_drawdown['ticker']}，最大回撤为 {format_percent(lowest_drawdown['max_drawdown'])}。",
        "",
        "不同股票的收益和风险差异很大。",
        "",
        "只看收益是不够的，还要看波动率、最大回撤和 Sharpe Ratio。",
        "",
        "## 7. 局限性",
        "",
        "本项目只使用历史价格数据。",
        "",
        "它没有考虑公司基本面、估值、行业变化和宏观经济。",
        "",
        "它没有考虑交易成本、税费和滑点。",
        "",
        "历史表现不代表未来表现。",
        "",
        "## 8. 文件位置",
        "",
        f"指标对比表：{metrics_path}",
        "",
        f"累计收益对比图：{chart_path}",
        "",
        "## 9. 重要说明",
        "",
        "本项目只用于学习和研究。",
        "",
        "它不是投资建议。",
        "",
        "真实投资有风险，请不要只根据这个项目做投资决定。",
        "",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def print_summary(
    tickers: list[str],
    data_paths: dict[str, Path],
    metrics_path: Path,
    chart_path: Path,
    report_path: Path,
    metrics_summary: pd.DataFrame,
) -> None:
    """Print the v5 run summary."""
    print("US Stock Quant Toolkit V5")
    print("-------------------------")
    print(f"Tickers: {', '.join(tickers)}")
    print()

    for _, row in metrics_summary.iterrows():
        print(row["ticker"])
        print(f"  Latest close: {row['latest_close']:.2f}")
        print(f"  Total return: {format_percent(row['total_return'])}")
        print(f"  Annualized return: {format_percent(row['annualized_return'])}")
        print(f"  Annualized volatility: {format_percent(row['annualized_volatility'])}")
        print(f"  Maximum drawdown: {format_percent(row['max_drawdown'])}")
        print(f"  Sharpe Ratio: {row['sharpe_ratio']:.2f}")
        print(f"  Data file: {data_paths[row['ticker']]}")
        print()

    print(f"Metrics summary saved to: {metrics_path}")
    print(f"Comparison chart saved to: {chart_path}")
    print(f"Report saved to: {report_path}")


def run_v5_multi_stock_comparison() -> None:
    """Run the v5 multi-stock comparison workflow."""
    project_root = Path(__file__).parent
    data_folder = project_root / "data"
    outputs_folder = project_root / "outputs"
    end_date = date.today().isoformat()

    tickers = get_user_tickers()
    data_paths: dict[str, Path] = {}
    analyzed_data: dict[str, pd.DataFrame] = {}
    metrics: list[dict[str, float | str]] = []

    for ticker in tickers:
        # Download the latest data each time the program runs.
        price_data = download_price_data(ticker, START_DATE, end_date)

        # Save each ticker's downloaded data to the data folder.
        data_path = save_price_data(price_data, data_folder / f"{ticker}_price_data.csv")
        data_paths[ticker] = data_path

        # Calculate returns and risk columns.
        data_with_returns = add_return_columns(price_data)
        analyzed_data[ticker] = data_with_returns

        # Calculate one row of metrics for the summary table.
        metrics.append(calculate_metrics(ticker, data_with_returns))

    metrics_path = outputs_folder / "v5_metrics_summary.csv"
    chart_path = outputs_folder / "v5_cumulative_return_comparison.png"
    report_path = project_root / "report_v5.md"

    metrics_summary = save_metrics_summary(metrics, metrics_path)
    create_cumulative_return_chart(analyzed_data, chart_path)
    create_report(tickers, metrics_summary, report_path, metrics_path, chart_path)
    print_summary(tickers, data_paths, metrics_path, chart_path, report_path, metrics_summary)


def calculate_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index."""
    price_change = close.diff()
    gains = price_change.clip(lower=0)
    losses = -price_change.clip(upper=0)
    average_gain = gains.rolling(window=window).mean()
    average_loss = losses.rolling(window=window).mean()
    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    return rsi


def build_strategy_returns(price_data: pd.DataFrame) -> pd.DataFrame:
    """Build daily and cumulative returns for all v6 strategies."""
    data = price_data.copy()
    data["daily_return"] = data["close"].pct_change().fillna(0)
    data["ma_20"] = data["close"].rolling(window=20).mean()
    data["ma_50"] = data["close"].rolling(window=50).mean()
    data["ma_60"] = data["close"].rolling(window=60).mean()
    data["ma_200"] = data["close"].rolling(window=200).mean()
    data["rsi_14"] = calculate_rsi(data["close"], window=14)
    data["momentum_126"] = data["close"].pct_change(periods=126)

    strategy_returns = pd.DataFrame(index=data.index)
    strategy_returns["Buy and Hold"] = data["daily_return"]

    ma_20_60_signal = (data["ma_20"] > data["ma_60"]).astype(int)
    strategy_returns["20/60 Moving Average"] = data["daily_return"] * ma_20_60_signal.shift(1).fillna(0)

    ma_50_200_signal = (data["ma_50"] > data["ma_200"]).astype(int)
    strategy_returns["50/200 Moving Average"] = data["daily_return"] * ma_50_200_signal.shift(1).fillna(0)

    rsi_signal = pd.Series(index=data.index, dtype=float)
    rsi_signal.loc[data["rsi_14"] < 30] = 1
    rsi_signal.loc[data["rsi_14"] > 70] = 0
    rsi_signal = rsi_signal.ffill().fillna(0)
    strategy_returns["RSI Mean Reversion"] = data["daily_return"] * rsi_signal.shift(1).fillna(0)

    momentum_signal = (data["momentum_126"] > 0).astype(int)
    strategy_returns["6-Month Momentum"] = data["daily_return"] * momentum_signal.shift(1).fillna(0)

    combined = pd.DataFrame(index=data.index)
    for strategy_name in strategy_returns.columns:
        daily_column = f"{strategy_name} Daily Return"
        cumulative_column = f"{strategy_name} Cumulative Return"
        combined[daily_column] = strategy_returns[strategy_name].fillna(0)
        combined[cumulative_column] = (1 + combined[daily_column]).cumprod() - 1

    return combined


def calculate_strategy_metrics(strategy_returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate v6 metrics for every strategy."""
    metrics = []

    for column in strategy_returns.columns:
        if not column.endswith(" Daily Return"):
            continue

        strategy_name = column.replace(" Daily Return", "")
        daily_returns = strategy_returns[column]
        cumulative_returns = strategy_returns[f"{strategy_name} Cumulative Return"]
        equity_curve = 1 + cumulative_returns
        drawdown = equity_curve / equity_curve.cummax() - 1
        years = len(daily_returns) / TRADING_DAYS_PER_YEAR
        total_return = float(cumulative_returns.iloc[-1])
        annualized_return = (1 + total_return) ** (1 / years) - 1
        annualized_volatility = float(daily_returns.std() * (TRADING_DAYS_PER_YEAR**0.5))
        max_drawdown = float(drawdown.min())
        sharpe_ratio = 0.0 if annualized_volatility == 0 else float(annualized_return / annualized_volatility)
        trading_days_in_market = int((daily_returns != 0).sum())

        metrics.append(
            {
                "Strategy": strategy_name,
                "Total Return": total_return,
                "Annualized Return": annualized_return,
                "Annualized Volatility": annualized_volatility,
                "Maximum Drawdown": max_drawdown,
                "Sharpe Ratio": sharpe_ratio,
                "Number of Trading Days in Market": trading_days_in_market,
            }
        )

    return pd.DataFrame(metrics)


def create_v6_strategy_chart(strategy_returns: pd.DataFrame, ticker: str, output_path: Path) -> Path:
    """Create a cumulative return chart for all v6 strategies."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(15, 8))

    for column in strategy_returns.columns:
        if column.endswith(" Cumulative Return"):
            strategy_name = column.replace(" Cumulative Return", "")
            axis.plot(strategy_returns.index, strategy_returns[column] * 100, linewidth=2, label=strategy_name)

    axis.set_title(f"V6 Strategy Cumulative Return Comparison - {ticker}", fontsize=16, pad=14)
    axis.set_xlabel("Date")
    axis.set_ylabel("Cumulative Return (%)")
    axis.legend(title="Strategy")
    axis.grid(True, alpha=0.3)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    figure.tight_layout()
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return output_path


def create_v6_chinese_report(ticker: str, metrics: pd.DataFrame, report_path: Path) -> Path:
    """Create the v6 Chinese strategy report."""
    best_return = metrics.sort_values("Total Return", ascending=False).iloc[0]
    best_drawdown = metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]
    lines = [
        "# v6 多策略回测对比报告",
        "",
        "## Project Objective",
        "",
        "本项目目标是在单只股票上对比多个常见策略的历史表现。默认测试 SPY。",
        "",
        "## Data Source",
        "",
        "数据来自 Yahoo Finance，使用 yfinance 下载 2018-01-01 到今天的历史价格数据。",
        "",
        "## Tested Ticker",
        "",
        ticker,
        "",
        "## Strategy Descriptions",
        "",
        "Buy and Hold：从第一天买入，一直持有到最后一天。",
        "",
        "20/60 Moving Average：20 日均线大于 60 日均线时持有，否则空仓。",
        "",
        "50/200 Moving Average：50 日均线大于 200 日均线时持有，否则空仓。",
        "",
        "RSI Mean Reversion：14 日 RSI 小于 30 时持有，大于 70 时空仓，其他时候保持上一期状态。",
        "",
        "6-Month Momentum：过去约 126 个交易日收益率大于 0 时持有，否则空仓。",
        "",
        "## Metrics Explanation",
        "",
        "Total Return：整个回测期间的总收益率。",
        "",
        "Annualized Return：把总收益换算成平均每年的收益率。",
        "",
        "Annualized Volatility：年化波动率，表示策略收益波动大小。",
        "",
        "Maximum Drawdown：最大回撤，表示从历史高点到低点的最大下跌幅度。",
        "",
        "Sharpe Ratio：用来简单比较收益和波动。",
        "",
        "Number of Trading Days in Market：策略实际持仓的交易日数量。",
        "",
        "## Results Summary",
        "",
        f"本次回测中，总收益率最高的策略是 {best_return['Strategy']}，总收益率为 {format_percent(best_return['Total Return'])}。",
        "",
        f"最大回撤相对较小的策略是 {best_drawdown['Strategy']}，最大回撤为 {format_percent(best_drawdown['Maximum Drawdown'])}。",
        "",
        "不同策略的收益、波动和回撤差异明显。收益较高不一定代表风险较低。",
        "",
        "## Limitations",
        "",
        "本项目只使用历史价格数据，没有考虑交易成本、税费、滑点和真实成交限制。",
        "",
        "策略规则很简单，不代表适合真实投资。",
        "",
        "历史回测结果不代表未来表现。",
        "",
        "## Disclaimer",
        "",
        "This project is for educational and research purposes only and does not constitute investment advice.",
        "",
        "本项目只用于学习和研究，不构成投资建议。",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def create_v6_english_report(ticker: str, metrics: pd.DataFrame, report_path: Path) -> Path:
    """Create the v6 English strategy report."""
    best_return = metrics.sort_values("Total Return", ascending=False).iloc[0]
    best_drawdown = metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]
    lines = [
        "# V6 Multi-Strategy Backtest Report",
        "",
        "## Project Objective",
        "",
        "The objective is to compare multiple historical trading strategies on one ticker. The default tested ticker is SPY.",
        "",
        "## Data Source",
        "",
        "Price data comes from Yahoo Finance through yfinance, from 2018-01-01 to today.",
        "",
        "## Tested Ticker",
        "",
        ticker,
        "",
        "## Strategy Descriptions",
        "",
        "Buy and Hold: Buy on the first day and hold until the final day.",
        "",
        "20/60 Moving Average Strategy: Hold when the 20-day moving average is above the 60-day moving average. Otherwise stay in cash.",
        "",
        "50/200 Moving Average Strategy: Hold when the 50-day moving average is above the 200-day moving average. Otherwise stay in cash.",
        "",
        "RSI Mean Reversion Strategy: Hold when 14-day RSI is below 30, stay in cash when RSI is above 70, and otherwise keep the previous position.",
        "",
        "6-Month Momentum Strategy: Hold when the past 126-trading-day return is above 0. Otherwise stay in cash.",
        "",
        "## Metrics Explanation",
        "",
        "Total Return: Total gain or loss over the full backtest period.",
        "",
        "Annualized Return: Total return converted into an average yearly return.",
        "",
        "Annualized Volatility: Yearlyized volatility of daily strategy returns.",
        "",
        "Maximum Drawdown: The largest decline from a previous equity high.",
        "",
        "Sharpe Ratio: A simple comparison of return versus volatility.",
        "",
        "Number of Trading Days in Market: The number of days when the strategy had market exposure.",
        "",
        "## Results Summary",
        "",
        f"The highest total return strategy is {best_return['Strategy']} with a total return of {format_percent(best_return['Total Return'])}.",
        "",
        f"The smallest maximum drawdown strategy is {best_drawdown['Strategy']} with a maximum drawdown of {format_percent(best_drawdown['Maximum Drawdown'])}.",
        "",
        "Different strategies show different return and risk profiles. Higher return does not always mean lower risk.",
        "",
        "## Limitations",
        "",
        "This project only uses historical price data and does not include trading costs, taxes, slippage, or execution limits.",
        "",
        "The strategy rules are simple and are not designed as real trading recommendations.",
        "",
        "Historical backtest results do not guarantee future performance.",
        "",
        "## Disclaimer",
        "",
        "This project is for educational and research purposes only and does not constitute investment advice.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def build_v6_indicators(price_data: pd.DataFrame) -> pd.DataFrame:
    """Build the v6 indicator table."""
    indicators = price_data.copy()
    indicators["daily_return"] = indicators["close"].pct_change().fillna(0)
    indicators["ma_20"] = indicators["close"].rolling(window=20).mean()
    indicators["ma_50"] = indicators["close"].rolling(window=50).mean()
    indicators["ma_60"] = indicators["close"].rolling(window=60).mean()
    indicators["ma_200"] = indicators["close"].rolling(window=200).mean()
    indicators["rsi_14"] = calculate_rsi(indicators["close"], window=14)
    indicators["momentum_126"] = indicators["close"].pct_change(periods=126)
    return indicators


def build_v6_strategy_signals(indicators: pd.DataFrame) -> pd.DataFrame:
    """Build position signals for all v6 strategies."""
    signals = pd.DataFrame(index=indicators.index)
    signals["Buy and Hold"] = 1
    signals["20/60 Moving Average"] = (indicators["ma_20"] > indicators["ma_60"]).astype(int)
    signals["50/200 Moving Average"] = (indicators["ma_50"] > indicators["ma_200"]).astype(int)

    rsi_signal = pd.Series(index=indicators.index, dtype=float)
    rsi_signal.loc[indicators["rsi_14"] < 30] = 1
    rsi_signal.loc[indicators["rsi_14"] > 70] = 0
    signals["RSI Mean Reversion"] = rsi_signal.ffill().fillna(0).astype(int)

    signals["6-Month Momentum"] = (indicators["momentum_126"] > 0).astype(int)
    return signals


def build_v6_returns(indicators: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """Build daily and cumulative strategy return data."""
    returns = pd.DataFrame(index=indicators.index)

    for strategy_name in signals.columns:
        daily_column = f"{strategy_name} Daily Return"
        cumulative_column = f"{strategy_name} Cumulative Return"

        if strategy_name == "Buy and Hold":
            position = signals[strategy_name]
        else:
            position = signals[strategy_name].shift(1).fillna(0)

        returns[daily_column] = indicators["daily_return"] * position
        returns[cumulative_column] = (1 + returns[daily_column]).cumprod() - 1

    return returns


def build_v6_trade_log(signals: pd.DataFrame) -> pd.DataFrame:
    """Create a simple trade log from signal changes."""
    rows = []

    for strategy_name in signals.columns:
        previous_position = 0

        for trade_date, position in signals[strategy_name].items():
            position = int(position)

            if position != previous_position:
                if position == 1:
                    action = "BUY"
                else:
                    action = "SELL"

                rows.append(
                    {
                        "date": trade_date,
                        "strategy": strategy_name,
                        "action": action,
                        "position": position,
                    }
                )

                previous_position = position

    return pd.DataFrame(rows)


def calculate_v6_strategy_metrics(strategy_returns: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """Calculate v6 metrics for every strategy."""
    metrics = []

    for strategy_name in signals.columns:
        daily_column = f"{strategy_name} Daily Return"
        cumulative_column = f"{strategy_name} Cumulative Return"
        daily_returns = strategy_returns[daily_column]
        cumulative_returns = strategy_returns[cumulative_column]
        equity_curve = 1 + cumulative_returns
        drawdown = equity_curve / equity_curve.cummax() - 1
        years = len(daily_returns) / TRADING_DAYS_PER_YEAR
        total_return = float(cumulative_returns.iloc[-1])
        annualized_return = (1 + total_return) ** (1 / years) - 1
        annualized_volatility = float(daily_returns.std() * (TRADING_DAYS_PER_YEAR**0.5))
        max_drawdown = float(drawdown.min())
        sharpe_ratio = 0.0 if annualized_volatility == 0 else float(annualized_return / annualized_volatility)

        metrics.append(
            {
                "Strategy": strategy_name,
                "Total Return": total_return,
                "Annualized Return": annualized_return,
                "Annualized Volatility": annualized_volatility,
                "Maximum Drawdown": max_drawdown,
                "Sharpe Ratio": sharpe_ratio,
                "Number of Trading Days in Market": int(signals[strategy_name].sum()),
            }
        )

    return pd.DataFrame(metrics)


def build_v6_monthly_returns(strategy_returns: pd.DataFrame) -> pd.DataFrame:
    """Build monthly compounded strategy returns."""
    daily_columns = [column for column in strategy_returns.columns if column.endswith(" Daily Return")]
    monthly = pd.DataFrame(index=strategy_returns.resample("ME").last().index)

    for daily_column in daily_columns:
        strategy_name = daily_column.replace(" Daily Return", "")
        monthly[strategy_name] = strategy_returns[daily_column].resample("ME").apply(lambda values: (1 + values).prod() - 1)

    return monthly


def create_v6_quant_chart(strategy_returns: pd.DataFrame, ticker: str, output_path: Path) -> Path:
    """Create the v6 cumulative return strategy chart."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(15, 8))

    for column in strategy_returns.columns:
        if column.endswith(" Cumulative Return"):
            strategy_name = column.replace(" Cumulative Return", "")
            axis.plot(strategy_returns.index, strategy_returns[column] * 100, linewidth=2, label=strategy_name)

    axis.set_title(f"{ticker} V6 Strategy Backtest Comparison", fontsize=16, pad=14)
    axis.set_xlabel("Date")
    axis.set_ylabel("Cumulative Return (%)")
    axis.legend(title="Strategy")
    axis.grid(True, alpha=0.3)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    figure.tight_layout()
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return output_path


def write_v6_markdown_reports(ticker: str, metrics: pd.DataFrame, reports_folder: Path) -> tuple[Path, Path]:
    """Write Chinese and English Markdown reports in the reports folder."""
    reports_folder.mkdir(parents=True, exist_ok=True)
    cn_path = reports_folder / "report_cn.md"
    en_path = reports_folder / "report_en.md"

    best_return = metrics.sort_values("Total Return", ascending=False).iloc[0]
    best_drawdown = metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]

    cn_lines = [
        "# v6 多策略回测报告",
        "",
        "## Project Objective",
        "",
        "本项目目标是在单只股票上对比多个策略的历史表现。默认测试 SPY。",
        "",
        "## Data Source",
        "",
        "数据来自 Yahoo Finance，使用 yfinance 下载 2018-01-01 到今天的历史价格数据。",
        "",
        "## Tested Ticker",
        "",
        ticker,
        "",
        "## Strategy Descriptions",
        "",
        "Buy and Hold：从第一天买入并一直持有到最后一天。",
        "",
        "20/60 Moving Average：20 日均线大于 60 日均线时持有，否则空仓。",
        "",
        "50/200 Moving Average：50 日均线大于 200 日均线时持有，否则空仓。",
        "",
        "RSI Mean Reversion：14 日 RSI 小于 30 时持有，大于 70 时空仓，其他时候保持上一期状态。",
        "",
        "6-Month Momentum：过去约 126 个交易日收益率大于 0 时持有，否则空仓。",
        "",
        "## Metrics Explanation",
        "",
        "Total Return：整个回测期间的总收益率。",
        "",
        "Annualized Return：把总收益换算成平均每年的收益率。",
        "",
        "Annualized Volatility：年化波动率，表示策略收益的波动大小。",
        "",
        "Maximum Drawdown：最大回撤，表示从历史高点到低点的最大下跌幅度。",
        "",
        "Sharpe Ratio：用来简单比较收益和波动。",
        "",
        "Number of Trading Days in Market：策略实际持仓的交易日数量。",
        "",
        "## Results Summary",
        "",
        f"本次回测中，总收益率最高的策略是 {best_return['Strategy']}，总收益率为 {format_percent(best_return['Total Return'])}。",
        "",
        f"最大回撤相对较小的策略是 {best_drawdown['Strategy']}，最大回撤为 {format_percent(best_drawdown['Maximum Drawdown'])}。",
        "",
        "收益较高不代表风险较低，需要同时观察波动率、最大回撤和持仓天数。",
        "",
        "## Limitations",
        "",
        "本项目只使用历史价格数据，没有考虑交易成本、税费、滑点和真实成交限制。",
        "",
        "策略规则较简单，不代表适合真实投资。",
        "",
        "历史回测结果不代表未来表现。",
        "",
        "## Disclaimer",
        "",
        "This project is for educational and research purposes only and does not constitute investment advice.",
        "",
        "本项目只用于学习和研究，不构成投资建议。",
        "",
    ]

    en_lines = [
        "# V6 Multi-Strategy Backtest Report",
        "",
        "## Project Objective",
        "",
        "This project compares multiple historical trading strategies on one ticker. The default tested ticker is SPY.",
        "",
        "## Data Source",
        "",
        "Price data comes from Yahoo Finance through yfinance, from 2018-01-01 to today.",
        "",
        "## Tested Ticker",
        "",
        ticker,
        "",
        "## Strategy Descriptions",
        "",
        "Buy and Hold: Buy on the first day and hold until the final day.",
        "",
        "20/60 Moving Average Strategy: Hold when the 20-day moving average is above the 60-day moving average. Otherwise stay in cash.",
        "",
        "50/200 Moving Average Strategy: Hold when the 50-day moving average is above the 200-day moving average. Otherwise stay in cash.",
        "",
        "RSI Mean Reversion Strategy: Hold when 14-day RSI is below 30, stay in cash when RSI is above 70, and otherwise keep the previous position.",
        "",
        "6-Month Momentum Strategy: Hold when the past 126-trading-day return is above 0. Otherwise stay in cash.",
        "",
        "## Metrics Explanation",
        "",
        "Total Return: Total gain or loss over the full backtest period.",
        "",
        "Annualized Return: Total return converted into an average yearly return.",
        "",
        "Annualized Volatility: Annualized volatility of daily strategy returns.",
        "",
        "Maximum Drawdown: The largest decline from a previous equity high.",
        "",
        "Sharpe Ratio: A simple comparison of return versus volatility.",
        "",
        "Number of Trading Days in Market: The number of days when the strategy had market exposure.",
        "",
        "## Results Summary",
        "",
        f"The highest total return strategy is {best_return['Strategy']} with a total return of {format_percent(best_return['Total Return'])}.",
        "",
        f"The smallest maximum drawdown strategy is {best_drawdown['Strategy']} with a maximum drawdown of {format_percent(best_drawdown['Maximum Drawdown'])}.",
        "",
        "Higher return does not always mean lower risk. Volatility, drawdown, and market exposure should also be reviewed.",
        "",
        "## Limitations",
        "",
        "This project only uses historical price data and does not include trading costs, taxes, slippage, or execution limits.",
        "",
        "The strategy rules are simple and are not designed as real trading recommendations.",
        "",
        "Historical backtest results do not guarantee future performance.",
        "",
        "## Disclaimer",
        "",
        "This project is for educational and research purposes only and does not constitute investment advice.",
        "",
    ]

    cn_path.write_text("\n".join(cn_lines), encoding="utf-8")
    en_path.write_text("\n".join(en_lines), encoding="utf-8")
    return cn_path, en_path


def markdown_to_pdf(markdown_path: Path, pdf_path: Path, language: str) -> tuple[bool, str | None]:
    """Convert Markdown to PDF with reportlab."""
    try:
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as error:
        return False, str(error)

    font_name = "Helvetica"
    if language == "cn":
        font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
        if font_path.exists():
            font_name = "MicrosoftYaHei"
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=20,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=14,
        leading=20,
        spaceBefore=12,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=10.5,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=6,
    )

    story = []
    for raw_line in markdown_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 4))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading_style))
        else:
            clean_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(clean_line, body_style))

    try:
        document = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=1.8 * cm,
            leftMargin=1.8 * cm,
            topMargin=1.6 * cm,
            bottomMargin=1.6 * cm,
        )
        document.build(story)
        return True, None
    except Exception as error:
        return False, str(error)


def markdown_to_html(markdown_path: Path, html_path: Path) -> Path:
    """Create an HTML fallback if PDF generation fails."""
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    body = []

    for line in lines:
        if line.startswith("# "):
            body.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{line[3:]}</h2>")
        elif line:
            body.append(f"<p>{line}</p>")
        else:
            body.append("<br>")

    html = "\n".join(
        [
            "<!doctype html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8">',
            "<style>body{font-family:Arial,'Microsoft YaHei',sans-serif;line-height:1.6;margin:40px;} h1,h2{color:#1f4e79;}</style>",
            "</head>",
            "<body>",
            *body,
            "</body>",
            "</html>",
        ]
    )
    html_path.write_text(html, encoding="utf-8")
    return html_path


def run_v6_strategy_backtest() -> None:
    """Run the v6 multi-strategy backtest on SPY."""
    ticker = "SPY"
    project_root = Path(__file__).parent
    data_folder = project_root / "data"
    outputs_folder = project_root / "outputs"
    reports_folder = project_root / "reports"
    end_date = date.today().isoformat()

    price_data = download_price_data(ticker, START_DATE, end_date)
    raw_data_path = save_price_data(price_data, data_folder / f"{ticker}_raw_price_data.csv")

    indicators = build_v6_indicators(price_data)
    signals = build_v6_strategy_signals(indicators)
    strategy_returns = build_v6_returns(indicators, signals)
    trade_log = build_v6_trade_log(signals)
    metrics = calculate_v6_strategy_metrics(strategy_returns, signals)
    monthly_returns = build_v6_monthly_returns(strategy_returns)

    indicators_path = outputs_folder / f"{ticker}_indicators.csv"
    signals_path = outputs_folder / f"{ticker}_strategy_signals.csv"
    trade_log_path = outputs_folder / f"{ticker}_trade_log.csv"
    metrics_path = outputs_folder / f"{ticker}_metrics_summary.csv"
    monthly_returns_path = outputs_folder / f"{ticker}_monthly_returns.csv"
    chart_path = outputs_folder / f"{ticker}_quant_analysis_v6.png"
    returns_path = outputs_folder / "v6_strategy_returns.csv"

    outputs_folder.mkdir(parents=True, exist_ok=True)
    indicators.to_csv(indicators_path, index_label="date")
    signals.to_csv(signals_path, index_label="date")
    trade_log.to_csv(trade_log_path, index=False)
    metrics.to_csv(metrics_path, index=False)
    monthly_returns.to_csv(monthly_returns_path, index_label="date")
    strategy_returns.to_csv(returns_path, index_label="date")
    create_v6_quant_chart(strategy_returns, ticker, chart_path)

    cn_report_path, en_report_path = write_v6_markdown_reports(ticker, metrics, reports_folder)
    cn_pdf_path = reports_folder / "report_cn.pdf"
    en_pdf_path = reports_folder / "report_en.pdf"
    cn_pdf_ok, cn_pdf_error = markdown_to_pdf(cn_report_path, cn_pdf_path, "cn")
    en_pdf_ok, en_pdf_error = markdown_to_pdf(en_report_path, en_pdf_path, "en")

    cn_html_path = None
    en_html_path = None
    if not cn_pdf_ok:
        cn_html_path = markdown_to_html(cn_report_path, reports_folder / "report_cn.html")
    if not en_pdf_ok:
        en_html_path = markdown_to_html(en_report_path, reports_folder / "report_en.html")

    print("US Stock Quant Toolkit V6")
    print("-------------------------")
    print(f"Tested ticker: {ticker}")
    print(f"Raw price data saved to: {raw_data_path}")
    print(f"Indicators saved to: {indicators_path}")
    print(f"Strategy signals saved to: {signals_path}")
    print(f"Trade log saved to: {trade_log_path}")
    print(f"Metrics summary saved to: {metrics_path}")
    print(f"Monthly returns saved to: {monthly_returns_path}")
    print(f"V6 chart saved to: {chart_path}")
    print(f"Strategy returns saved to: {returns_path}")
    print(f"Chinese Markdown report saved to: {cn_report_path}")
    print(f"English Markdown report saved to: {en_report_path}")
    print(f"Chinese PDF report saved to: {cn_pdf_path if cn_pdf_ok else 'PDF failed'}")
    print(f"English PDF report saved to: {en_pdf_path if en_pdf_ok else 'PDF failed'}")

    if not cn_pdf_ok:
        print(f"Chinese PDF error: {cn_pdf_error}")
        print(f"Chinese HTML fallback saved to: {cn_html_path}")
    if not en_pdf_ok:
        print(f"English PDF error: {en_pdf_error}")
        print(f"English HTML fallback saved to: {en_html_path}")


def main() -> None:
    """Run the current v6 workflow by default."""
    run_v6_strategy_backtest()


if __name__ == "__main__":
    main()
