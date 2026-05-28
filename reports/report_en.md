# V6 Multi-Strategy Backtest Report

## Project Objective

This project compares multiple historical trading strategies on one ticker. The default tested ticker is SPY.

## Data Source

Price data comes from Yahoo Finance through yfinance, from 2018-01-01 to today.

## Tested Ticker

SPY

## Strategy Descriptions

Buy and Hold: Buy on the first day and hold until the final day.

20/60 Moving Average Strategy: Hold when the 20-day moving average is above the 60-day moving average. Otherwise stay in cash.

50/200 Moving Average Strategy: Hold when the 50-day moving average is above the 200-day moving average. Otherwise stay in cash.

RSI Mean Reversion Strategy: Hold when 14-day RSI is below 30, stay in cash when RSI is above 70, and otherwise keep the previous position.

6-Month Momentum Strategy: Hold when the past 126-trading-day return is above 0. Otherwise stay in cash.

## Metrics Explanation

Total Return: Total gain or loss over the full backtest period.

Annualized Return: Total return converted into an average yearly return.

Annualized Volatility: Annualized volatility of daily strategy returns.

Maximum Drawdown: The largest decline from a previous equity high.

Sharpe Ratio: A simple comparison of return versus volatility.

Number of Trading Days in Market: The number of days when the strategy had market exposure.

## Results Summary

The highest total return strategy is Buy and Hold with a total return of 217.24%.

The smallest maximum drawdown strategy is 6-Month Momentum with a maximum drawdown of -23.34%.

Higher return does not always mean lower risk. Volatility, drawdown, and market exposure should also be reviewed.

## Limitations

This project only uses historical price data and does not include trading costs, taxes, slippage, or execution limits.

The strategy rules are simple and are not designed as real trading recommendations.

Historical backtest results do not guarantee future performance.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
