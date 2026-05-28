# US Stock Quant Toolkit: A US Equity Quantitative Strategy Backtesting Project

## Executive Summary

This project is a Python-based quantitative research and backtesting toolkit. It downloads real market data, evaluates multiple rule-based strategies, and compares return and risk characteristics in a reproducible workflow.

## Data Source

The project uses yfinance to download historical price data for SPY or other US-listed equities and ETFs.

## Data Range

Full period: 2018-01-02 to 2026-05-27.

Train period: 2018-01-01 to 2021-12-31.

Test period: 2022-01-01 to 2026-05-27.

## Strategy Design

- Buy and Hold: fully invested throughout the sample.
- 20/60 Moving Average: invested when the 20-day moving average is above the 60-day moving average.
- 50/200 Moving Average: invested when the 50-day moving average is above the 200-day moving average.
- RSI Mean Reversion: invested when RSI is below 30 and out of the market when RSI is above 70.
- 6-Month Momentum: invested when the trailing 126-trading-day return is positive.

## Backtesting Methodology

The backtest uses daily returns. All trading signals are shifted by one day with shift(1) to avoid look-ahead bias. Transaction cost is included through transaction_cost = 0.001. The sample is split into training and testing periods, and the testing period is emphasized for out-of-sample evaluation.

## Transaction Cost Assumption

A transaction cost of 0.001 is applied when positions change. This penalizes strategies that trade more frequently.

## Train/Test Evaluation

The training period is used to review in-sample behavior, while the testing period is used to evaluate whether strategy performance remains stable outside the initial sample.

## Performance Metrics

The project reports cumulative return, annualized return, annualized volatility, Sharpe Ratio, maximum drawdown, Calmar Ratio, win rate, number of trades, and turnover.

## Empirical Results

### Full Sample Results

| Period   | Strategy              | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio | Win Rate   |   Number of Trades | Turnover   |
|:---------|:----------------------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|:-----------|-------------------:|:-----------|
| Full     | 20/60 Moving Average  | 87.75%              | 7.81%               | 12.16%                  |           0.64 | -27.12%            |       0.287966 | 39.03%     |                 35 | 1.66%      |
| Full     | 50/200 Moving Average | 103.14%             | 8.83%               | 15.55%                  |           0.57 | -33.72%            |       0.261849 | 39.98%     |                  9 | 0.43%      |
| Full     | 6-Month Momentum      | 72.28%              | 6.71%               | 12.36%                  |           0.54 | -23.96%            |       0.280009 | 40.12%     |                 67 | 3.17%      |
| Full     | Buy and Hold          | 216.92%             | 14.76%              | 19.21%                  |           0.77 | -33.72%            |       0.437836 | 55.33%     |                  1 | 0.05%      |
| Full     | RSI Mean Reversion    | 65.74%              | 6.22%               | 15.47%                  |           0.4  | -28.34%            |       0.219358 | 17.43%     |                 44 | 2.08%      |

### Train/Test Results

| Period   | Strategy              | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio | Win Rate   |   Number of Trades | Turnover   |
|:---------|:----------------------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|:-----------|-------------------:|:-----------|
| Full     | 20/60 Moving Average  | 87.75%              | 7.81%               | 12.16%                  |           0.64 | -27.12%            |       0.287966 | 39.03%     |                 35 | 1.66%      |
| Full     | 50/200 Moving Average | 103.14%             | 8.83%               | 15.55%                  |           0.57 | -33.72%            |       0.261849 | 39.98%     |                  9 | 0.43%      |
| Full     | 6-Month Momentum      | 72.28%              | 6.71%               | 12.36%                  |           0.54 | -23.96%            |       0.280009 | 40.12%     |                 67 | 3.17%      |
| Full     | Buy and Hold          | 216.92%             | 14.76%              | 19.21%                  |           0.77 | -33.72%            |       0.437836 | 55.33%     |                  1 | 0.05%      |
| Full     | RSI Mean Reversion    | 65.74%              | 6.22%               | 15.47%                  |           0.4  | -28.34%            |       0.219358 | 17.43%     |                 44 | 2.08%      |
| Train    | 20/60 Moving Average  | 65.43%              | 13.41%              | 12.90%                  |           1.04 | -12.44%            |       1.07824  | 41.96%     |                 13 | 1.29%      |
| Train    | 50/200 Moving Average | 34.90%              | 7.77%               | 17.48%                  |           0.44 | -33.72%            |       0.230457 | 37.90%     |                  5 | 0.50%      |
| Train    | 6-Month Momentum      | 31.33%              | 7.05%               | 13.38%                  |           0.53 | -23.96%            |       0.294303 | 38.59%     |                 19 | 1.88%      |
| Train    | Buy and Hold          | 89.21%              | 17.28%              | 20.80%                  |           0.83 | -33.72%            |       0.512599 | 56.94%     |                  1 | 0.10%      |
| Train    | RSI Mean Reversion    | 32.31%              | 7.25%               | 16.84%                  |           0.43 | -28.34%            |       0.255791 | 16.57%     |                 20 | 1.98%      |
| Test     | 20/60 Moving Average  | 13.49%              | 2.93%               | 11.44%                  |           0.26 | -26.42%            |       0.111038 | 36.36%     |                 22 | 1.99%      |
| Test     | 50/200 Moving Average | 50.59%              | 9.81%               | 13.57%                  |           0.72 | -18.76%            |       0.522797 | 41.89%     |                  4 | 0.36%      |
| Test     | 6-Month Momentum      | 31.18%              | 6.40%               | 11.35%                  |           0.56 | -22.84%            |       0.280052 | 41.52%     |                 48 | 4.35%      |
| Test     | Buy and Hold          | 67.49%              | 12.51%              | 17.64%                  |           0.71 | -24.50%            |       0.510538 | 53.85%     |                  0 | 0.00%      |
| Test     | RSI Mean Reversion    | 25.27%              | 5.28%               | 14.11%                  |           0.37 | -19.29%            |       0.273776 | 18.22%     |                 24 | 2.18%      |

## Key Findings

- The highest cumulative return strategy is Buy and Hold with 216.92%.
- The lowest drawdown strategy is 6-Month Momentum with -23.96%.
- The highest Sharpe Ratio strategy is Buy and Hold with a Sharpe Ratio of 0.77.
- The best testing-period Sharpe Ratio strategy is 50/200 Moving Average with a Sharpe Ratio of 0.72.
- Whether the best testing-period strategy is consistent with the full-sample top return strategy: no.
- Transaction costs reduce the performance of strategies with higher turnover.

## Limitations

This project only uses historical data and does not forecast future returns. It does not include slippage, taxes, liquidity constraints, or multi-asset portfolio effects. A single-asset backtest cannot represent all market environments.

## Future Improvements

Future work may include multi-asset portfolios, risk parity allocation, parameter optimization, walk-forward validation, Monte Carlo simulation, and macroeconomic or machine learning features.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
