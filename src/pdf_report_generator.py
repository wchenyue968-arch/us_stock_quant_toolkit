from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


DISCLAIMER = "This project is for educational and research purposes only and does not constitute investment advice."


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def register_font(language: str) -> str:
    if language == "cn":
        font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
        if font_path.exists():
            font_name = "MicrosoftYaHei"
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            return font_name
    return "Helvetica"


def build_styles(language: str) -> dict[str, ParagraphStyle]:
    font_name = register_font(language)
    sample = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "CustomTitle",
            parent=sample["Title"],
            fontName=font_name,
            fontSize=20,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "heading": ParagraphStyle(
            "CustomHeading",
            parent=sample["Heading2"],
            fontName=font_name,
            fontSize=14,
            leading=20,
            textColor=colors.HexColor("#1F4E79"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "CustomBody",
            parent=sample["BodyText"],
            fontName=font_name,
            fontSize=9.8,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "caption": ParagraphStyle(
            "CustomCaption",
            parent=sample["BodyText"],
            fontName=font_name,
            fontSize=8.8,
            leading=13,
            textColor=colors.HexColor("#444444"),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=10,
        ),
    }


def para(text: str, style: ParagraphStyle) -> Paragraph:
    safe = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(safe, style)


def add_section(story: list, title: str, body: list[str], styles: dict[str, ParagraphStyle]) -> None:
    story.append(para(title, styles["heading"]))
    for item in body:
        story.append(para(item, styles["body"]))


def add_metrics_table(story: list, metrics: pd.DataFrame, styles: dict[str, ParagraphStyle], max_rows: int = 8) -> None:
    columns = ["Strategy", "Cumulative Return", "Annualized Return", "Sharpe Ratio", "Maximum Drawdown", "Calmar Ratio"]
    available = [column for column in columns if column in metrics.columns]
    table_data = [[para(column, styles["body"]) for column in available]]

    for _, row in metrics.head(max_rows).iterrows():
        current = []
        for column in available:
            value = row[column]
            if column in {"Cumulative Return", "Annualized Return", "Maximum Drawdown", "Calmar Ratio"}:
                text = format_percent(float(value)) if column != "Sharpe Ratio" else f"{float(value):.2f}"
            elif column == "Sharpe Ratio":
                text = f"{float(value):.2f}"
            else:
                text = str(value)
            current.append(para(text, styles["body"]))
        table_data.append(current)

    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))


def add_image_or_warning(
    story: list,
    image_path: Path,
    caption: str,
    explanation: str,
    styles: dict[str, ParagraphStyle],
) -> None:
    if image_path.exists():
        story.append(Image(str(image_path), width=16 * cm, height=8.5 * cm, kind="proportional"))
        story.append(para(caption, styles["caption"]))
    else:
        story.append(para(f"Missing image: {image_path}", styles["body"]))
    story.append(para(explanation, styles["body"]))
    story.append(Spacer(1, 8))


def read_metrics(project_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    full_path = project_root / "outputs" / "v7_full_strategy_metrics.csv"
    train_test_path = project_root / "outputs" / "v7_train_test_metrics.csv"
    missing_files = [str(path) for path in [full_path, train_test_path] if not path.exists()]

    if missing_files:
        missing_text = "\n".join(missing_files)
        raise FileNotFoundError(f"Missing required CSV file(s) for PDF generation:\n{missing_text}")

    full = pd.read_csv(full_path)
    train_test = pd.read_csv(train_test_path)
    return full, train_test


def read_data_range(project_root: Path, ticker: str = "SPY") -> dict[str, str]:
    raw_path = project_root / "data" / f"{ticker}_raw_price_data.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Missing required raw data file for PDF generation:\n{raw_path}")

    raw_data = pd.read_csv(raw_path, parse_dates=["date"])
    data_start = str(raw_data["date"].min().date())
    data_end = str(raw_data["date"].max().date())
    return {
        "data_start": data_start,
        "data_end": data_end,
        "train_start": "2018-01-01",
        "train_end": "2021-12-31",
        "test_start": "2022-01-01",
        "test_end": data_end,
    }


