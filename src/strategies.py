import pandas as pd


def build_strategy_signals(indicators: pd.DataFrame) -> pd.DataFrame:
    """Build unshifted strategy position signals.

    The backtester shifts these signals by one trading day before applying returns,
    so today's return can only use yesterday's known position.
    """
    signals = pd.DataFrame(index=indicators.index)
    signals["Buy and Hold"] = 1
    signals["20/60 Moving Average"] = (indicators["ma_20"] > indicators["ma_60"]).astype(int)
    signals["50/200 Moving Average"] = (indicators["ma_50"] > indicators["ma_200"]).astype(int)

    rsi_signal = pd.Series(index=indicators.index, dtype=float)
    rsi_signal[indicators["rsi_14"] < 30] = 1
    rsi_signal[indicators["rsi_14"] > 70] = 0
    signals["RSI Mean Reversion"] = rsi_signal.ffill().fillna(0).astype(int)

    signals["6-Month Momentum"] = (indicators["momentum_126"] > 0).astype(int)
    return signals
