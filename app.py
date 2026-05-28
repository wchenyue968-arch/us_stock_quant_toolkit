from __future__ import annotations

import contextlib
import io
import sys
import traceback
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from asset_universe import (  # noqa: E402
    MULTI_ASSET_TICKERS,
    MULTI_STOCK_TICKERS,
    SECTOR_ETF_TICKERS,
)
from data_loader import get_data_path  # noqa: E402
from main import (  # noqa: E402
    run_multi_asset_allocation,
    run_multi_stock_comparison,
    run_sector_etf_comparison,
    run_v7_research_backtest,
)


MODE_SINGLE = "Single Asset Strategy Backtest"
MODE_MULTI_STOCK = "Multi-Stock Comparison"
MODE_SECTOR = "Sector ETF Comparison"
MODE_MULTI_ASSET = "Multi-Asset Allocation Research"

PRESETS = {
    "Broad Market ETFs": ["SPY", "QQQ", "DIA", "IWM", "VTI"],
    "Mega-Cap Tech Stocks": MULTI_STOCK_TICKERS,
    "Sector ETFs": SECTOR_ETF_TICKERS,
    "Multi-Asset ETFs": MULTI_ASSET_TICKERS,
    "Custom": [],
}


def parse_tickers(text: str) -> list[str]:
    """Parse comma-separated ticker input."""
    tickers = []
    for item in text.split(","):
        ticker = item.strip().upper()
        if ticker and ticker not in tickers:
            tickers.append(ticker)
    return tickers


def default_tickers_for_mode(mode: str) -> list[str]:
    """Return the default tickers for a selected research mode."""
    if mode == MODE_MULTI_STOCK:
        return MULTI_STOCK_TICKERS
    if mode == MODE_SECTOR:
        return SECTOR_ETF_TICKERS
    if mode == MODE_MULTI_ASSET:
        return MULTI_ASSET_TICKERS
    return ["SPY"]


def show_csv(path: Path, title: str) -> pd.DataFrame | None:
    """Display a CSV file if it exists."""
    st.subheader(title)
    if not path.exists():
        st.warning(f"文件尚未生成：{path}")
        return None
    data = pd.read_csv(path)
    st.dataframe(data, use_container_width=True)
    return data


def show_image(path: Path, caption: str) -> None:
    """Display an image if it exists."""
    st.subheader(caption)
    if not path.exists():
        st.warning(f"文件尚未生成：{path}")
        return
    st.image(str(path), caption=caption, use_container_width=True)


def download_file(path: Path, label: str) -> None:
    """Create a download button for an existing file."""
    if not path.exists():
        st.warning(f"文件尚未生成：{path}")
        return

    suffix = path.suffix.lower()
    mime = "application/pdf" if suffix == ".pdf" else "text/markdown" if suffix == ".md" else "text/csv"
    st.download_button(
        label=label,
        data=path.read_bytes(),
        file_name=path.name,
        mime=mime,
        use_container_width=True,
    )


