# Application Materials

## English Project Summary

US Stock Quant Toolkit is a Python-based quantitative research and backtesting project for US equities and ETFs. It downloads the latest available historical market data with yfinance, maintains a local CSV cache with incremental updates, and supports single-asset strategy backtesting, multi-stock comparison, sector ETF comparison, and multi-asset allocation research.

The project includes modular Python code, CSV outputs, professional charts, Markdown reports, PDF reports, and a local Streamlit web app. The single-asset research mode evaluates rule-based strategies such as Buy and Hold, moving average strategies, RSI mean reversion, and momentum. The backtesting logic uses shifted positions to reduce look-ahead bias and includes transaction cost assumptions.

This project is intended for educational and research purposes only. It uses historical market data only. It does not use real-time market data, does not connect to any brokerage account, and does not execute trades.

## Project Highlights

- Historical market data is downloaded with yfinance and updated through a local CSV cache.
- The default single-asset research mode tests SPY with multiple rule-based strategies.
- The strategy backtest uses one-day shifted positions to reduce look-ahead bias.
- Transaction costs are included when portfolio positions change.
- Train/test evaluation separates in-sample and out-of-sample performance review.
- Multi-stock, sector ETF, and multi-asset ETF comparison modes extend the research scope.
- Outputs include CSV files, PNG charts, Markdown reports, PDF reports, and a local Streamlit web app.
- The project is designed for learning, research practice, GitHub presentation, and graduate school application materials.

## Resume Bullet Points

- Built a Python quantitative research toolkit for US equities and ETFs using pandas, yfinance, matplotlib, ReportLab, and Streamlit.
- Implemented historical data download, local CSV caching, and automatic incremental updates for yfinance market data.
- Developed a modular backtesting framework with Buy and Hold, moving average, RSI mean reversion, and momentum strategies.
- Reduced look-ahead bias by applying one-day shifted strategy positions and included transaction cost assumptions in strategy returns.
- Added train/test evaluation, risk metrics, drawdown analysis, rolling risk charts, Markdown reports, and automatically generated PDF reports.
- Extended the project to support multi-stock comparison, sector ETF analysis, and multi-asset allocation research with equal-weight portfolio analysis.
- Built a local Streamlit web app for selecting research modes, entering tickers, running analysis, viewing charts, and downloading reports.

## One-Minute English Presentation Script

Hello, my project is called US Stock Quant Toolkit. It is a Python-based quantitative research and backtesting tool for US stocks and ETFs.

The project uses yfinance to download the latest available historical market data and stores the data in a local CSV cache. Each time the program runs, it checks whether new historical data is available and updates only the missing part.

The core research mode tests several rule-based strategies on a single asset, including Buy and Hold, moving average strategies, RSI mean reversion, and momentum. To make the backtest more realistic, I use shifted trading signals to reduce look-ahead bias and include transaction costs when positions change.

I also added research modes for comparing multiple stocks, sector ETFs, and multi-asset ETFs such as stocks, bonds, and gold. The project produces CSV files, charts, Markdown reports, PDF reports, and a local Streamlit web app.

This project is designed for learning and research. It does not use real-time data, does not connect to a brokerage account, and does not execute trades.

## GitHub Repository Description

A Python quantitative research toolkit for US stocks and ETFs, featuring yfinance historical data updates, strategy backtesting, multi-asset comparison, professional charts, PDF reports, and a local Streamlit web app.

## Short README Tagline

A Python toolkit for educational US equity and ETF quantitative research, historical backtesting, multi-asset comparison, and Streamlit-based visualization.
