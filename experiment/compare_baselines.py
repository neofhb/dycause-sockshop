"""
Compare DyCause with simple RCA baselines on existing SockShop datasets.

Baselines:
  - random: expected Top-K hit rate for one true root among candidates
  - pearson: absolute Pearson correlation with the entry service latency
  - anomaly: absolute baseline-to-fault mean shift, normalized by baseline std
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "baseline_comparison"
MAIN_MESH_PARAMS = {"lag": 5, "step": 30, "edge_thres": 0.8}
EXTENDED_MESH_PARAMS = {"lag": 7, "step": 30, "edge_thres": 0.8}
ORIGINAL_DYCAUSE = {
    "e1": {"root_rank": 2, "pr1": 0.0, "pr2": 1.0, "pr5": 1.0, "acc": 0.75},
    "e2": {"root_rank": 2, "pr1": 0.0, "pr2": 1.0, "pr5": 1.0, "acc": 0.75},
}


@dataclass(frozen=True)
class DatasetSpec:
    dataset_group: str
    experiment: str
    run: str
    run_dir: Path
    rawdata_path: Path
    metadata_path: Path
    summary_path: Path | None
    root_id: int
    root_service: str
    entry_service: str
    services: list[str]
    anomaly_start: int
    dycause: dict[str, float | int | str | bool | None]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def parse_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_int(value: str) -> int | None:
    value = str(value).strip()
    if value == "":
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def read_summary_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def params_match(row: dict[str, str], params: dict[str, float | int]) -> bool:
    for key, expected in params.items():
        actual = parse_float(row.get(key, ""))
        if actual is None or not math.isclose(actual, float(expected), rel_tol=0, abs_tol=1e-9):
            return False
    return True


def dycause_from_summary(
    summary_path: Path | None,
    experiment: str,
    run: str,
    params: dict[str, float | int],
) -> dict[str, float | int | str | bool | None]:
    if summary_path is None:
        return {"root_rank": None, "pr1": None, "pr2": None, "pr5": None, "acc": None}
    candidates = []
    for row in read_summary_rows(summary_path):
        if row.get("experiment") == experiment and row.get("run") == run and params_match(row, params):
            candidates.append(row)
    if not candidates:
        return {"root_rank": None, "pr1": None, "pr2": None, "pr5": None, "acc": None}
    row = candidates[0]
    return {
        "root_rank": parse_int(row.get("root_rank", "")),
        "pr1": parse_float(row.get("pr1", "")),
        "pr2": parse_float(row.get("pr2", "")),
        "pr5": parse_float(row.get("pr5", "")),
        "acc": parse_float(row.get("acc", "")),
        "dycause_ok": as_bool(row.get("dycause_ok", "")),
    }


def specs_original() -> Iterable[DatasetSpec]:
    data_root = ROOT / "data" / "sockshop"
    for exp_dir in sorted(data_root.glob("e[0-9]*")):
        meta_path = exp_dir / "metadata.json"
        raw_path = exp_dir / "rawdata.xlsx"
        if not meta_path.exists() or not raw_path.exists():
            continue
        meta = load_json(meta_path)
        root_id = int(meta["root_cause_indices"][0])
        services = list(meta["services"])
        yield DatasetSpec(
            dataset_group="sockshop_4svc",
            experiment=meta["experiment"],
            run="single",
            run_dir=exp_dir,
            rawdata_path=raw_path,
            metadata_path=meta_path,
            summary_path=None,
            root_id=root_id,
            root_service=services[root_id],
            entry_service=services[int(meta.get("frontend_idx", 0))],
            services=services,
            anomaly_start=int(meta["anomaly_start_second"]),
            dycause={**ORIGINAL_DYCAUSE.get(meta["experiment"], {})},
        )


def specs_mesh(data_root: Path, dataset_group: str, params: dict[str, float | int]) -> Iterable[DatasetSpec]:
    summary_path = data_root / "summary.csv"
    for meta_path in sorted(data_root.glob("*/*/metadata.json")):
        run_dir = meta_path.parent
        raw_path = run_dir / "rawdata.xlsx"
        if not raw_path.exists():
            continue
        meta = load_json(meta_path)
        services = list(meta["services"])
        experiment = meta.get("experiment", run_dir.parent.name)
        run = meta.get("run", run_dir.name)
        root_service = meta.get("root_cause") or services[int(meta["root_cause_indices"][0])]
        root_id = int(meta["root_cause_indices"][0])
        yield DatasetSpec(
            dataset_group=dataset_group,
            experiment=experiment,
            run=run,
            run_dir=run_dir,
            rawdata_path=raw_path,
            metadata_path=meta_path,
            summary_path=summary_path,
            root_id=root_id,
            root_service=root_service,
            entry_service=services[int(meta.get("frontend_idx", 0))],
            services=services,
            anomaly_start=int(meta.get("anomaly_start_second", 315)),
            dycause=dycause_from_summary(summary_path, experiment, run, params),
        )


def candidate_service_ids(spec: DatasetSpec) -> dict[str, int]:
    if spec.dataset_group == "sockshop_4svc":
        return {service: idx for idx, service in enumerate(spec.services) if service != spec.entry_service}
    # Mesh DyCause uses front-end=0 and 1-based IDs for the remaining services.
    return {service: idx + 1 for idx, service in enumerate(spec.services) if service != spec.entry_service}


def rank_of(root_id: int, ranked_ids: list[int]) -> int | None:
    try:
        return ranked_ids.index(root_id) + 1
    except ValueError:
        return None


def hit(rank: int | None, k: int, n: int) -> float:
    if rank is None:
        return 0.0
    return float(rank <= min(k, n))


def acc(rank: int | None, total_services: int) -> float:
    if rank is None:
        return 0.0
    return round((total_services - rank + 1) / total_services, 4)


def metric_row(
    spec: DatasetSpec,
    method: str,
    rank: int | None,
    n: int,
    top_services: list[str],
    scores: dict[str, float] | None = None,
    acc_override: float | None = None,
) -> dict[str, object]:
    return {
        "dataset_group": spec.dataset_group,
        "experiment": spec.experiment,
        "run": spec.run,
        "root": spec.root_service,
        "root_id": spec.root_id,
        "method": method,
        "candidate_count": n,
        "root_rank": "" if rank is None else rank,
        "top2_hit": hit(rank, 2, n),
        "top5_hit": hit(rank, 5, n),
        "acc": acc_override if acc_override is not None else acc(rank, len(spec.services)),
        "top_services": " > ".join(top_services),
        "root_score": "" if scores is None or spec.root_service not in scores else scores[spec.root_service],
        "run_dir": str(spec.run_dir),
    }


def compare_one(spec: DatasetSpec) -> list[dict[str, object]]:
    df = pd.read_excel(spec.rawdata_path)
    df = df.replace([np.inf, -np.inf], np.nan)
    candidates = candidate_service_ids(spec)
    n = len(candidates)

    rows: list[dict[str, object]] = []
    random_top = sorted(candidates, key=candidates.get)
    rows.append(
        {
            "dataset_group": spec.dataset_group,
            "experiment": spec.experiment,
            "run": spec.run,
            "root": spec.root_service,
            "root_id": spec.root_id,
            "method": "random_expected",
            "candidate_count": n,
            "root_rank": "expected",
            "top2_hit": min(2, n) / n,
            "top5_hit": min(5, n) / n,
            "acc": (len(spec.services) + 1 - ((n + 1) / 2)) / len(spec.services),
            "top_services": "random permutation",
            "root_score": "",
            "run_dir": str(spec.run_dir),
        }
    )

    dy_rank = spec.dycause.get("root_rank")
    if isinstance(dy_rank, float) and math.isnan(dy_rank):
        dy_rank = None
    rows.append(
        metric_row(
            spec,
            "dycause",
            int(dy_rank) if dy_rank not in ("", None) else None,
            n,
            [],
            None,
            parse_float(str(spec.dycause.get("acc", ""))),
        )
    )

    entry = pd.to_numeric(df[spec.entry_service], errors="coerce")
    pearson_scores = {}
    for service in candidates:
        series = pd.to_numeric(df[service], errors="coerce")
        corr = entry.corr(series)
        pearson_scores[service] = 0.0 if pd.isna(corr) else abs(float(corr))
    pearson_services = sorted(pearson_scores, key=lambda name: (-pearson_scores[name], candidates[name]))
    pearson_ids = [candidates[name] for name in pearson_services]
    rows.append(metric_row(spec, "pearson_entry_abs", rank_of(spec.root_id, pearson_ids), n, pearson_services, pearson_scores))

    start = min(max(spec.anomaly_start, 1), len(df) - 1)
    baseline = df.iloc[:start]
    fault = df.iloc[start:]
    anomaly_scores = {}
    for service in candidates:
        base = pd.to_numeric(baseline[service], errors="coerce")
        fault_values = pd.to_numeric(fault[service], errors="coerce")
        std = float(base.std(ddof=0))
        mean_shift = abs(float(fault_values.mean()) - float(base.mean()))
        if not math.isfinite(std) or std == 0:
            anomaly_scores[service] = 0.0 if mean_shift == 0 else float("inf")
        else:
            anomaly_scores[service] = mean_shift / std
    anomaly_services = sorted(anomaly_scores, key=lambda name: (-anomaly_scores[name], candidates[name]))
    anomaly_ids = [candidates[name] for name in anomaly_services]
    rows.append(metric_row(spec, "anomaly_z_mean_shift", rank_of(spec.root_id, anomaly_ids), n, anomaly_services, anomaly_scores))

    return rows


def aggregate(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    frame = pd.DataFrame(rows)
    grouped = (
        frame.groupby(["dataset_group", "method"], dropna=False)
        .agg(
            runs=("experiment", "count"),
            top2_hit=("top2_hit", "mean"),
            top5_hit=("top5_hit", "mean"),
            acc=("acc", "mean"),
        )
        .reset_index()
    )
    return grouped.to_dict("records")


def write_markdown(rows: list[dict[str, object]], aggregate_rows: list[dict[str, object]], output_path: Path) -> None:
    def fmt(value: object) -> str:
        if isinstance(value, float):
            return f"{value:.4f}"
        return str(value)

    lines = [
        "# DyCause vs Baselines",
        "",
        "随机基线为期望命中率：单一真根因在候选集合中均匀随机排序时，Top-K 命中率为 `min(K, N) / N`。",
        "",
        "## Aggregate",
        "",
        "| Dataset | Method | Runs | Top-2 Hit | Top-5 Hit | Acc |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in aggregate_rows:
        lines.append(
            f"| {row['dataset_group']} | {row['method']} | {row['runs']} | "
            f"{fmt(row['top2_hit'])} | {fmt(row['top5_hit'])} | {fmt(row['acc'])} |"
        )

    lines.extend(
        [
            "",
            "## Per Run",
            "",
            "| Dataset | Experiment | Run | Root | Method | Rank | Top-2 | Top-5 | Acc | Top Services |",
            "|---|---|---|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dataset_group']} | {row['experiment']} | {row['run']} | {row['root']} | "
            f"{row['method']} | {row['root_rank']} | {fmt(row['top2_hit'])} | "
            f"{fmt(row['top5_hit'])} | {fmt(row['acc'])} | {row['top_services']} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    specs: list[DatasetSpec] = []
    specs.extend(specs_original())
    specs.extend(specs_mesh(ROOT / "data" / "sockshop_mesh_business", "sockshop_mesh_business", MAIN_MESH_PARAMS))
    specs.extend(specs_mesh(ROOT / "data" / "sockshop_mesh_extended", "sockshop_mesh_extended", EXTENDED_MESH_PARAMS))

    rows: list[dict[str, object]] = []
    for spec in specs:
        rows.extend(compare_one(spec))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    details_path = output_dir / "baseline_comparison_details.csv"
    aggregate_path = output_dir / "baseline_comparison_summary.csv"
    report_path = output_dir / "baseline_comparison.md"

    pd.DataFrame(rows).to_csv(details_path, index=False)
    aggregate_rows = aggregate(rows)
    pd.DataFrame(aggregate_rows).to_csv(aggregate_path, index=False)
    write_markdown(rows, aggregate_rows, report_path)

    print(f"Wrote {details_path}")
    print(f"Wrote {aggregate_path}")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
