"""
Run DyCause SockShop experiments using Istio service-mesh latency metrics.

Outputs:
  <data-root>/<exp>/runXX/{baseline,fault,rawdata.xlsx,metadata.json}
  dycause_rca/data/<dataset-prefix><exp>_mesh_runXX/rawdata.xlsx
"""

import argparse
import csv
import itertools
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect_istio_latency import SERVICES, collect  # noqa: E402


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
CHAOS_DIR = os.path.join(BASE_DIR, "chaos")
DEFAULT_DATA_ROOT = os.path.join(ROOT_DIR, "data", "sockshop_mesh_extended")
DATA_ROOT = DEFAULT_DATA_ROOT
DYCAUSE_ROOT = os.path.join(ROOT_DIR, "dycause_rca")


def experiment(name, yaml, root, root_idx, desc, group, fault_type, object_role):
    return {
        "name": name,
        "yaml": yaml,
        "root": root,
        "root_idx": root_idx,
        "desc": desc,
        "group": group,
        "fault_type": fault_type,
        "object_role": object_role,
    }


EXPERIMENTS = [
    experiment(
        "mesh_e1",
        "e1-pod-kill-payment.yaml",
        "payment",
        5,
        "Istio latency + Pod-Kill: payment",
        "business",
        "pod-kill",
        "main-reference",
    ),
    experiment(
        "mesh_e2",
        "e2-pod-kill-user.yaml",
        "user",
        7,
        "Istio latency + Pod-Kill: user",
        "business",
        "pod-kill",
        "negative-case",
    ),
    experiment(
        "mesh_e3",
        "mesh-e3-network-delay-payment.yaml",
        "payment",
        5,
        "Istio latency + NetworkDelay 300ms: payment",
        "business",
        "network-delay",
        "main-reference",
    ),
    experiment(
        "mesh_e4",
        "mesh-e4-network-delay-user.yaml",
        "user",
        7,
        "Istio latency + NetworkDelay 300ms: user",
        "business",
        "network-delay",
        "negative-case",
    ),
    experiment(
        "mesh_e5",
        "mesh-e5-network-delay-catalogue.yaml",
        "catalogue",
        2,
        "Istio latency + NetworkDelay 300ms: catalogue",
        "business",
        "network-delay",
        "negative-case",
    ),
    experiment(
        "mesh_e6",
        "mesh-e6-network-delay-orders.yaml",
        "orders",
        4,
        "Istio latency + NetworkDelay 300ms: orders",
        "candidate",
        "network-delay",
        "candidate",
    ),
    experiment(
        "mesh_e7",
        "mesh-e7-network-delay-carts.yaml",
        "carts",
        3,
        "Istio latency + NetworkDelay 300ms: carts",
        "candidate",
        "network-delay",
        "candidate",
    ),
    experiment(
        "mesh_e8",
        "mesh-e8-network-delay-shipping.yaml",
        "shipping",
        6,
        "Istio latency + NetworkDelay 300ms: shipping",
        "candidate",
        "network-delay",
        "negative-case",
    ),
    experiment(
        "mesh_e9",
        "mesh-e9-pod-kill-orders.yaml",
        "orders",
        4,
        "Istio latency + Pod-Kill: orders",
        "candidate",
        "pod-kill",
        "candidate",
    ),
    experiment(
        "final_e1",
        "final-e1-pod-kill-payment.yaml",
        "payment",
        5,
        "Formal: Pod-Kill payment",
        "formal",
        "pod-kill",
        "core",
    ),
    experiment(
        "final_e2",
        "final-e2-network-delay-payment.yaml",
        "payment",
        5,
        "Formal: NetworkDelay 300ms payment",
        "formal",
        "network-delay",
        "core",
    ),
    experiment(
        "final_e3",
        "final-e3-network-loss-payment.yaml",
        "payment",
        5,
        "Formal: NetworkLoss 5% payment",
        "formal",
        "network-loss",
        "augmentation",
    ),
    experiment(
        "final_e4",
        "final-e4-pod-kill-orders.yaml",
        "orders",
        4,
        "Formal: Pod-Kill orders",
        "formal",
        "pod-kill",
        "core",
    ),
    experiment(
        "final_e5",
        "final-e5-network-delay-orders.yaml",
        "orders",
        4,
        "Formal: NetworkDelay 300ms orders",
        "formal",
        "network-delay",
        "core",
    ),
    experiment(
        "final_e6",
        "final-e6-network-loss-orders.yaml",
        "orders",
        4,
        "Formal: NetworkLoss 5% orders",
        "formal",
        "network-loss",
        "augmentation",
    ),
    experiment(
        "final_e7",
        "final-e7-network-delay-carts.yaml",
        "carts",
        3,
        "Formal: NetworkDelay 300ms carts",
        "formal",
        "network-delay",
        "supplementary",
    ),
    experiment(
        "el_e1",
        "el-e1-network-loss-payment.yaml",
        "payment",
        5,
        "Extended: NetworkLoss 5% payment",
        "extended",
        "network-loss",
        "core",
    ),
    experiment(
        "el_e2",
        "el-e2-network-corrupt-payment.yaml",
        "payment",
        5,
        "Extended: NetworkCorrupt 2% payment",
        "extended",
        "network-corrupt",
        "core",
    ),
    experiment(
        "el_e3",
        "el-e3-network-duplicate-payment.yaml",
        "payment",
        5,
        "Extended: NetworkDuplicate 5% payment",
        "extended",
        "network-duplicate",
        "core",
    ),
    experiment(
        "el_e4",
        "el-e4-cpu-stress-payment.yaml",
        "payment",
        5,
        "Extended: CPUStress 80% payment",
        "extended",
        "cpu-stress",
        "exploratory",
    ),
    experiment(
        "el_e5",
        "el-e5-pod-kill-orders.yaml",
        "orders",
        4,
        "Extended: Pod-Kill orders",
        "extended",
        "pod-kill",
        "core",
    ),
    experiment(
        "el_e6",
        "el-e6-network-delay-orders.yaml",
        "orders",
        4,
        "Extended: NetworkDelay 300ms orders",
        "extended",
        "network-delay",
        "core",
    ),
    experiment(
        "el_e7",
        "el-e7-network-loss-orders.yaml",
        "orders",
        4,
        "Extended: NetworkLoss 5% orders",
        "extended",
        "network-loss",
        "core",
    ),
    experiment(
        "el_e8",
        "el-e8-network-corrupt-orders.yaml",
        "orders",
        4,
        "Extended: NetworkCorrupt 2% orders",
        "extended",
        "network-corrupt",
        "core",
    ),
    experiment(
        "el_e9",
        "el-e9-network-duplicate-orders.yaml",
        "orders",
        4,
        "Extended: NetworkDuplicate 5% orders",
        "extended",
        "network-duplicate",
        "core",
    ),
    experiment(
        "el_e10",
        "el-e10-cpu-stress-orders.yaml",
        "orders",
        4,
        "Extended: CPUStress 80% orders",
        "extended",
        "cpu-stress",
        "exploratory",
    ),
    experiment(
        "el_e11",
        "el-e11-pod-kill-carts.yaml",
        "carts",
        3,
        "Extended: Pod-Kill carts",
        "extended",
        "pod-kill",
        "core",
    ),
    experiment(
        "el_e12",
        "el-e12-network-delay-carts.yaml",
        "carts",
        3,
        "Extended: NetworkDelay 300ms carts",
        "extended",
        "network-delay",
        "core",
    ),
    experiment(
        "el_e13",
        "el-e13-network-loss-carts.yaml",
        "carts",
        3,
        "Extended: NetworkLoss 5% carts",
        "extended",
        "network-loss",
        "core",
    ),
    experiment(
        "el_e14",
        "el-e14-network-corrupt-carts.yaml",
        "carts",
        3,
        "Extended: NetworkCorrupt 2% carts",
        "extended",
        "network-corrupt",
        "core",
    ),
    experiment(
        "el_e15",
        "el-e15-network-duplicate-carts.yaml",
        "carts",
        3,
        "Extended: NetworkDuplicate 5% carts",
        "extended",
        "network-duplicate",
        "core",
    ),
    experiment(
        "el_e16",
        "el-e16-cpu-stress-carts.yaml",
        "carts",
        3,
        "Extended: CPUStress 80% carts",
        "extended",
        "cpu-stress",
        "exploratory",
    ),
]


