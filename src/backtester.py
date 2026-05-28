import pandas as pd


def apply_strategy_returns(
    indicators: pd.DataFrame,
    signals: pd.DataFrame,
    transaction_cost: float,
) -> pd.DataFrame:
    """Apply v7 backtest returns with one-day shifted positions.

    Formula:
    strategy_return = position.shift(1) * daily_return - abs(position.diff()) * transaction_cost
    """
    output = pd.DataFrame(index=indicators.index)
    daily_return = indicators["daily_return"]

    for strategy in signals.columns:
        raw_position = signals[strategy].astype(float)
        tradable_position = raw_position.shift(1).fillna(0)
        turnover = raw_position.diff().abs().fillna(raw_position.abs())
        strategy_return = tradable_position * daily_return - turnover * transaction_cost

        output[f"{strategy} Signal"] = raw_position
        output[f"{strategy} Position"] = tradable_position
        output[f"{strategy} Turnover"] = turnover
        output[f"{strategy} Daily Return"] = strategy_return
        output[f"{strategy} Cumulative Return"] = (1 + strategy_return).cumprod() - 1
        equity = 1 + output[f"{strategy} Cumulative Return"]
        output[f"{strategy} Drawdown"] = equity / equity.cummax() - 1

    return output


def build_trade_log(signals: pd.DataFrame) -> pd.DataFrame:
    """Build a simple trade log from strategy signal changes."""
    rows = []

    for strategy in signals.columns:
        previous = 0
        for trade_date, value in signals[strategy].items():
            current = int(value)
            if current != previous:
                rows.append(
                    {
                        "date": trade_date,
                        "strategy": strategy,
                        "action": "BUY" if current else "SELL",
                        "position": current,
                    }
                )
                previous = current

    return pd.DataFrame(rows)


def build_monthly_returns(strategy_data: pd.DataFrame) -> pd.DataFrame:
    """Build monthly compounded returns for every strategy."""
    monthly = pd.DataFrame(index=strategy_data.resample("ME").last().index)

    for column in strategy_data.columns:
        if column.endswith(" Daily Return"):
            strategy = column.replace(" Daily Return", "")
            monthly[strategy] = strategy_data[column].resample("ME").apply(lambda values: (1 + values).prod() - 1)

    return monthly
