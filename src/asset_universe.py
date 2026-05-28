"""Default asset lists and research mode names."""

SINGLE_ASSET_STRATEGY_BACKTEST = "single_asset_strategy_backtest"
MULTI_STOCK_COMPARISON = "multi_stock_comparison"
SECTOR_ETF_COMPARISON = "sector_etf_comparison"
MULTI_ASSET_ALLOCATION = "multi_asset_allocation"

SINGLE_ASSET_TICKER = "SPY"

MULTI_STOCK_TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META"]

SECTOR_ETF_TICKERS = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLC", "XLRE"]

MULTI_ASSET_TICKERS = ["SPY", "QQQ", "TLT", "IEF", "GLD"]

RESEARCH_MODES = {
    SINGLE_ASSET_STRATEGY_BACKTEST: {
        "name": "Single Asset Strategy Backtest",
        "description": "Run the v7 single-asset strategy backtest.",
        "tickers": [SINGLE_ASSET_TICKER],
    },
    MULTI_STOCK_COMPARISON: {
        "name": "Multi-Stock Comparison",
        "description": "Compare several large US stocks by historical return and risk.",
        "tickers": MULTI_STOCK_TICKERS,
    },
    SECTOR_ETF_COMPARISON: {
        "name": "Sector ETF Comparison",
        "description": "Compare major US sector ETFs by historical return and risk.",
        "tickers": SECTOR_ETF_TICKERS,
    },
    MULTI_ASSET_ALLOCATION: {
        "name": "Multi-Asset Allocation Research",
        "description": "Compare stocks, bonds, and gold ETFs, plus an equal-weight portfolio.",
        "tickers": MULTI_ASSET_TICKERS,
    },
}