DEFAULT_DYCAUSE_PARAMS = {"lag": 7, "step": 30, "edge_thres": 0.8}
SENSITIVITY_GRID = {
    "lag": [3, 5, 7],
    "step": [20, 30, 60],
    "edge_thres": [0.4, 0.6, 0.8],
}


def run_checked(args, timeout=60, cwd=None, capture=True):
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() if capture else ""
        raise RuntimeError(f"Command failed: {' '.join(args)}\n{detail}")
    return result


def apply_chaos(yaml_path):
    run_checked(["kubectl", "apply", "-f", yaml_path], timeout=30)


def delete_chaos(yaml_path):
    subprocess.run(
        ["kubectl", "delete", "-f", yaml_path, "--ignore-not-found"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def merge_quality(baseline_quality, fault_quality, min_valid_ratio):
    service_quality = {}
    valid = True
    for service in SERVICES:
        bq = baseline_quality["service_quality"].get(service, {})
        fq = fault_quality["service_quality"].get(service, {})
        expected = int(bq.get("expected_points", 0)) + int(fq.get("expected_points", 0))
        valid_points = int(bq.get("valid_points", 0)) + int(fq.get("valid_points", 0))
        missing_points = int(bq.get("missing_points", 0)) + int(fq.get("missing_points", 0))
        zero_points = int(bq.get("zero_points", 0)) + int(fq.get("zero_points", 0))
        valid_ratio = valid_points / expected if expected else 0.0
        service_quality[service] = {
            "expected_points": expected,
            "valid_points": valid_points,
            "missing_points": missing_points,
            "zero_points": zero_points,
            "valid_ratio": valid_ratio,
        }
        valid = valid and valid_ratio >= min_valid_ratio
    return {
        "min_valid_ratio": min_valid_ratio,
        "valid": valid,
        "service_quality": service_quality,
    }


def export_for_dycause(merged_df, dataset_name):
    dycause_data = os.path.join(DYCAUSE_ROOT, "data", dataset_name)
    os.makedirs(dycause_data, exist_ok=True)
    transposed = merged_df.T
    transposed.columns = range(transposed.shape[1])
    transposed.to_excel(os.path.join(dycause_data, "rawdata.xlsx"), index=True, header=False)
    return dycause_data


def dycause_command(dataset, root_idx, anomaly, baseline, fault, params):
    return [
        sys.executable,
        "main_dycause_mp.py",
        dataset,
        "0",
        str(root_idx),
        "--start",
        str(anomaly),
        "--bef",
        str(baseline),
        "--aft",
        str(fault),
        "--lag",
        str(params["lag"]),
        "--step",
        str(params["step"]),
        "--edge_thres",
        str(params["edge_thres"]),
        "--verbose",
        "2",
    ]


def run_dycause(dataset, root_idx, anomaly, baseline, fault, params, out_dir):
    label = f"lag{params['lag']}_step{params['step']}_edge{params['edge_thres']}"
    log_path = os.path.join(out_dir, f"dycause_{label}.log")
    cmd = dycause_command(dataset, root_idx, anomaly, baseline, fault, params)

    result = subprocess.run(
        cmd,
        cwd=DYCAUSE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
    )
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n\n")
        handle.write(result.stdout)
        if result.stderr:
            handle.write("\n[stderr]\n")
            handle.write(result.stderr)

    tail_lines = result.stdout.splitlines()[-30:]
    return {
        "params": params,
        "returncode": result.returncode,
        "log_path": log_path,
        "tail": tail_lines,
    }


def parameter_sets(enable_sensitivity):
    if not enable_sensitivity:
        return [DEFAULT_DYCAUSE_PARAMS]
    return [
        {"lag": lag, "step": step, "edge_thres": edge}
        for lag, step, edge in itertools.product(
            SENSITIVITY_GRID["lag"],
            SENSITIVITY_GRID["step"],
            SENSITIVITY_GRID["edge_thres"],
        )
    ]


def main_dycause_params(args):
    return getattr(args, "dycause_params", DEFAULT_DYCAUSE_PARAMS)


def write_summary_row(row, data_root=None):
    data_root = data_root or DATA_ROOT
    os.makedirs(data_root, exist_ok=True)
    path = os.path.join(data_root, "summary.csv")
    fieldnames = [
        "timestamp",
        "experiment",
        "run",
        "dataset",
        "root",
        "root_idx",
        "group",
        "fault_type",
        "object_role",
        "valid",
        "min_valid_ratio",
        "dycause_runs",
        "dycause_failures",
        "load_profile",
        "data_root",
        "dataset_prefix",
        "path",
    ]
    existing_rows = []
    exists = os.path.exists(path)
    if exists:
        with open(path, "r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            existing_rows = list(reader)
            current_fields = reader.fieldnames or []
        if current_fields != fieldnames:
            for field in current_fields:
                if field not in fieldnames:
                    fieldnames.append(field)
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_rows)
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in fieldnames})


