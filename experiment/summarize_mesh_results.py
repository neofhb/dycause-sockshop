"""
Summarize SockShop Istio mesh experiment runs.

Reads:
  <data-root>/<exp>/runXX/metadata.json
  <data-root>/<exp>/runXX/quality.json
  <data-root>/<exp>/runXX/dycause_*.log

Writes:
  <data-root>/summary.csv
  <data-root>/results.md
"""

import argparse
import csv
import glob
import json
import os
import re
from collections import defaultdict
from statistics import mean, pstdev


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_ROOT = os.path.join(ROOT, "data", "sockshop_mesh_extended")
DEFAULT_MAIN_PARAMS = {"lag": 7, "step": 30, "edge_thres": 0.8}
KNOWN_EXPERIMENT_DEFAULTS = {
    "mesh_e1": {"group": "legacy", "fault_type": "pod-kill", "object_role": "main-reference"},
    "mesh_e2": {"group": "legacy", "fault_type": "pod-kill", "object_role": "negative-case"},
    "mesh_e3": {"group": "legacy", "fault_type": "network-delay", "object_role": "main-reference"},
    "mesh_e4": {"group": "legacy", "fault_type": "network-delay", "object_role": "negative-case"},
    "mesh_e5": {"group": "legacy", "fault_type": "network-delay", "object_role": "negative-case"},
}


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_params(log_path, text):
    params = {"lag": None, "step": None, "edge_thres": None}
    name = os.path.basename(log_path)
    match = re.search(r"lag(?P<lag>\d+)_step(?P<step>\d+)_edge(?P<edge>[0-9.]+)", name)
    if match:
        params["lag"] = int(match.group("lag"))
        params["step"] = int(match.group("step"))
        params["edge_thres"] = float(match.group("edge").rstrip("."))
        return params

    command = next((line for line in text.splitlines() if line.startswith("$ ")), "")
    for key in ("lag", "step", "edge_thres"):
        match = re.search(rf"--{key}\s+([0-9.]+)", command)
        if match:
            params[key] = float(match.group(1)) if "." in match.group(1) else int(match.group(1))
    return params


def parse_pr_table(text):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "PR@1" not in line or "Acc" not in line:
            continue
        for row in lines[index + 1 : index + 5]:
            if not row.strip() or set(row.strip()) <= {"-", " "}:
                continue
            numbers = re.findall(r"[-+]?\d+\.\d+|[-+]?\d+", row)
            if len(numbers) >= 7:
                return {
                    "pr1": float(numbers[0]),
                    "pr2": float(numbers[1]),
                    "pr3": float(numbers[2]),
                    "pr4": float(numbers[3]),
                    "pr5": float(numbers[4]),
                    "pr_avg": float(numbers[5]),
                    "acc": float(numbers[6]),
                }
    return {"pr1": None, "pr2": None, "pr3": None, "pr4": None, "pr5": None, "pr_avg": None, "acc": None}


def parse_ranking(text):
    ranked = []
    for line in text.splitlines():
        match = re.match(r"\s*\|\s*(\d+)\s*\|\s*([-+]?\d+(?:\.\d+)?)\s*\|", line)
        if match:
            ranked.append((int(match.group(1)), float(match.group(2))))
    return ranked


def quality_summary(quality):
    service_quality = (quality or {}).get("service_quality", {})
    if not service_quality:
        return {"quality_valid": False, "min_valid_ratio": 0.0, "missing_points": 0, "zero_points": 0}
    ratios = [float(item.get("valid_ratio", 0.0)) for item in service_quality.values()]
    return {
        "quality_valid": bool((quality or {}).get("valid", False)),
        "min_valid_ratio": min(ratios) if ratios else 0.0,
        "missing_points": sum(int(item.get("missing_points", 0)) for item in service_quality.values()),
        "zero_points": sum(int(item.get("zero_points", 0)) for item in service_quality.values()),
    }


