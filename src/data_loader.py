from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_data_path(ticker: str) -> Path:
    """Return the local cache path for one ticker."""
    return PROJECT_ROOT / "data" / "raw" / f"{ticker.upper()}.csv"


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean downloaded or cached price data into date-indexed close prices."""
    if df.empty:
        return pd.DataFrame(columns=["close"])

    data = df.copy()

    # yfinance may return a MultiIndex if multiple tickers are requested.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Cached CSV files contain a date column; downloaded data uses the index.
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"])
        data = data.set_index("date")
    else:
        data.index = pd.to_datetime(data.index)

    # Prefer the adjusted close produced by auto_adjust=True, which is named Close.
    if "close" not in data.columns:
        if "Close" in data.columns:
            data = data[["Close"]].rename(columns={"Close": "close"})
        elif "Adj Close" in data.columns:
            data = data[["Adj Close"]].rename(columns={"Adj Close": "close"})
        else:
            raise ValueError("Price data must contain a Close, Adj Close, or close column.")
    else:
        data = data[["close"]]

    data["close"] = pd.to_numeric(data["close"], errors="coerce")
    data = data.dropna(subset=["close"])
    data = data[~data.index.duplicated(keep="last")]
    data = data.sort_index()
    return data


def load_local_data(ticker: str) -> pd.DataFrame | None:
    """Load cached local data if it exists."""
    data_path = get_data_path(ticker)
    if not data_path.exists():
        return None

    cached = pd.read_csv(data_path)
    return clean_price_data(cached)


def download_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Download historical data from yfinance for the requested date range."""
    raw_data = yf.download(
        tickers=ticker.upper(),
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if raw_data.empty:
        return pd.DataFrame(columns=["close"])

    return clean_price_data(raw_data)


def save_local_data(ticker: str, data: pd.DataFrame) -> Path:
    """Save cleaned price data back to the local cache."""
    data_path = get_data_path(ticker)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(data_path, index_label="date")
    return data_path


def update_data(
    ticker: str,
    start_date: str,
    end_date: str | None = None,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Load cached data and incrementally update it with latest available history."""
    ticker = ticker.upper()
    end_date = end_date or date.today().isoformat()
    local_data = load_local_data(ticker)

    if force_refresh or local_data is None:
        try:
            full_data = download_data(ticker, start_date, end_date)
        except Exception as error:
            if local_data is not None and not local_data.empty:
                print(f"Warning: yfinance download failed. Using local cache for {ticker}. Error: {error}")
                return local_data
            raise RuntimeError(f"Cannot run without data for {ticker}. No local cache and yfinance failed: {error}") from error

        if full_data.empty:
            if local_data is not None and not local_data.empty:
                print("No new trading data available.")
                return local_data
            raise RuntimeError(f"Cannot run without data for {ticker}. yfinance returned no data and no cache exists.")

        save_local_data(ticker, full_data)
        return full_data

    last_local_date = local_data.index.max().date()
    requested_end_date = datetime.fromisoformat(end_date).date()
    next_download_date = last_local_date + timedelta(days=1)

    if next_download_date > requested_end_date:
        print("No new trading data available.")
        return local_data

    try:
        new_data = download_data(ticker, next_download_date.isoformat(), end_date)
    except Exception as error:
        print(f"Warning: yfinance incremental update failed. Using local cache for {ticker}. Error: {error}")
        return local_data

    if new_data.empty:
        print("No new trading data available.")
        return local_data

    updated_data = pd.concat([local_data, new_data])
    updated_data = clean_price_data(updated_data)

    if updated_data.index.max().date() <= last_local_date:
        print("No new trading data available.")
        return local_data

    save_local_data(ticker, updated_data)
    return updated_data
