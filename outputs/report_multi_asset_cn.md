# 多资产 ETF 配置研究

## 项目目标

比较股票、债券和黄金 ETF 的历史表现，并加入一个简单等权重组合。

## 数据来源

本研究使用 yfinance 下载 Yahoo Finance 上的最新可用历史价格数据。本地 CSV 只是缓存，每次运行会尝试补充缺失数据。

## 分析资产

SPY, QQQ, TLT, IEF, GLD, Equal Weight Portfolio

## 指标说明

- Cumulative Return：从开始到结束的累计收益。
- Annualized Return：把历史收益换算成年化收益。
- Annualized Volatility：年化波动率，用来观察价格波动大小。
- Sharpe Ratio：收益和风险的简单对比指标。
- Maximum Drawdown：从历史高点到低点的最大下跌。
- Calmar Ratio：年化收益和最大回撤的对比。

## 结果表

| Ticker                 | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio |
|:-----------------------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|
| SPY                    | 217.24%             | 14.78%              | 19.22%                  |           0.77 | -33.72%            |      0.438465  |
| QQQ                    | 385.58%             | 20.77%              | 23.81%                  |           0.87 | -35.12%            |      0.591438  |
| TLT                    | -13.92%             | -1.77%              | 15.52%                  |          -0.11 | -48.35%            |     -0.0366955 |
| IEF                    | 9.17%               | 1.05%               | 6.93%                   |           0.15 | -23.92%            |      0.0440102 |
| GLD                    | 226.40%             | 15.17%              | 16.62%                  |           0.91 | -22.00%            |      0.689701  |
| Equal Weight Portfolio | 134.41%             | 10.71%              | 10.39%                  |           1.03 | -23.67%            |      0.452437  |

## 图表文件

- outputs/multi_asset_cumulative_returns.png
- outputs/multi_asset_correlation.png
- outputs/equal_weight_portfolio_returns.csv

## 主要发现

- 累计收益较高的资产是 QQQ，累计收益为 385.58%。
- Sharpe Ratio 较高的资产是 Equal Weight Portfolio，Sharpe Ratio 为 1.03。
- 最大回撤相对较低的资产是 GLD，最大回撤为 -22.00%。

## 局限性

- 本研究只使用历史数据，不能预测未来。
- 不同资产的历史表现不能保证未来继续出现。
- 没有考虑税费、滑点、流动性限制和真实交易执行问题。

## 下载失败的资产

无。

## 免责声明

本项目只用于学习和研究，不构成投资建议，不连接券商，不自动交易，不下单。

This project is for educational and research purposes only and does not constitute investment advice.