def wait_window(seconds, label, no_wait=False):
    if no_wait or seconds <= 0:
        print(f"  Skipping live wait for {label} ({seconds}s)")
        return
    print(f"  Waiting {seconds}s for {label} window...")
    deadline = time.time() + seconds
    while True:
        remaining = int(deadline - time.time())
        if remaining <= 0:
            break
        print(f"    {label}: {remaining}s remaining", end="\r", flush=True)
        time.sleep(min(10, remaining))
    print(" " * 50, end="\r")


def run_one(exp, run_id, args):
    data_root = getattr(args, "data_root", DATA_ROOT)
    dataset_prefix = getattr(args, "dataset_prefix", "")
    load_profile = getattr(args, "load_profile", "direct-service-v1")
    run_name = f"run{run_id:02d}"
    out_dir = os.path.join(data_root, exp["name"], run_name)
    os.makedirs(out_dir, exist_ok=True)
    yaml_path = os.path.join(CHAOS_DIR, exp["yaml"])
    anomaly = args.baseline + args.delay
    dataset = f"{dataset_prefix}{exp['name']}_mesh_run{run_id:02d}"

    print(f"\n{'#' * 60}")
    print(f"# {exp['name']} {run_name}: {exp['desc']}")
    print(f"{'#' * 60}")

    print("\n[Phase 1] BASELINE")
    wait_window(args.baseline, "baseline", no_wait=args.no_wait)
    baseline_df, baseline_quality = collect(
        SERVICES,
        args.baseline,
        os.path.join(out_dir, "baseline"),
        rate_window=args.rate_window,
        min_valid_ratio=args.min_valid_ratio,
    )

    print(f"\n[Phase 2] Chaos: {exp['yaml']}")
    apply_chaos(yaml_path)
    chaos_apply_epoch = int(time.time())
    time.sleep(args.delay)

    try:
        print("\n[Phase 3] FAULT")
        wait_window(args.fault, "fault", no_wait=args.no_wait)
        fault_df, fault_quality = collect(
            SERVICES,
            args.fault,
            os.path.join(out_dir, "fault"),
            rate_window=args.rate_window,
            min_valid_ratio=args.min_valid_ratio,
        )
    finally:
        print("\n[Cleanup]")
        delete_chaos(yaml_path)
        time.sleep(args.cleanup_wait)

    merged = pd.concat([baseline_df, fault_df], ignore_index=True)
    merged.to_excel(os.path.join(out_dir, "rawdata.xlsx"), index=False)

    quality = merge_quality(baseline_quality, fault_quality, args.min_valid_ratio)
    with open(os.path.join(out_dir, "quality.json"), "w", encoding="utf-8") as handle:
        json.dump(quality, handle, indent=2)

    dycause_data = export_for_dycause(merged, dataset)

    dycause_results = []
    if args.run_dycause:
        print("\n[Phase 4] DyCause")
        params_list = parameter_sets(args.sensitivity) if args.sensitivity else [main_dycause_params(args)]
        for params in params_list:
            result = run_dycause(
                dataset,
                exp["root_idx"],
                anomaly,
                args.baseline,
                args.fault,
                params,
                out_dir,
            )
            dycause_results.append(result)
            print(
                f"  lag={params['lag']} step={params['step']} "
                f"edge={params['edge_thres']} rc={result['returncode']}"
            )

    meta = {
        "experiment": exp["name"],
        "run": run_name,
        "desc": exp["desc"],
        "root_cause": exp["root"],
        "root_cause_indices": [exp["root_idx"]],
        "group": exp.get("group", ""),
        "fault_type": exp.get("fault_type", ""),
        "object_role": exp.get("object_role", ""),
        "frontend_idx": 0,
        "services": SERVICES,
        "anomaly_start_second": anomaly,
        "baseline_seconds": args.baseline,
        "fault_seconds": args.fault,
        "delay_seconds": args.delay,
        "rate_window": args.rate_window,
        "load_profile": load_profile,
        "data_root": data_root,
        "dataset_prefix": dataset_prefix,
        "chaos_apply_epoch": chaos_apply_epoch,
        "dycause_dataset": dataset,
        "dycause_data_dir": dycause_data,
        "dycause_cmd": " ".join(
            dycause_command(
                dataset,
                exp["root_idx"],
                anomaly,
                args.baseline,
                args.fault,
                main_dycause_params(args),
            )
        ),
        "dycause_results": dycause_results,
        "quality_valid": quality["valid"],
    }
    with open(os.path.join(out_dir, "metadata.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)

    dycause_failures = sum(1 for item in dycause_results if item["returncode"] != 0)
    write_summary_row(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "experiment": exp["name"],
            "run": run_name,
            "dataset": dataset,
            "root": exp["root"],
            "root_idx": exp["root_idx"],
            "group": exp.get("group", ""),
            "fault_type": exp.get("fault_type", ""),
            "object_role": exp.get("object_role", ""),
            "valid": quality["valid"],
            "min_valid_ratio": args.min_valid_ratio,
            "dycause_runs": len(dycause_results),
            "dycause_failures": dycause_failures,
            "load_profile": load_profile,
            "data_root": data_root,
            "dataset_prefix": dataset_prefix,
            "path": out_dir,
        },
        data_root=data_root,
    )

    print(f"\n  Data: {os.path.relpath(out_dir, ROOT_DIR)} ({merged.shape[0]}x{merged.shape[1]})")
    print(f"  DyCause dataset: {dataset}")
    print(f"  Quality valid: {quality['valid']}")


def cleanup_dycause_cache():
    cache_root = os.path.join(DYCAUSE_ROOT, "dycause", "results")
    if not os.path.isdir(cache_root):
        return
    for name in os.listdir(cache_root):
        if name.startswith(("mesh_e", "business_", "candidate_", "final_", "el_e", "extended_")):
            shutil.rmtree(os.path.join(cache_root, name), ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Run Istio mesh latency experiments for SockShop")
    parser.add_argument("--run-all", action="store_true")
    parser.add_argument("--exp", default=None, help="Single experiment name: mesh_e*, final_e*, or el_e*")
    parser.add_argument("--repeat", type=int, default=10)
    parser.add_argument("--baseline", type=int, default=600)
    parser.add_argument("--fault", type=int, default=600)
    parser.add_argument("--delay", type=int, default=15)
    parser.add_argument("--rate-window", default="15s")
    parser.add_argument("--data-root", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset-prefix", default="")
    parser.add_argument("--load-profile", default="legacy-compressed-v1")
    parser.add_argument("--cleanup-wait", type=int, default=30)
    parser.add_argument("--min-valid-ratio", type=float, default=0.95)
    parser.add_argument("--run-dycause", action="store_true")
    parser.add_argument("--sensitivity", action="store_true")
    parser.add_argument("--clear-dycause-cache", action="store_true")
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Query recent Prometheus history without waiting; useful only for quick pipeline checks.",
    )
    args = parser.parse_args()
    global DATA_ROOT
    DATA_ROOT = os.path.abspath(args.data_root)

    if args.clear_dycause_cache:
        cleanup_dycause_cache()

    if args.exp:
        selected = [exp for exp in EXPERIMENTS if exp["name"] == args.exp]
        if not selected:
            names = ", ".join(exp["name"] for exp in EXPERIMENTS)
            raise SystemExit(f"Unknown experiment: {args.exp}. Choose one of: {names}")
    elif args.run_all:
        selected = EXPERIMENTS
    else:
        parser.print_help()
        return

    for exp in selected:
        for run_id in range(1, args.repeat + 1):
            try:
                run_one(exp, run_id, args)
            except Exception as exc:
                print(f"ERROR {exp['name']} run{run_id:02d}: {exc}")
                delete_chaos(os.path.join(CHAOS_DIR, exp["yaml"]))
                time.sleep(args.cleanup_wait)


if __name__ == "__main__":
    main()
