# US Sector ETF Comparison Research

## Project Objective

Compare the historical return, risk, and risk-adjusted performance of major US sector ETFs.

## Data Source

This study uses yfinance to download the latest available historical price data from Yahoo Finance. Local CSV files are only cache files, and each run attempts to fill missing rows.

## Analyzed Assets

XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLC, XLRE

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
| XLK      | 517.38%             | 24.28%              | 26.23%                  |           0.93 | -33.56%            |       0.723633 |
| XLF      | 115.29%             | 9.59%               | 23.32%                  |           0.41 | -42.86%            |       0.223752 |
| XLE      | 121.34%             | 9.95%               | 31.48%                  |           0.32 | -66.81%            |       0.148986 |
| XLV      | 104.60%             | 8.93%               | 17.42%                  |           0.51 | -28.40%            |       0.314245 |
| XLY      | 162.67%             | 12.23%              | 23.66%                  |           0.52 | -39.67%            |       0.308175 |
| XLP      | 86.65%              | 7.74%               | 15.57%                  |           0.5  | -24.51%            |       0.315684 |
| XLI      | 163.08%             | 12.25%              | 21.28%                  |           0.58 | -42.33%            |       0.289269 |
| XLU      | 124.21%             | 10.12%              | 20.24%                  |           0.5  | -36.07%            |       0.280688 |
| XLC      | 150.97%             | 11.62%              | 22.21%                  |           0.52 | -46.65%            |       0.248989 |
| XLRE     | 79.69%              | 7.25%               | 21.64%                  |           0.33 | -38.82%            |       0.186737 |

## Chart Files

- outputs/sector_etf_cumulative_returns.png
- outputs/sector_etf_annual_return_ranking.png
- outputs/sector_etf_max_drawdown_ranking.png
- outputs/sector_etf_sharpe_ranking.png

## Key Findings

- The highest cumulative return asset is XLK with 517.38%.
- The highest Sharpe Ratio asset is XLK with a Sharpe Ratio of 0.93.
- The relatively lowest drawdown asset is XLP with a maximum drawdown of -24.51%.

## Limitations

- The study only uses historical data and does not forecast future returns.
- Historical asset performance may not persist in the future.
- Taxes, slippage, liquidity constraints, and real execution issues are not included.

## Failed Downloads

None.

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
