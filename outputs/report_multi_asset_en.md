# Multi-Asset Allocation Research

## Project Objective

Compare stock, bond, and gold ETFs, and include a simple equal-weight portfolio.

## Data Source

This study uses yfinance to download the latest available historical price data from Yahoo Finance. Local CSV files are only cache files, and each run attempts to fill missing rows.

## Analyzed Assets

SPY, QQQ, TLT, IEF, GLD, Equal Weight Portfolio

## Metrics

- Cumulative Return: total return over the sample.
- Annualized Return: return converted into an annualized figure.
- Annualized Volatility: annualized standard deviation of daily returns.
- Sharpe Ratio: a simple return-to-risk measure.
- Maximum Drawdown: the largest decline from a historical peak.
- Calmar Ratio: annualized return divided by the absolute maximum drawdown.

## Results Table

| Ticker                 | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio |
|:-----------------------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|
| SPY                    | 217.24%             | 14.78%              | 19.22%                  |           0.77 | -33.72%            |      0.438465  |
| QQQ                    | 385.58%             | 20.77%              | 23.81%                  |           0.87 | -35.12%            |      0.591438  |
| TLT                    | -13.92%             | -1.77%              | 15.52%                  |          -0.11 | -48.35%            |     -0.0366955 |
| IEF                    | 9.17%               | 1.05%               | 6.93%                   |           0.15 | -23.92%            |      0.0440102 |
| GLD                    | 226.40%             | 15.17%              | 16.62%                  |           0.91 | -22.00%            |      0.689701  |
| Equal Weight Portfolio | 134.41%             | 10.71%              | 10.39%                  |           1.03 | -23.67%            |      0.452437  |

## Chart Files

- outputs/multi_asset_cumulative_returns.png
- outputs/multi_asset_correlation.png
- outputs/equal_weight_portfolio_returns.csv

## Key Findings

- The highest cumulative return asset is QQQ with 385.58%.
- The highest Sharpe Ratio asset is Equal Weight Portfolio with a Sharpe Ratio of 1.03.
- The relatively lowest drawdown asset is GLD with a maximum drawdown of -22.00%.

## Limitations

- The study only uses historical data and does not forecast future returns.
- Historical asset performance may not persist in the future.
- Taxes, slippage, liquidity constraints, and real execution issues are not included.

## Failed Downloads

None.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
