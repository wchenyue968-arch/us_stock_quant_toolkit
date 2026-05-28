# US Stock Quant Toolkit：美股量化策略回测研究项目

## 项目摘要

这是一个用于学习和研究的 Python 美股量化回测项目。项目可以下载真实市场数据，测试多种策略，并比较收益和风险。

## 数据来源

本项目使用 yfinance 下载 SPY 或其他美股 ETF/股票的历史价格数据。

## 数据时间范围

Full period：2018-01-02 到 2026-05-27。

Train period：2018-01-01 到 2021-12-31。

Test period：2022-01-01 到 2026-05-27。

## 策略设计

- Buy and Hold：买入并持有。
- 20/60 Moving Average：20 日均线高于 60 日均线时持有。
- 50/200 Moving Average：50 日均线高于 200 日均线时持有。
- RSI Mean Reversion：RSI 低于 30 时持有，高于 70 时空仓。
- 6-Month Momentum：过去约 126 个交易日收益为正时持有。

## 回测方法

- 使用日收益率进行回测。
- 所有交易信号使用 shift(1)，避免未来函数。
- 加入交易成本 transaction_cost = 0.001。
- 分为训练期和测试期。
- 重点分析测试期结果。

## 指标解释

- Cumulative Return：累计收益。
- Annualized Return：年化收益率。
- Annualized Volatility：年化波动率。
- Sharpe Ratio：风险调整后收益指标。
- Maximum Drawdown：最大回撤。
- Calmar Ratio：年化收益率除以最大回撤绝对值。
- Win Rate：正收益交易日占比。
- Number of Trades：交易次数。
- Turnover：换手率或仓位变化频率。

## 回测结果

### 全样本结果

| Period   | Strategy              | Cumulative Return   | Annualized Return   | Annualized Volatility   |   Sharpe Ratio | Maximum Drawdown   |   Calmar Ratio | Win Rate   |   Number of Trades | Turnover   |
|:---------|:----------------------|:--------------------|:--------------------|:------------------------|---------------:|:-------------------|---------------:|:-----------|-------------------:|:-----------|
| Full     | 20/60 Moving Average  | 87.75%              | 7.81%               | 12.16%                  |           0.64 | -27.12%            |       0.287966 | 39.03%     |                 35 | 1.66%      |
| Full     | 50/200 Moving Average | 103.14%             | 8.83%               | 15.55%                  |           0.57 | -33.72%            |       0.261849 | 39.98%     |                  9 | 0.43%      |
| Full     | 6-Month Momentum      | 72.28%              | 6.71%               | 12.36%                  |           0.54 | -23.96%            |       0.280009 | 40.12%     |                 67 | 3.17%      |
| Full     | Buy and Hold          | 216.92%             | 14.76%              | 19.21%                  |           0.77 | -33.72%            |       0.437836 | 55.33%     |                  1 | 0.05%      |
| Full     | RSI Mean Reversion    | 65.74%              | 6.22%               | 15.47%                  |           0.4  | -28.34%            |       0.219358 | 17.43%     |                 44 | 2.08%      |

### 训练期 / 测试期结果

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

## 图表展示

- outputs/v7_strategy_comparison_full.png
- outputs/v7_strategy_comparison_test.png
- outputs/v7_drawdown_comparison.png
- outputs/v7_rolling_risk.png

## 主要结论

- 累计收益较高的策略是 Buy and Hold，累计收益为 216.92%。
- 回撤较低的策略是 6-Month Momentum，最大回撤为 -23.96%。
- Sharpe Ratio 较高的策略是 Buy and Hold，Sharpe Ratio 为 0.77。
- 测试期 Sharpe Ratio 较高的策略是 50/200 Moving Average，Sharpe Ratio 为 0.72。
- 样本外测试期最优策略是否与全样本累计收益最高策略一致：no。
- 本项目已加入交易成本，因此频繁交易策略的表现会受到成本影响。

## 项目局限性

- 只使用历史数据。
- 没有预测未来收益。
- 没有考虑滑点、税费、流动性限制。
- 单一资产测试不能代表所有市场环境。
- 回测结果不等于未来表现。

## 后续改进方向

- 多资产组合。
- 风险平价组合。
- 参数优化。
- Walk-forward validation。
- Monte Carlo simulation。
- 加入宏观因子或机器学习模型。

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
