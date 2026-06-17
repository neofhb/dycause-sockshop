from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "experiment" / "figures" / "paper_report"

COLORS = ["#2f5d8c", "#b85c38", "#4b7f52", "#7c5a9e"]


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.sans-serif": [
                "Microsoft YaHei",
                "SimHei",
                "Noto Sans CJK SC",
                "Arial Unicode MS",
                "DejaVu Sans",
            ],
            "axes.unicode_minus": False,
            "figure.dpi": 150,
            "savefig.dpi": 180,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.7,
        }
    )


def pct_label(ax, bars) -> None:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height * 100:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )


def save(fig, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / name, bbox_inches="tight")
    plt.close(fig)


def fig1_current_scope_prk() -> None:
    df = pd.read_csv(ROOT / "data" / "sockshop_mesh_extended" / "current_report_overall.csv")
    labels = {
        "all_main_param_quality_valid": "全部有效 run",
        "repeated_ge5": "重复数 >= 5",
        "selected_current_positive": "主要正例组",
    }
    df["scope"] = df["scope"].map(labels)
    metrics = ["top1", "top2", "top5"]

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    x = range(len(df))
    width = 0.23
    for idx, metric in enumerate(metrics):
        bars = ax.bar(
            [i + (idx - 1) * width for i in x],
            df[metric],
            width=width,
            label=metric.upper().replace("TOP", "Top-"),
            color=COLORS[idx],
        )
        pct_label(ax, bars)

    ax.set_title("当前主参数下不同统计范围的 PR@K")
    ax.set_ylabel("命中率")
    ax.set_ylim(0, 0.62)
    ax.set_xticks(list(x), df["scope"], rotation=0)
    ax.legend(ncol=3, frameon=False, loc="upper left")
    save(fig, "fig1_current_scope_prk.png")


def fig2_main_experiment_effect() -> None:
    df = pd.read_csv(ROOT / "data" / "sockshop_mesh_extended" / "current_report_algorithm_effect.csv")
    selected = ["mesh_e1", "mesh_e3", "el_e2", "el_e5", "el_e13", "el_e4"]
    df = df[df["experiment"].isin(selected)].copy()
    df["label"] = df["experiment"] + "\n" + df["root"] + " / " + df["fault_type"]
    metrics = [("pr2_rate", "Top-2"), ("pr5_rate", "Top-5"), ("acc_mean", "Acc")]

    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    x = range(len(df))
    width = 0.24
    for idx, (col, label) in enumerate(metrics):
        bars = ax.bar(
            [i + (idx - 1) * width for i in x],
            df[col],
            width=width,
            label=label,
            color=COLORS[idx],
        )
        pct_label(ax, bars)

    ax.set_title("主要实验组的根因定位效果")
    ax.set_ylabel("指标值")
    ax.set_ylim(0, 0.72)
    ax.set_xticks(list(x), df["label"], fontsize=8)
    ax.legend(ncol=3, frameon=False, loc="upper right")
    save(fig, "fig2_main_experiment_effect.png")


def fig3_baseline_comparison() -> None:
    df = pd.read_csv(ROOT / "data" / "baseline_comparison" / "baseline_comparison_summary.csv")
    df = df[df["dataset_group"] == "sockshop_mesh_extended"].copy()
    order = ["dycause", "pearson_entry_abs", "anomaly_z_mean_shift", "random_expected"]
    label_map = {
        "dycause": "DyCause",
        "pearson_entry_abs": "Pearson",
        "anomaly_z_mean_shift": "z-shift",
        "random_expected": "Random",
    }
    df["method"] = pd.Categorical(df["method"], categories=order, ordered=True)
    df = df.sort_values("method")
    df["label"] = df["method"].map(label_map)

    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    x = range(len(df))
    width = 0.26
    for idx, (col, label) in enumerate([("top2_hit", "Top-2"), ("top5_hit", "Top-5"), ("acc", "Acc")]):
        bars = ax.bar(
            [i + (idx - 1) * width for i in x],
            df[col],
            width=width,
            label=label,
            color=COLORS[idx],
        )
        pct_label(ax, bars)

    ax.set_title("SockShop Extended 上 DyCause 与简单基线对比")
    ax.set_ylabel("指标值")
    ax.set_ylim(0, 1.02)
    ax.set_xticks(list(x), df["label"])
    ax.legend(ncol=3, frameon=False, loc="upper left")
    save(fig, "fig3_baseline_comparison.png")


def fig4_scoring_ablation() -> None:
    keep = ["original_dycause", "pearson_only", "path_only", "normalized_path_plus_pearson"]
    label_map = {
        "original_dycause": "DyCause",
        "pearson_only": "Pearson",
        "path_only": "Path only",
        "normalized_path_plus_pearson": "Norm path+Pearson",
    }
    frames = []
    for dataset, path in [
        ("pymicro", ROOT / "debug_results_scoring_pymicro" / "summary.csv"),
        ("SockShop Extended", ROOT / "debug_results_scoring_extended" / "summary.csv"),
    ]:
        part = pd.read_csv(path)
        part = part[part["method"].isin(keep)].copy()
        part["dataset"] = dataset
        part["method"] = pd.Categorical(part["method"], categories=keep, ordered=True)
        frames.append(part)
    df = pd.concat(frames).sort_values(["dataset", "method"])

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8), sharey=True)
    for ax, dataset in zip(axes, ["pymicro", "SockShop Extended"]):
        part = df[df["dataset"] == dataset]
        x = range(len(part))
        width = 0.24
        for idx, (col, label) in enumerate([("top2", "Top-2"), ("top5", "Top-5"), ("mrr", "MRR")]):
            bars = ax.bar(
                [i + (idx - 1) * width for i in x],
                part[col],
                width=width,
                label=label,
                color=COLORS[idx],
            )
            pct_label(ax, bars)
        ax.set_title(dataset)
        ax.set_xticks(list(x), [label_map[m] for m in part["method"]], rotation=18, ha="right")
        ax.set_ylim(0, 1.06)
    axes[0].set_ylabel("指标值")
    axes[0].legend(ncol=3, frameon=False, loc="upper left")
    fig.suptitle("DyCause 路径机制与融合方法消融", y=1.02)
    save(fig, "fig4_scoring_ablation.png")


def main() -> None:
    setup_style()
    fig1_current_scope_prk()
    fig2_main_experiment_effect()
    fig3_baseline_comparison()
    fig4_scoring_ablation()
    print(f"Saved figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
