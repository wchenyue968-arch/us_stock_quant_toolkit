# US Stock Quant Toolkit

A Python toolkit for educational US equity and ETF quantitative research, historical backtesting, multi-asset comparison, professional report generation, and local Streamlit visualization.

## Project Overview

US Stock Quant Toolkit is a research-oriented Python project for analyzing US stocks and ETFs with historical market data. It supports rule-based strategy backtesting, multi-asset comparison, chart generation, Markdown/PDF reporting, and a local Streamlit web app.

The project is designed for learning, quantitative research practice, GitHub portfolio presentation, and graduate school application materials.

Important scope notes:

- This project uses the latest available historical market data.
- It does not use real-time market data.
- It does not connect to any brokerage account.
- It does not execute trades.
- It is for educational and research purposes only.
- It does not constitute investment advice.

## Key Features

- Download historical US stock and ETF data with `yfinance`.
- Cache data locally under `data/raw/{ticker}.csv`.
- Automatically update only missing historical data rows.
- Run a single-asset strategy backtest on SPY or another ticker.
- Compare multiple US stocks.
- Compare major US sector ETFs.
- Compare multi-asset ETFs such as stocks, bonds, and gold.
- Generate CSV outputs, PNG charts, Markdown reports, and PDF reports.
- Use a local Streamlit web app for interactive analysis and downloads.

## Research Modes

The project supports four research modes.

### 1. Single Asset Strategy Backtest

Default ticker:

```text
SPY
```

This mode runs the v7 single-asset strategy backtest and produces strategy metrics, cumulative return charts, drawdown charts, rolling risk charts, Markdown reports, and PDF reports.

### 2. Multi-Stock Comparison

Default tickers:

```text
AAPL, MSFT, NVDA, AMZN, GOOGL, META
```

This mode compares historical return, volatility, drawdown, Sharpe Ratio, and correlation for multiple large US stocks.

### 3. Sector ETF Comparison

Default tickers:

```text
XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLC, XLRE
```

This mode compares major US sector ETFs and produces performance ranking charts.

### 4. Multi-Asset Allocation Research

Default tickers:

```text
SPY, QQQ, TLT, IEF, GLD
```

This mode compares stock, bond, and gold ETFs. It also builds a simple equal-weight portfolio where the portfolio daily return is the average of available asset daily returns.

## Data Source

The project uses `yfinance` to download historical price data from Yahoo Finance.

The default data range is:

```text
2018-01-01 to the latest available historical trading day
```

Supported assets include any US stock or ETF that can be downloaded by `yfinance`.

Examples:

```text
Broad market ETFs: SPY, QQQ, DIA, IWM, VTI
Stocks: AAPL, MSFT, NVDA, TSLA, AMZN, META, GOOGL, JPM, XOM
Sector ETFs: XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLC, XLRE
Multi-asset ETFs: TLT, IEF, SHY, GLD, SLV, USO, UUP
```

## Data Update and Local Cache

Downloaded historical data is stored as a local CSV cache:

```text
data/raw/{ticker}.csv
```

Example:

```text
data/raw/SPY.csv
```

Each time the project runs, it checks the final date in the local cache. If the cache is outdated, the project downloads only the missing historical rows, merges the new data with the old data, removes duplicate dates, sorts by date, and saves the updated CSV.

If there is no new historical trading data, the program prints:

```text
No new trading data available.
```

If the network fails and a local cache exists, the project attempts to continue with the cached data. If the network fails and no cache exists, the project displays a clear error.

## Strategy Design

The single-asset strategy backtest includes:

- Buy and Hold
- 20/60 Moving Average Strategy
- 50/200 Moving Average Strategy
- RSI Mean Reversion Strategy
- 6-Month Momentum Strategy

No strategy connects to a brokerage account or sends orders.

## Backtesting Methodology

The backtest uses daily returns. Strategy positions are generated from historical indicators and then shifted by one trading day before calculating strategy returns.

The simplified strategy return formula is:

```text
strategy_return = position.shift(1) * daily_return - abs(position.diff()) * transaction_cost
```

This means today's return can only use yesterday's already-known position.

## Look-Ahead Bias Prevention

All strategy returns use shifted positions with `position.shift(1)`.

This prevents the backtest from using today's closing price signal to trade today's return. Instead, a signal generated from available historical information is applied to the next trading day.

This does not make the backtest perfect, but it is an important basic step for avoiding look-ahead bias.

