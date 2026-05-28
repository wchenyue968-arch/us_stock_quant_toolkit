# v6 多策略回测对比报告

## Project Objective

本项目目标是在单只股票上对比多个常见策略的历史表现。默认测试 SPY。

## Data Source

数据来自 Yahoo Finance，使用 yfinance 下载 2018-01-01 到今天的历史价格数据。

## Tested Ticker

SPY

## Strategy Descriptions

Buy and Hold：从第一天买入，一直持有到最后一天。

20/60 Moving Average：20 日均线大于 60 日均线时持有，否则空仓。

50/200 Moving Average：50 日均线大于 200 日均线时持有，否则空仓。

RSI Mean Reversion：14 日 RSI 小于 30 时持有，大于 70 时空仓，其他时候保持上一期状态。

6-Month Momentum：过去约 126 个交易日收益率大于 0 时持有，否则空仓。

## Metrics Explanation

Total Return：整个回测期间的总收益率。

Annualized Return：把总收益换算成平均每年的收益率。

Annualized Volatility：年化波动率，表示策略收益波动大小。

Maximum Drawdown：最大回撤，表示从历史高点到低点的最大下跌幅度。

Sharpe Ratio：用来简单比较收益和波动。

Number of Trading Days in Market：策略实际持仓的交易日数量。

## Results Summary

本次回测中，总收益率最高的策略是 Buy and Hold，总收益率为 217.24%。

最大回撤相对较小的策略是 6-Month Momentum，最大回撤为 -23.34%。

不同策略的收益、波动和回撤差异明显。收益较高不一定代表风险较低。

## Limitations

本项目只使用历史价格数据，没有考虑交易成本、税费、滑点和真实成交限制。

策略规则很简单，不代表适合真实投资。

历史回测结果不代表未来表现。

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.

本项目只用于学习和研究，不构成投资建议。
