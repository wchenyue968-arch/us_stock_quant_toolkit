# Multi-Stock Comparison Research

## Project Objective

Compare the historical return, risk, and correlation characteristics of several US stocks.

## Data Source

This study uses yfinance to download the latest available historical price data from Yahoo Finance. Local CSV files are only cache files, and each run attempts to fill missing rows.

## Analyzed Assets

AAPL, MSFT, NVDA, AMZN, GOOGL, META

## Metrics

- Cumulative Return: total return over the sample.
- Annualized Return: return converted into an annualized figure.
- Annualized Volatility: annualized standard deviation of daily returns.
- Sharpe Ratio: a simple return-to-risk measure.
- Maximum Drawdown: the largest decline from a historical peak.
- Calmar Ratio: annualized return divided by the absolute maximum drawdown.

## Results Table

| Ticker   | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio |
|:---------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|
| AAPL     | 671.97%             | 27.65%              | 30.50%                  |           0.91 | -38.52%            |       0.717782 |
| MSFT     | 424.36%             | 21.88%              | 28.50%                  |           0.77 | -37.15%            |       0.589091 |
| NVDA     | 4213.89%            | 56.77%              | 50.68%                  |           1.12 | -66.34%            |       0.855761 |
| AMZN     | 357.27%             | 19.91%              | 34.22%                  |           0.58 | -56.15%            |       0.354567 |
| GOOGL    | 630.60%             | 26.81%              | 30.96%                  |           0.87 | -44.32%            |       0.604897 |
| META     | 252.91%             | 16.25%              | 41.37%                  |           0.39 | -76.74%            |       0.211817 |

## Chart Files

- outputs/multi_stock_cumulative_returns.png
- outputs/multi_stock_drawdown.png
- outputs/multi_stock_correlation.png

## Key Findings

- The highest cumulative return asset is NVDA with 4213.89%.
- The highest Sharpe Ratio asset is NVDA with a Sharpe Ratio of 1.12.
- The relatively lowest drawdown asset is MSFT with a maximum drawdown of -37.15%.

## Limitations

- The study only uses historical data and does not forecast future returns.
- Historical asset performance may not persist in the future.
- Taxes, slippage, liquidity constraints, and real execution issues are not included.

## Failed Downloads

None.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
