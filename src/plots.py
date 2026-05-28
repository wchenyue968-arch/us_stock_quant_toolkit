from pathlib import Path
import os

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


TRADING_DAYS_PER_YEAR = 252


def plot_cumulative(
    strategy_data: pd.DataFrame,
    output_path: Path,
    title: str,
    start_date: pd.Timestamp | None = None,
) -> Path:
    """Plot cumulative returns for full or test period."""
    data = strategy_data if start_date is None else strategy_data[strategy_data.index >= start_date]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(15, 8))

    for column in data.columns:
        if column.endswith(" Cumulative Return"):
            strategy = column.replace(" Cumulative Return", "")
            series = data[column]
            if start_date is not None and not series.empty:
                series = (1 + data[column]) / (1 + data[column].iloc[0]) - 1
            ax.plot(data.index, series * 100, label=strategy, linewidth=2)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_drawdown(strategy_data: pd.DataFrame, output_path: Path) -> Path:
    """Plot drawdown comparison."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(15, 8))

    for column in strategy_data.columns:
        if column.endswith(" Drawdown"):
            ax.plot(strategy_data.index, strategy_data[column] * 100, label=column.replace(" Drawdown", ""), linewidth=1.8)

    ax.set_title("V7 Strategy Drawdown Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_rolling_risk(strategy_data: pd.DataFrame, output_path: Path) -> Path:
    """Plot rolling volatility and rolling Sharpe Ratio."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

    for column in strategy_data.columns:
        if column.endswith(" Daily Return"):
            strategy = column.replace(" Daily Return", "")
            rolling_vol = strategy_data[column].rolling(126).std() * (TRADING_DAYS_PER_YEAR**0.5)
            rolling_return = strategy_data[column].rolling(126).mean() * TRADING_DAYS_PER_YEAR
            rolling_sharpe = rolling_return / rolling_vol
            axes[0].plot(strategy_data.index, rolling_vol * 100, label=strategy, linewidth=1.5)
            axes[1].plot(strategy_data.index, rolling_sharpe, label=strategy, linewidth=1.5)

    axes[0].set_title("Rolling 126-Day Annualized Volatility")
    axes[0].set_ylabel("Volatility (%)")
    axes[1].set_title("Rolling 126-Day Sharpe Ratio")
    axes[1].set_ylabel("Sharpe Ratio")
    axes[1].set_xlabel("Date")

    for ax in axes:
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_multi_cumulative_returns(cumulative_returns: pd.DataFrame, output_path: Path, title: str) -> Path:
    """Plot cumulative returns for several assets."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(15, 8))

    for column in cumulative_returns.columns:
        ax.plot(cumulative_returns.index, cumulative_returns[column] * 100, label=column, linewidth=2)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_multi_drawdown(drawdowns: pd.DataFrame, output_path: Path, title: str) -> Path:
    """Plot drawdowns for several assets."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(15, 8))

    for column in drawdowns.columns:
        ax.plot(drawdowns.index, drawdowns[column] * 100, label=column, linewidth=1.8)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_correlation_heatmap(daily_returns: pd.DataFrame, output_path: Path, title: str) -> Path:
    """Plot a return-correlation heatmap."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    correlation = daily_returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    image = ax.imshow(correlation, cmap="RdYlBu", vmin=-1, vmax=1)
    ax.set_title(title)
    ax.set_xticks(range(len(correlation.columns)))
    ax.set_yticks(range(len(correlation.index)))
    ax.set_xticklabels(correlation.columns, rotation=45, ha="right")
    ax.set_yticklabels(correlation.index)

    for row in range(len(correlation.index)):
        for col in range(len(correlation.columns)):
            ax.text(col, row, f"{correlation.iloc[row, col]:.2f}", ha="center", va="center", fontsize=8)

    fig.colorbar(image, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_metric_ranking(
    metrics: pd.DataFrame,
    metric_column: str,
    output_path: Path,
    title: str,
    higher_is_better: bool = True,
) -> Path:
    """Plot a ranking chart for one metric."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ranking = metrics.sort_values(metric_column, ascending=not higher_is_better)
    percent_metrics = {
        "Cumulative Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
    }
    scale = 100 if metric_column in percent_metrics else 1
    ylabel = f"{metric_column} (%)" if metric_column in percent_metrics else metric_column

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(ranking["Ticker"], ranking[metric_column] * scale)
    ax.set_title(title)
    ax.set_xlabel("Ticker")
    ax.set_ylabel(ylabel)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path
