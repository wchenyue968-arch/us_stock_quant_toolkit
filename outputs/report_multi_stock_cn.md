# 多只美股个股对比研究

## 项目目标

比较多只美股个股的历史收益、风险和相关性表现。

## 数据来源

本研究使用 yfinance 下载 Yahoo Finance 上的最新可用历史价格数据。本地 CSV 只是缓存，每次运行会尝试补充缺失数据。

## 分析资产

AAPL, MSFT, NVDA, AMZN, GOOGL, META

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
| AAPL     | 671.97%             | 27.65%              | 30.50%                  |           0.91 | -38.52%            |       0.717782 |
| MSFT     | 424.36%             | 21.88%              | 28.50%                  |           0.77 | -37.15%            |       0.589091 |
| NVDA     | 4213.89%            | 56.77%              | 50.68%                  |           1.12 | -66.34%            |       0.855761 |
| AMZN     | 357.27%             | 19.91%              | 34.22%                  |           0.58 | -56.15%            |       0.354567 |
| GOOGL    | 630.60%             | 26.81%              | 30.96%                  |           0.87 | -44.32%            |       0.604897 |
| META     | 252.91%             | 16.25%              | 41.37%                  |           0.39 | -76.74%            |       0.211817 |

## 图表文件

- outputs/multi_stock_cumulative_returns.png
- outputs/multi_stock_drawdown.png
- outputs/multi_stock_correlation.png

## 主要发现

- 累计收益较高的资产是 NVDA，累计收益为 4213.89%。
- Sharpe Ratio 较高的资产是 NVDA，Sharpe Ratio 为 1.12。
- 最大回撤相对较低的资产是 MSFT，最大回撤为 -37.15%。

## 局限性

- 本研究只使用历史数据，不能预测未来。
- 不同资产的历史表现不能保证未来继续出现。
- 没有考虑税费、滑点、流动性限制和真实交易执行问题。

## 下载失败的资产

无。

## 免责声明

本项目只用于学习和研究，不构成投资建议，不连接券商，不自动交易，不下单。

This project is for educational and research purposes only and does not constitute investment advice.