def get_findings(full_metrics: pd.DataFrame, train_test_metrics: pd.DataFrame) -> dict[str, str]:
    best_return = full_metrics.sort_values("Cumulative Return", ascending=False).iloc[0]
    best_drawdown = full_metrics.sort_values("Maximum Drawdown", ascending=False).iloc[0]
    best_sharpe = full_metrics.sort_values("Sharpe Ratio", ascending=False).iloc[0]
    test = train_test_metrics[train_test_metrics["Period"] == "Test"]
    best_test = test.sort_values("Sharpe Ratio", ascending=False).iloc[0]
    return {
        "best_return": f"{best_return['Strategy']} ({format_percent(float(best_return['Cumulative Return']))})",
        "best_drawdown": f"{best_drawdown['Strategy']} ({format_percent(float(best_drawdown['Maximum Drawdown']))})",
        "best_sharpe": f"{best_sharpe['Strategy']} ({float(best_sharpe['Sharpe Ratio']):.2f})",
        "best_test": f"{best_test['Strategy']} ({float(best_test['Sharpe Ratio']):.2f})",
    }


def build_formal_story(project_root: Path, language: str) -> list:
    styles = build_styles(language)
    full_metrics, train_test_metrics = read_metrics(project_root)
    data_range = read_data_range(project_root)
    findings = get_findings(full_metrics, train_test_metrics)
    story = []

    if language == "cn":
        story.append(para("US Stock Quant Toolkit：美股量化策略回测研究项目", styles["title"]))
        add_section(story, "项目摘要", ["这是一个用于学习和研究的 Python 美股量化回测项目，可以下载真实市场数据，测试多种策略，并比较收益和风险。"], styles)
        add_section(story, "数据来源", ["使用 yfinance 下载 SPY 或其他美股 ETF/股票的历史价格数据。"], styles)
        add_section(
            story,
            "数据时间范围",
            [
                f"Full period：{data_range['data_start']} 到 {data_range['data_end']}。",
                f"Train period：{data_range['train_start']} 到 {data_range['train_end']}。",
                f"Test period：{data_range['test_start']} 到 {data_range['test_end']}。",
            ],
            styles,
        )
        add_section(story, "策略设计", ["Buy and Hold、20/60 Moving Average、50/200 Moving Average、RSI Mean Reversion、6-Month Momentum。"], styles)
        add_section(story, "回测方法", ["使用日收益率进行回测。所有交易信号使用 shift(1)，避免未来函数。交易成本 transaction_cost = 0.001。样本分为训练期和测试期，并重点分析测试期结果。"], styles)
        add_section(story, "指标解释", ["指标包括 Cumulative Return、Annualized Return、Annualized Volatility、Sharpe Ratio、Maximum Drawdown、Calmar Ratio、Win Rate、Number of Trades 和 Turnover。"], styles)
        story.append(para("回测结果：全样本", styles["heading"]))
        add_metrics_table(story, full_metrics, styles)
        story.append(para("回测结果：训练期和测试期", styles["heading"]))
        add_metrics_table(story, train_test_metrics, styles, max_rows=15)
        add_section(story, "主要结论", [f"累计收益较高：{findings['best_return']}。", f"回撤较低：{findings['best_drawdown']}。", f"Sharpe Ratio 较高：{findings['best_sharpe']}。", f"测试期 Sharpe Ratio 较高：{findings['best_test']}。", "交易成本会降低高换手策略的表现。"], styles)
        add_section(story, "项目局限性", ["只使用历史数据，没有预测未来收益。没有考虑滑点、税费和流动性限制。单一资产测试不能代表所有市场环境。回测结果不等于未来表现。"], styles)
        add_section(story, "后续改进方向", ["可以加入多资产组合、风险平价组合、参数优化、Walk-forward validation、Monte Carlo simulation、宏观因子或机器学习模型。"], styles)
    else:
        story.append(para("US Stock Quant Toolkit: Quantitative Strategy Backtesting Project", styles["title"]))
        add_section(story, "Executive Summary", ["This is a Python-based quantitative research project that downloads real market data, tests multiple rule-based strategies, and compares return and risk profiles."], styles)
        add_section(story, "Data Source", ["The project uses yfinance to download historical price data for SPY or other US-listed stocks and ETFs."], styles)
        add_section(
            story,
            "Data Range",
            [
                f"Full period: {data_range['data_start']} to {data_range['data_end']}.",
                f"Train period: {data_range['train_start']} to {data_range['train_end']}.",
                f"Test period: {data_range['test_start']} to {data_range['test_end']}.",
            ],
            styles,
        )
        add_section(story, "Strategy Design", ["The tested strategies are Buy and Hold, 20/60 Moving Average, 50/200 Moving Average, RSI Mean Reversion, and 6-Month Momentum."], styles)
        add_section(story, "Backtesting Methodology", ["The backtest uses daily returns. All signals are shifted by one day using shift(1) to avoid look-ahead bias. The transaction cost assumption is transaction_cost = 0.001. The sample is split into training and testing periods."], styles)
        add_section(story, "Performance Metrics", ["The report includes cumulative return, annualized return, annualized volatility, Sharpe Ratio, maximum drawdown, Calmar Ratio, win rate, number of trades, and turnover."], styles)
        story.append(para("Empirical Results: Full Sample", styles["heading"]))
        add_metrics_table(story, full_metrics, styles)
        story.append(para("Empirical Results: Train/Test", styles["heading"]))
        add_metrics_table(story, train_test_metrics, styles, max_rows=15)
        add_section(story, "Key Findings", [f"Highest cumulative return: {findings['best_return']}.", f"Lowest drawdown: {findings['best_drawdown']}.", f"Highest Sharpe Ratio: {findings['best_sharpe']}.", f"Best testing-period Sharpe Ratio: {findings['best_test']}.", "Transaction costs reduce the performance of high-turnover strategies."], styles)
        add_section(story, "Limitations", ["The project only uses historical data and does not forecast future returns. It does not include slippage, taxes, or liquidity constraints. A single-asset test cannot represent every market environment."], styles)
        add_section(story, "Future Improvements", ["Potential extensions include multi-asset portfolios, risk parity, parameter optimization, walk-forward validation, Monte Carlo simulation, macro factors, and machine learning models."], styles)

    story.append(PageBreak())
    story.append(para("Charts", styles["heading"]))
    image_info = [
        ("v7_strategy_comparison_full.png", "Full-sample cumulative return comparison."),
        ("v7_strategy_comparison_test.png", "Testing-period cumulative return comparison."),
        ("v7_drawdown_comparison.png", "Drawdown comparison across strategies."),
        ("v7_rolling_risk.png", "Rolling volatility and rolling Sharpe Ratio."),
    ]
    for filename, explanation in image_info:
        add_image_or_warning(story, project_root / "outputs" / filename, filename, explanation, styles)
    add_section(story, "Disclaimer", [DISCLAIMER], styles)
    return story