def display_data_status(tickers: list[str]) -> None:
    """Show local cache status for selected tickers."""
    st.subheader("数据更新状态")
    rows = []
    for ticker in tickers:
        path = get_data_path(ticker)
        if not path.exists():
            rows.append({"Ticker": ticker, "Cache File": str(path), "Status": "未找到缓存", "Start": "", "End": ""})
            continue
        data = pd.read_csv(path)
        if "date" not in data.columns or data.empty:
            rows.append({"Ticker": ticker, "Cache File": str(path), "Status": "缓存为空或格式异常", "Start": "", "End": ""})
            continue
        dates = pd.to_datetime(data["date"])
        rows.append(
            {
                "Ticker": ticker,
                "Cache File": str(path),
                "Status": "已读取本地缓存",
                "Start": str(dates.min().date()),
                "End": str(dates.max().date()),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True)


def run_selected_mode(
    mode: str,
    tickers: list[str],
    start_date: str,
    end_date: str,
    transaction_cost: float,
    split_date: str,
    force_refresh: bool,
) -> tuple[dict, str]:
    """Run one research mode and capture printed status messages."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        if mode == MODE_SINGLE:
            if not tickers:
                raise ValueError("请输入至少一个 ticker。")
            paths = run_v7_research_backtest(
                ticker=tickers[0],
                start_date=start_date,
                end_date=end_date,
                transaction_cost=transaction_cost,
                train_test_split_date=split_date,
                force_refresh=force_refresh,
            )
        elif mode == MODE_MULTI_STOCK:
            paths = run_multi_stock_comparison(
                tickers=tickers,
                start_date=start_date,
                end_date=end_date,
                force_refresh=force_refresh,
            )
        elif mode == MODE_SECTOR:
            paths = run_sector_etf_comparison(
                tickers=tickers,
                start_date=start_date,
                end_date=end_date,
                force_refresh=force_refresh,
            )
        elif mode == MODE_MULTI_ASSET:
            paths = run_multi_asset_allocation(
                tickers=tickers,
                start_date=start_date,
                end_date=end_date,
                force_refresh=force_refresh,
            )
        else:
            raise ValueError(f"未知研究模式：{mode}")
    return paths, buffer.getvalue()


def display_single_asset_results() -> None:
    """Display single-asset v7 outputs."""
    show_csv(OUTPUTS_DIR / "v7_full_strategy_metrics.csv", "Full Period 策略绩效指标")
    show_csv(OUTPUTS_DIR / "v7_train_test_metrics.csv", "Train/Test 策略绩效指标")

    show_image(OUTPUTS_DIR / "v7_strategy_comparison_full.png", "Full Period 策略累计收益对比")
    show_image(OUTPUTS_DIR / "v7_strategy_comparison_test.png", "Test Period 策略累计收益对比")
    show_image(OUTPUTS_DIR / "v7_drawdown_comparison.png", "策略最大回撤对比")
    show_image(OUTPUTS_DIR / "v7_rolling_risk.png", "滚动风险指标")

    st.subheader("报告下载")
    col1, col2 = st.columns(2)
    with col1:
        download_file(PROJECT_ROOT / "report_v7_cn.md", "下载中文 Markdown 报告")
        download_file(OUTPUTS_DIR / "report_v7_cn.pdf", "下载中文正式 PDF")
        download_file(OUTPUTS_DIR / "report_v7_explained_cn.pdf", "下载中文图表解释 PDF")
    with col2:
        download_file(PROJECT_ROOT / "report_v7_en.md", "Download English Markdown Report")
        download_file(OUTPUTS_DIR / "report_v7_en.pdf", "Download English Formal PDF")
        download_file(OUTPUTS_DIR / "report_v7_explained_en.pdf", "Download English Explained PDF")


def display_multi_stock_results() -> None:
    """Display multi-stock outputs."""
    show_csv(OUTPUTS_DIR / "multi_stock_metrics.csv", "多股票指标表")
    show_image(OUTPUTS_DIR / "multi_stock_cumulative_returns.png", "多股票累计收益对比")
    show_image(OUTPUTS_DIR / "multi_stock_drawdown.png", "多股票回撤对比")
    show_image(OUTPUTS_DIR / "multi_stock_correlation.png", "多股票相关性")
    st.subheader("报告下载")
    download_file(OUTPUTS_DIR / "report_multi_stock_cn.md", "下载中文报告")
    download_file(OUTPUTS_DIR / "report_multi_stock_en.md", "Download English Report")


def display_sector_results() -> None:
    """Display sector ETF outputs."""
    show_csv(OUTPUTS_DIR / "sector_etf_metrics.csv", "行业 ETF 指标表")
    show_image(OUTPUTS_DIR / "sector_etf_cumulative_returns.png", "行业 ETF 累计收益对比")
    show_image(OUTPUTS_DIR / "sector_etf_annual_return_ranking.png", "行业 ETF 年化收益排名")
    show_image(OUTPUTS_DIR / "sector_etf_max_drawdown_ranking.png", "行业 ETF 最大回撤排名")
    show_image(OUTPUTS_DIR / "sector_etf_sharpe_ranking.png", "行业 ETF Sharpe Ratio 排名")
    st.subheader("报告下载")
    download_file(OUTPUTS_DIR / "report_sector_etf_cn.md", "下载中文报告")
    download_file(OUTPUTS_DIR / "report_sector_etf_en.md", "Download English Report")


def display_multi_asset_results() -> None:
    """Display multi-asset allocation outputs."""
    show_csv(OUTPUTS_DIR / "multi_asset_metrics.csv", "多资产指标表")
    show_csv(OUTPUTS_DIR / "equal_weight_portfolio_returns.csv", "等权组合每日收益")
    show_image(OUTPUTS_DIR / "multi_asset_cumulative_returns.png", "多资产累计收益对比")
    show_image(OUTPUTS_DIR / "multi_asset_correlation.png", "多资产相关性")
    st.subheader("报告下载")
    download_file(OUTPUTS_DIR / "report_multi_asset_cn.md", "下载中文报告")
    download_file(OUTPUTS_DIR / "report_multi_asset_en.md", "Download English Report")


def main() -> None:
    st.set_page_config(page_title="US Stock Quant Toolkit", layout="wide")
    st.title("US Stock Quant Toolkit")
    st.write(
        "这是一个用于学习、研究和研究生申请展示的 Python 美股量化研究工具。"
        "项目使用 yfinance 下载最新可用历史数据，支持策略回测、多资产比较、图表和报告生成。"
        "不连接券商，不自动交易，不下单，不构成投资建议。"
    )

    with st.sidebar:
        st.header("参数设置")
        mode = st.selectbox(
            "Research Mode",
            [MODE_SINGLE, MODE_MULTI_STOCK, MODE_SECTOR, MODE_MULTI_ASSET],
        )
        preset = st.selectbox(
            "Preset Portfolio",
            ["Broad Market ETFs", "Mega-Cap Tech Stocks", "Sector ETFs", "Multi-Asset ETFs", "Custom"],
            index=4 if mode == MODE_SINGLE else 1 if mode == MODE_MULTI_STOCK else 2 if mode == MODE_SECTOR else 3,
        )

        preset_tickers = PRESETS[preset] if preset != "Custom" else default_tickers_for_mode(mode)
        default_ticker_text = ", ".join(preset_tickers if mode != MODE_SINGLE else [preset_tickers[0]])
        ticker_text = st.text_area("Ticker 输入框", value=default_ticker_text, height=90)

        start = st.date_input("Start Date", value=date(2018, 1, 1))
        end = st.date_input("End Date", value=date.today())
        transaction_cost = st.number_input("Transaction Cost", value=0.001, min_value=0.0, step=0.001, format="%.4f")
        split = st.date_input("Train/Test Split Date", value=date(2022, 1, 1))
        force_refresh = st.checkbox("Force Refresh Data", value=False)
        run_button = st.button("Run Backtest", type="primary", use_container_width=True)

    tickers = parse_tickers(ticker_text)
    if mode == MODE_SINGLE and len(tickers) > 1:
        st.info(f"单资产模式只使用第一个 ticker：{tickers[0]}")
        tickers = tickers[:1]

    if run_button:
        if not tickers:
            st.error("请输入至少一个有效 ticker。")
            return

        try:
            with st.spinner("正在运行研究流程，请稍等..."):
                paths, run_log = run_selected_mode(
                    mode,
                    tickers,
                    str(start),
                    str(end),
                    transaction_cost,
                    str(split),
                    force_refresh,
                )
            st.success("运行完成。")
            if run_log.strip():
                st.code(run_log.strip())
            failed = paths.get("failed_tickers", []) if isinstance(paths, dict) else []
            if failed:
                st.warning(f"以下 ticker 下载失败或被跳过：{', '.join(failed)}")
            display_data_status(tickers)
        except Exception:
            st.error("主流程运行失败，完整错误信息如下：")
            st.code(traceback.format_exc())
            return

    st.divider()
    if mode == MODE_SINGLE:
        display_single_asset_results()
    elif mode == MODE_MULTI_STOCK:
        display_multi_stock_results()
    elif mode == MODE_SECTOR:
        display_sector_results()
    elif mode == MODE_MULTI_ASSET:
        display_multi_asset_results()

    st.divider()
    st.caption("This project is for educational and research purposes only and does not constitute investment advice.")


if __name__ == "__main__":
    main()