## Transaction Cost

The default transaction cost is:

```text
transaction_cost = 0.001
```

Transaction cost is deducted when the position changes. This penalizes strategies that trade more frequently.

## Train/Test Split

The default split is:

```text
Full period: 2018-01-01 to the latest available historical trading day
Train period: 2018-01-01 to 2021-12-31
Test period: 2022-01-01 to the latest available historical trading day
```

The test period is used to review out-of-sample behavior.

## Performance Metrics

The project calculates metrics such as:

- Cumulative Return
- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Maximum Drawdown
- Calmar Ratio
- Win Rate
- Number of Trades
- Turnover

Multi-asset comparison modes calculate core return and risk metrics for each asset.

## Output Files

Single-asset v7 outputs:

```text
outputs/v7_full_strategy_metrics.csv
outputs/v7_train_test_metrics.csv
outputs/v7_strategy_returns.csv
outputs/v7_strategy_comparison_full.png
outputs/v7_strategy_comparison_test.png
outputs/v7_drawdown_comparison.png
outputs/v7_rolling_risk.png
report_v7_cn.md
report_v7_en.md
outputs/report_v7_cn.pdf
outputs/report_v7_en.pdf
outputs/report_v7_explained_cn.pdf
outputs/report_v7_explained_en.pdf
```

Multi-stock outputs:

```text
outputs/multi_stock_metrics.csv
outputs/multi_stock_cumulative_returns.png
outputs/multi_stock_drawdown.png
outputs/multi_stock_correlation.png
outputs/report_multi_stock_cn.md
outputs/report_multi_stock_en.md
```

Sector ETF outputs:

```text
outputs/sector_etf_metrics.csv
outputs/sector_etf_cumulative_returns.png
outputs/sector_etf_annual_return_ranking.png
outputs/sector_etf_max_drawdown_ranking.png
outputs/sector_etf_sharpe_ranking.png
outputs/report_sector_etf_cn.md
outputs/report_sector_etf_en.md
```

Multi-asset outputs:

```text
outputs/multi_asset_metrics.csv
outputs/multi_asset_cumulative_returns.png
outputs/multi_asset_correlation.png
outputs/equal_weight_portfolio_returns.csv
outputs/report_multi_asset_cn.md
outputs/report_multi_asset_en.md
```

## Streamlit Web App

The project includes a local Streamlit web app:

```text
app.py
```

The app supports:

- Research mode selection
- Preset portfolio selection
- Custom ticker input
- Start and end date settings
- Transaction cost setting
- Train/test split date setting
- Force refresh option
- Result table display
- Chart display
- Markdown and PDF report downloads

If a CSV, PNG, or PDF file has not been generated, the app displays a clear message instead of crashing.

## How to Run

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the command-line workflow:

```bash
.\.venv\Scripts\python.exe src\main.py
```

Run the Streamlit web app:

```bash
streamlit run app.py
```

On Windows, you can also double-click:

```text
run_app.bat
```

## Suggested GitHub Structure

```text

us_stock_quant_toolkit/

- app.py

- run_app.bat

- requirements.txt

- README.md

- docs/

  - application_materials.md

- src/

  - main.py

  - data_loader.py

  - indicators.py

  - strategies.py

  - backtester.py

  - metrics.py

  - plots.py

  - report_generator.py

  - pdf_report_generator.py

  - asset_universe.py

  - multi_asset_analysis.py

- outputs/

  - *.png

  - *.pdf
```

The local cache, virtual environment, Python cache files, and generated CSV files are excluded by `.gitignore`.

## Limitations

- The project only uses historical data.
- It does not predict future returns.
- It does not use real-time market data.
- It does not include slippage, taxes, or liquidity constraints.
- It does not model realistic order execution.
- Backtest results may be sensitive to the selected time period and parameters.
- A strategy that worked historically may not work in the future.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.

This project does not use real-time market data, does not connect to any brokerage account, and does not execute trades.

Historical backtest results do not guarantee future performance.

## Future Improvements

Potential future extensions include:

- More portfolio construction methods
- Risk parity allocation
- Parameter sensitivity analysis
- Walk-forward validation
- Monte Carlo simulation
- Better transaction cost and slippage modeling
- More polished Streamlit dashboard design
- Optional GitHub Actions checks
## Online Demo

This project can be deployed with Streamlit Cloud using `app.py` as the entry point.

Local run command:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