def build_explained_story(project_root: Path, language: str) -> list:
    styles = build_styles(language)
    story = []
    if language == "cn":
        story.append(para("v7 图表解释版报告", styles["title"]))
        explanations = [
            ("v7_strategy_comparison_full.png", "全样本累计收益图", "这张图是什么：它展示所有策略在完整回测区间的累计收益。横轴是什么：日期。纵轴是什么：累计收益率。每条线代表什么：每条线代表一个策略。怎么看这张图：曲线越高，代表历史累计收益越高。说明了什么：可以比较不同策略长期收益差异。局限：收益高不代表风险低，需要结合最大回撤图一起看。"),
            ("v7_strategy_comparison_test.png", "测试期累计收益图", "这张图是什么：它展示测试期内各策略的累计收益。横轴是什么：日期。纵轴是什么：测试期累计收益率。每条线代表什么：每条线代表一个策略。怎么看这张图：测试期表现更接近样本外观察。说明了什么：它可以帮助判断策略在训练期之外是否仍然稳定。局限：测试期仍然是历史数据，不能保证未来表现。"),
            ("v7_drawdown_comparison.png", "回撤图", "这张图是什么：它展示各策略从历史高点下跌的幅度。横轴是什么：日期。纵轴是什么：回撤百分比。每条线代表什么：每条线代表一个策略。怎么看这张图：回撤越深，说明策略风险越大。说明了什么：最大回撤是衡量策略风险的重要指标。局限：回撤只描述历史下跌，不预测未来风险。"),
            ("v7_rolling_risk.png", "滚动风险图", "这张图是什么：它展示滚动波动率和滚动 Sharpe Ratio。横轴是什么：日期。纵轴是什么：上半部分是滚动波动率，下半部分是滚动 Sharpe Ratio。每条线代表什么：每条线代表一个策略。怎么看这张图：如果某段时间波动率突然升高，说明市场风险变大；如果滚动 Sharpe Ratio 长期为正，说明策略风险调整后表现较好。说明了什么：滚动指标可以观察策略表现是否稳定。局限：滚动窗口选择会影响观察结果。"),
        ]
    else:
        story.append(para("V7 Chart Explanation Report", styles["title"]))
        explanations = [
            ("v7_strategy_comparison_full.png", "Full-sample cumulative return chart", "The x-axis is date and the y-axis is cumulative return. Each line represents one strategy. A higher line means a higher historical cumulative return, but higher return does not mean lower risk."),
            ("v7_strategy_comparison_test.png", "Testing-period cumulative return chart", "This chart focuses on out-of-sample performance. It helps evaluate whether a strategy remains stable outside the training period."),
            ("v7_drawdown_comparison.png", "Drawdown comparison chart", "Drawdown measures the decline from a previous high. Deeper drawdowns imply higher historical downside risk."),
            ("v7_rolling_risk.png", "Rolling risk chart", "Rolling metrics help evaluate stability. Rising rolling volatility indicates higher market risk, while a positive rolling Sharpe Ratio suggests better risk-adjusted performance."),
        ]
    for filename, title, explanation in explanations:
        story.append(para(title, styles["heading"]))
        add_image_or_warning(story, project_root / "outputs" / filename, filename, explanation, styles)
        if language == "cn":
            story.append(para("局限：图表只显示历史结果，不能预测未来。", styles["body"]))
        else:
            story.append(para("Limitation: the chart only describes historical results and does not predict the future.", styles["body"]))
    add_section(story, "Disclaimer", [DISCLAIMER], styles)
    return story


def build_pdf(story: list, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
    )
    document.build(story)
    return output_path


def generate_all_v7_pdfs(project_root: Path) -> dict[str, Path]:
    outputs = project_root / "outputs"
    paths = {
        "cn_pdf": outputs / "report_v7_cn.pdf",
        "en_pdf": outputs / "report_v7_en.pdf",
        "explained_cn_pdf": outputs / "report_v7_explained_cn.pdf",
        "explained_en_pdf": outputs / "report_v7_explained_en.pdf",
    }
    build_pdf(build_formal_story(project_root, "cn"), paths["cn_pdf"])
    build_pdf(build_formal_story(project_root, "en"), paths["en_pdf"])
    build_pdf(build_explained_story(project_root, "cn"), paths["explained_cn_pdf"])
    build_pdf(build_explained_story(project_root, "en"), paths["explained_en_pdf"])
    return paths
