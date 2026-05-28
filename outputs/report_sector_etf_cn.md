# 美国行业 ETF 对比研究

## 项目目标

比较美国不同行业 ETF 的历史收益、风险和风险调整后表现。

## 数据来源

本研究使用 yfinance 下载 Yahoo Finance 上的最新可用历史价格数据。本地 CSV 只是缓存，每次运行会尝试补充缺失数据。

## 分析资产

XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLC, XLRE

## 指标说明

- Cumulative Return：从开始到结束的累计收益。
- Annualized Return：把历史收益换算成年化收益。
- Annualized Volatility：年化波动率，用来观察价格波动大小。
- Sharpe Ratio：收益和风险的简单对比指标。
- Maximum Drawdown：从历史高点到低点的最大下跌。
- Calmar Ratio：年化收益和最大回撤的对比。

## 结果表

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

## 图表文件

- outputs/sector_etf_cumulative_returns.png
- outputs/sector_etf_annual_return_ranking.png
- outputs/sector_etf_max_drawdown_ranking.png
- outputs/sector_etf_sharpe_ranking.png

## 主要发现

- 累计收益较高的资产是 XLK，累计收益为 517.38%。
- Sharpe Ratio 较高的资产是 XLK，Sharpe Ratio 为 0.93。
- 最大回撤相对较低的资产是 XLP，最大回撤为 -24.51%。

## 局限性

- 本研究只使用历史数据，不能预测未来。
- 不同资产的历史表现不能保证未来继续出现。
- 没有考虑税费、滑点、流动性限制和真实交易执行问题。

## 下载失败的资产

无。

## 免责声明

本项目只用于学习和研究，不构成投资建议，不连接券商，不自动交易，不下单。

This project is for educational and research purposes only and does not constitute investment advice.
