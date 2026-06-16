"""
Run DyCause on already-collected SockShop mesh runs.

This is useful for parameter sensitivity without recollecting 600s+600s data.
"""

import argparse
import itertools
import json
import os
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DYCAUSE_ROOT = os.path.join(ROOT, "dycause_rca")


def parse_csv_numbers(value, cast):
    return [cast(item.strip()) for item in value.split(",") if item.strip()]


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


def run_one(run_dir, params, timeout):
    meta_path = os.path.join(run_dir, "metadata.json")
    with open(meta_path, "r", encoding="utf-8") as handle:
        meta = json.load(handle)

    dataset = meta["dycause_dataset"]
    root_idx = meta["root_cause_indices"][0]
    anomaly = meta["anomaly_start_second"]
    baseline = meta["baseline_seconds"]
    fault = meta["fault_seconds"]

    label = f"lag{params['lag']}_step{params['step']}_edge{params['edge_thres']}"
    log_path = os.path.join(run_dir, f"dycause_{label}.log")
    cmd = dycause_command(dataset, root_idx, anomaly, baseline, fault, params)

    print(f"Running {label}")
    result = subprocess.run(
        cmd,
        cwd=DYCAUSE_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n\n")
        handle.write(result.stdout)
        if result.stderr:
            handle.write("\n[stderr]\n")
            handle.write(result.stderr)

    meta.setdefault("dycause_results", [])
    meta["dycause_results"].append(
        {
            "params": params,
            "returncode": result.returncode,
            "log_path": log_path,
            "tail": result.stdout.splitlines()[-30:],
        }
    )
    with open(meta_path, "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)

    print(f"  rc={result.returncode} log={log_path}")


def main():
    parser = argparse.ArgumentParser(description="Run DyCause sensitivity on existing mesh run data")
    parser.add_argument("run_dir", help="Path such as data/sockshop_mesh/mesh_e1/run01")
    parser.add_argument("--lags", default="3,5,7")
    parser.add_argument("--steps", default="20,30,60")
    parser.add_argument("--edge-thres", default="0.6,0.7,0.8")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    lags = parse_csv_numbers(args.lags, int)
    steps = parse_csv_numbers(args.steps, int)
    edges = parse_csv_numbers(args.edge_thres, float)

    for lag, step, edge in itertools.product(lags, steps, edges):
        if step <= 3 * lag + 1:
            print(f"Skipping lag={lag} step={step}: DyCause requires step > 3*lag+1")
            continue
        run_one(args.run_dir, {"lag": lag, "step": step, "edge_thres": edge}, args.timeout)


if __name__ == "__main__":
    main()