def phase_service_mean(run_dir, phase, service):
    if not service:
        return ""
    path = os.path.join(run_dir, phase, "raw_prometheus.csv")
    if not os.path.exists(path):
        return ""
    with open(path, "r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if service not in (reader.fieldnames or []):
            return ""
        values = []
        for row in reader:
            value = row.get(service, "")
            if value == "":
                continue
            values.append(float(value))
    return mean(values) if values else ""


def canonical_load_profile(meta, run_dir):
    profile = meta.get("load_profile", "")
    if profile:
        return profile
    parts = os.path.normpath(run_dir).split(os.sep)
    if "sockshop_mesh_extended" in parts:
        return "legacy-compressed-v0"
    return ""


def summarize_run(run_dir):
    meta = load_json(os.path.join(run_dir, "metadata.json"), {})
    quality = load_json(os.path.join(run_dir, "quality.json"), {})
    q = quality_summary(quality)
    logs = sorted(glob.glob(os.path.join(run_dir, "dycause_*.log")))
    root = meta.get("root_cause", "")
    baseline_mean = phase_service_mean(run_dir, "baseline", root)
    fault_mean = phase_service_mean(run_dir, "fault", root)
    fault_baseline_ratio = ""
    if baseline_mean not in ("", 0) and fault_mean != "":
        fault_baseline_ratio = fault_mean / baseline_mean
    experiment_name = meta.get("experiment", os.path.basename(os.path.dirname(run_dir)))
    defaults = KNOWN_EXPERIMENT_DEFAULTS.get(experiment_name, {})

    base = {
        "experiment": experiment_name,
        "run": meta.get("run", os.path.basename(run_dir)),
        "dataset": meta.get("dycause_dataset", ""),
        "desc": meta.get("desc", ""),
        "group": meta.get("group", "") or defaults.get("group", ""),
        "fault_type": meta.get("fault_type", "") or defaults.get("fault_type", ""),
        "object_role": meta.get("object_role", "") or defaults.get("object_role", ""),
        "root": root,
        "root_idx": (meta.get("root_cause_indices") or [""])[0],
        "baseline_mean": baseline_mean,
        "fault_mean": fault_mean,
        "fault_baseline_ratio": fault_baseline_ratio,
        "baseline_seconds": meta.get("baseline_seconds", ""),
        "fault_seconds": meta.get("fault_seconds", ""),
        "rate_window": meta.get("rate_window", ""),
        "load_profile": canonical_load_profile(meta, run_dir),
        "data_root": meta.get("data_root", ""),
        "dataset_prefix": meta.get("dataset_prefix", ""),
        "path": run_dir,
        **q,
    }

    if not logs:
        return [{**base, **empty_result_fields()}]

    rows = []
    for log_path in logs:
        with open(log_path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        params = parse_params(log_path, text)
        pr = parse_pr_table(text)
        ranked = parse_ranking(text)
        root_idx = base["root_idx"]
        root_rank = ""
        if root_idx != "":
            node_order = [node for node, _score in ranked]
            if int(root_idx) in node_order:
                root_rank = node_order.index(int(root_idx)) + 1

        rows.append(
            {
                **base,
                "dycause_log": log_path,
                "dycause_ok": all(pr[key] is not None for key in ("pr1", "pr2", "pr5", "acc")),
                "lag": params["lag"],
                "step": params["step"],
                "edge_thres": params["edge_thres"],
                "root_rank": root_rank,
                **pr,
            }
        )
    return rows


def empty_result_fields():
    return {
        "dycause_log": "",
        "dycause_ok": False,
        "lag": "",
        "step": "",
        "edge_thres": "",
        "root_rank": "",
        "pr1": "",
        "pr2": "",
        "pr3": "",
        "pr4": "",
        "pr5": "",
        "pr_avg": "",
        "acc": "",
    }


def write_csv(path, rows):
    if not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        if row.get("dycause_ok") and row.get("quality_valid"):
            groups[(row.get("load_profile", ""), row["experiment"])].append(row)

    result = []
    for (load_profile, exp), exp_rows in sorted(groups.items()):
        first = exp_rows[0]

        def values(key):
            return [float(row[key]) for row in exp_rows if row.get(key) not in ("", None)]

        pr2_values = values("pr2")
        acc_values = values("acc")
        result.append(
            {
                "experiment": exp,
                "load_profile": load_profile,
                "group": first.get("group", ""),
                "fault_type": first.get("fault_type", ""),
                "object_role": first.get("object_role", ""),
                "root": first.get("root", ""),
                "root_idx": first.get("root_idx", ""),
                "result_rows": len(exp_rows),
                "pr1_mean": mean(values("pr1")) if values("pr1") else None,
                "pr2_mean": mean(pr2_values) if pr2_values else None,
                "pr5_mean": mean(values("pr5")) if values("pr5") else None,
                "acc_mean": mean(acc_values) if acc_values else None,
                "acc_std": pstdev(acc_values) if len(acc_values) > 1 else 0.0,
                "top2_hit_rate": mean(1.0 if float(row["pr2"]) > 0 else 0.0 for row in exp_rows),
            }
        )
    return result


def aggregate_by_service_fault(rows):
    groups = defaultdict(list)
    for row in rows:
        if row.get("dycause_ok") and row.get("quality_valid"):
            groups[(row.get("load_profile", ""), row.get("root", ""), row.get("fault_type", ""))].append(row)

    result = []
    for (load_profile, root, fault_type), group_rows in sorted(groups.items()):
        def values(key):
            return [float(row[key]) for row in group_rows if row.get(key) not in ("", None)]

        acc_values = values("acc")
        result.append(
            {
                "load_profile": load_profile,
                "root": root,
                "fault_type": fault_type,
                "result_rows": len(group_rows),
                "pr2_mean": mean(values("pr2")) if values("pr2") else None,
                "pr5_mean": mean(values("pr5")) if values("pr5") else None,
                "acc_mean": mean(acc_values) if acc_values else None,
                "acc_std": pstdev(acc_values) if len(acc_values) > 1 else 0.0,
                "top2_hit_rate": mean(1.0 if float(row["pr2"]) > 0 else 0.0 for row in group_rows),
            }
        )
    return result


def fmt(value):
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def dataset_label(path):
    return os.path.basename(os.path.normpath(path))


def write_markdown(path, rows, main_params=None):
    main_params = main_params or DEFAULT_MAIN_PARAMS
    lines = [f"# SockShop Mesh Results ({dataset_label(os.path.dirname(path))})", ""]
    load_profiles = sorted({row.get("load_profile", "") for row in rows if row.get("load_profile")})
    if load_profiles:
        lines += [
            "## Load Profiles",
            "",
            "| Load Profile | Rows |",
            "|---|---:|",
        ]
        for profile in load_profiles:
            lines.append(f"| {profile} | {sum(1 for row in rows if row.get('load_profile') == profile)} |")
        lines.append("")

    main_rows = [
        row
        for row in rows
        if row.get("lag") == main_params["lag"]
        and row.get("step") == main_params["step"]
        and row.get("edge_thres") == main_params["edge_thres"]
    ]
    aggregate_source = main_rows if main_rows else rows
    agg = aggregate(aggregate_source)
    service_fault_agg = aggregate_by_service_fault(aggregate_source)
    if main_rows:
        lines += [
            "## Main Parameters",
            "",
            f"`lag={main_params['lag']}`, `step={main_params['step']}`, `edge_thres={main_params['edge_thres']}`",
            "",
            "| Experiment | Load Profile | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |",
            "|---|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|",
        ]
        for row in main_rows:
            lines.append(
                "| {experiment} | {load_profile} | {group} | {fault_type} | {object_role} | {run} | {quality_valid} | "
                "{root}({root_idx}) | {root_rank} | {pr1} | {pr2} | {pr5} | {acc} |".format(
                    **{key: fmt(value) for key, value in row.items()}
                )
            )
        lines.append("")

        lines += [
            "## Main Result Rows",
            "",
            "| Experiment | Load Profile | Group | Fault | Role | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |",
            "|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in main_rows:
            lines.append(
                "| {experiment} | {load_profile} | {group} | {fault_type} | {object_role} | {run} | {root}({root_idx}) | "
                "{quality_valid} | {root_rank} | {pr2} | {pr5} | {acc} | {baseline_mean} | {fault_mean} | {fault_baseline_ratio} |".format(
                    **{key: fmt(value) for key, value in row.items()}
                )
            )
        lines.append("")

    if agg:
        lines += [
            "## Aggregate Over Result Rows",
            "",
            "| Experiment | Load Profile | Group | Fault | Role | Root | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |",
            "|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in agg:
            lines.append(
                "| {experiment} | {load_profile} | {group} | {fault_type} | {object_role} | {root}({root_idx}) | "
                "{result_rows} | {pr1_mean} | {pr2_mean} | {pr5_mean} | {acc_mean} | {acc_std} | {top2_hit_rate} |".format(
                    **{key: fmt(value) for key, value in row.items()}
                )
            )
        lines.append("")

    if service_fault_agg:
        lines += [
            "## Aggregate By Service And Fault",
            "",
            "| Load Profile | Root | Fault | Result Rows | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
        for row in service_fault_agg:
            lines.append(
                "| {load_profile} | {root} | {fault_type} | {result_rows} | {pr2_mean} | {pr5_mean} | "
                "{acc_mean} | {acc_std} | {top2_hit_rate} |".format(
                    **{key: fmt(value) for key, value in row.items()}
                )
            )
        lines.append("")

    lines += [
        "## Runs",
        "",
        "| Experiment | Load Profile | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |",
        "|---|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        params = f"lag={row.get('lag')}, step={row.get('step')}, edge={row.get('edge_thres')}"
        lines.append(
            "| {experiment} | {load_profile} | {group} | {fault_type} | {object_role} | {run} | {quality_valid} | "
            "{root}({root_idx}) | {root_rank} | {pr1} | {pr2} | {pr5} | {acc} | {params} |".format(
                params=params,
                **{key: fmt(value) for key, value in row.items()},
            )
        )

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Summarize SockShop mesh experiment results")
    parser.add_argument("--data-root", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--main-lag", type=int, default=DEFAULT_MAIN_PARAMS["lag"])
    parser.add_argument("--main-step", type=int, default=DEFAULT_MAIN_PARAMS["step"])
    parser.add_argument("--main-edge-thres", type=float, default=DEFAULT_MAIN_PARAMS["edge_thres"])
    args = parser.parse_args()

    run_dirs = sorted(
        run_dir
        for run_dir in glob.glob(os.path.join(args.data_root, "*", "run*"))
        if os.path.isdir(run_dir)
    )
    rows = []
    for run_dir in run_dirs:
        rows.extend(summarize_run(run_dir))

    write_csv(os.path.join(args.data_root, "summary.csv"), rows)
    write_markdown(
        os.path.join(args.data_root, "results.md"),
        rows,
        main_params={"lag": args.main_lag, "step": args.main_step, "edge_thres": args.main_edge_thres},
    )
    print(f"Summarized {len(rows)} result rows from {len(run_dirs)} run directories.")


if __name__ == "__main__":
    main()
