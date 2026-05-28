import pandas as pd


def calculate_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index."""
    change = close.diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)
    average_gain = gains.rolling(window=window).mean()
    average_loss = losses.rolling(window=window).mean()
    relative_strength = average_gain / average_loss
    return 100 - (100 / (1 + relative_strength))


def build_indicators(price_data: pd.DataFrame) -> pd.DataFrame:
    """Build all indicator columns used by v7 strategies."""
    indicators = price_data.copy()
    indicators["daily_return"] = indicators["close"].pct_change().fillna(0)
    indicators["ma_20"] = indicators["close"].rolling(20).mean()
    indicators["ma_50"] = indicators["close"].rolling(50).mean()
    indicators["ma_60"] = indicators["close"].rolling(60).mean()
    indicators["ma_200"] = indicators["close"].rolling(200).mean()
    indicators["rsi_14"] = calculate_rsi(indicators["close"], 14)
    indicators["momentum_126"] = indicators["close"].pct_change(126)
    return indicators
