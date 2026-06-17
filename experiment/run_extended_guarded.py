"""
Run extended-compressed experiments one by one with hard quality gates.

This is the conservative runner for the formal sockshop_mesh_extended line:
every run gets pre-flight checks, post-run cluster checks, data quality checks,
DyCause return-code checks, and an immediate stop on invalid output.
"""

import argparse
import json
import os
import sys
from types import SimpleNamespace

import pandas as pd

from run_compressed_mesh_batch import (
    DEFAULT_MINIKUBE_CPUS,
    DEFAULT_MINIKUBE_MEMORY,
    ensure_load_gen,
    ensure_no_chaos,
    load_gen_manifest,
    minikube_mem_percent,
    next_run_id,
    parse_plan,
    restart_minikube,
    run_cmd,
    summarize,
)
from run_mesh_experiments import EXPERIMENTS, ROOT_DIR, run_one


DEFAULT_PLAN = ",".join(f"el_e{index}=1" for index in range(1, 17))
DEFAULT_DATA_ROOT = os.path.join(ROOT_DIR, "data", "sockshop_mesh_extended")
DEFAULT_LOAD_PROFILE = "legacy-compressed-v1"
DEFAULT_DATASET_PREFIX = "extended_"
DEFAULT_RATE_WINDOW = "15s"
DEFAULT_BASELINE = 300
DEFAULT_FAULT = 300
DEFAULT_DELAY = 15
DEFAULT_LAG = 7
DEFAULT_STEP = 30
DEFAULT_EDGE_THRES = 0.8
DEFAULT_MIN_VALID_RATIO = 0.95


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_deployments_available():
    result = run_cmd(["kubectl", "get", "deploy", "-n", "sock-shop", "-o", "json"], timeout=40)
    payload = json.loads(result.stdout)
    unavailable = []
    for item in payload.get("items", []):
        name = item["metadata"]["name"]
        desired = item.get("spec", {}).get("replicas", 1)
        available = item.get("status", {}).get("availableReplicas", 0)
        if desired and available < desired:
            unavailable.append(f"{name} {available}/{desired}")
    if unavailable:
        raise RuntimeError("SockShop deployments not fully available: " + ", ".join(unavailable))


def assert_load_gen_ready(manifest):
    result = run_cmd(["kubectl", "get", "pod", "load-gen", "-n", "sock-shop"], timeout=20, check=False)
    if result.returncode != 0:
        ensure_load_gen(manifest)
        return
    run_cmd(
        ["kubectl", "wait", "pod/load-gen", "-n", "sock-shop", "--for=condition=Ready", "--timeout=60s"],
        timeout=80,
    )


def istio_metric_series_count():
    result = run_cmd(
        [
            "kubectl",
            "exec",
            "-n",
            "monitoring",
            "deploy/prometheus-deployment",
            "--",
            "wget",
            "-qO-",
            "http://localhost:9090/api/v1/query?query=count(istio_request_duration_milliseconds_count)",
        ],
        timeout=40,
    )
    payload = json.loads(result.stdout)
    values = payload.get("data", {}).get("result", [])
    if not values:
        return 0
    return int(float(values[0]["value"][1]))


def assert_prometheus_ready(min_series):
    count = istio_metric_series_count()
    if count < min_series:
        raise RuntimeError(f"Istio latency series too low: {count} < {min_series}")
    print(f"[check] Istio latency series: {count}")


def assert_no_live_chaos():
    result = run_cmd(["kubectl", "get", "podchaos,networkchaos,stresschaos", "-A"], timeout=30, check=False)
    output = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        raise RuntimeError(output)
    if output and "No resources found" not in output:
        raise RuntimeError("Chaos resources still exist:\n" + output)


def preflight(manifest, min_series):
    print("[check] Pre-flight")
    assert_deployments_available()
    assert_load_gen_ready(manifest)
    ensure_no_chaos()
    assert_no_live_chaos()
    assert_prometheus_ready(min_series)


def postflight(manifest, min_series):
    print("[check] Post-run cluster state")
    ensure_no_chaos()
    assert_no_live_chaos()
    run_cmd(
        ["kubectl", "wait", "deploy", "--all", "-n", "sock-shop", "--for=condition=Available", "--timeout=240s"],
        timeout=270,
    )
    assert_deployments_available()
    assert_load_gen_ready(manifest)
    assert_prometheus_ready(min_series)


def validate_run_output(out_dir, args):
    print("[check] Run output quality")
    quality_path = os.path.join(out_dir, "quality.json")
    metadata_path = os.path.join(out_dir, "metadata.json")
    rawdata_path = os.path.join(out_dir, "rawdata.xlsx")
    for path in (quality_path, metadata_path, rawdata_path):
        if not os.path.exists(path):
            raise RuntimeError(f"Missing run artifact: {path}")

    rawdata = pd.read_excel(rawdata_path)
    expected_rows = args.baseline + args.fault
    if rawdata.shape != (expected_rows, 7):
        raise RuntimeError(f"Unexpected rawdata shape: {rawdata.shape}, expected ({expected_rows}, 7)")

    quality = load_json(quality_path)
    if not quality.get("valid"):
        raise RuntimeError(f"quality_valid=false in {quality_path}")
    bad_services = []
    for service, service_quality in quality.get("service_quality", {}).items():
        ratio = float(service_quality.get("valid_ratio", 0.0))
        if ratio < args.min_valid_ratio:
            bad_services.append(f"{service}={ratio:.3f}")
    if bad_services:
        raise RuntimeError("Service valid_ratio below threshold: " + ", ".join(bad_services))

    metadata = load_json(metadata_path)
    if metadata.get("load_profile") != args.load_profile:
        raise RuntimeError(
            f"Unexpected load_profile={metadata.get('load_profile')}, expected {args.load_profile}"
        )
    dycause_results = metadata.get("dycause_results", [])
    if not dycause_results:
        raise RuntimeError("No DyCause result recorded in metadata.json")
    failures = [item for item in dycause_results if int(item.get("returncode", 1)) != 0]
    if failures:
        raise RuntimeError(f"DyCause return code failure: {failures}")

    min_ratio = min(
        float(item.get("valid_ratio", 0.0)) for item in quality.get("service_quality", {}).values()
    )
    print(f"[check] rawdata={rawdata.shape[0]}x{rawdata.shape[1]} min_valid_ratio={min_ratio:.3f}")


def run_args_from_cli(args):
    return SimpleNamespace(
        baseline=args.baseline,
        fault=args.fault,
        delay=args.delay,
        rate_window=args.rate_window,
        cleanup_wait=args.cleanup_wait,
        min_valid_ratio=args.min_valid_ratio,
        run_dycause=True,
        sensitivity=False,
        no_wait=False,
        data_root=os.path.abspath(args.data_root),
        dataset_prefix=args.dataset_prefix,
        load_profile=args.load_profile,
        dycause_params={"lag": args.lag, "step": args.step, "edge_thres": args.edge_thres},
    )


def remove_empty_run_dirs(data_root):
    if not os.path.isdir(data_root):
        return
    for exp_name in os.listdir(data_root):
        exp_dir = os.path.join(data_root, exp_name)
        if not os.path.isdir(exp_dir):
            continue
        for run_name in os.listdir(exp_dir):
            run_dir = os.path.join(exp_dir, run_name)
            if not os.path.isdir(run_dir) or not run_name.startswith("run"):
                continue
            if not any(os.scandir(run_dir)):
                os.rmdir(run_dir)
                print(f"[cleanup] Removed empty run directory: {run_dir}")


def main():
    parser = argparse.ArgumentParser(description="Run extended experiments with per-run checks")
    parser.add_argument("--plan", default=DEFAULT_PLAN)
    parser.add_argument("--baseline", type=int, default=DEFAULT_BASELINE)
    parser.add_argument("--fault", type=int, default=DEFAULT_FAULT)
    parser.add_argument("--delay", type=int, default=DEFAULT_DELAY)
    parser.add_argument("--rate-window", default=DEFAULT_RATE_WINDOW)
    parser.add_argument("--data-root", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset-prefix", default=DEFAULT_DATASET_PREFIX)
    parser.add_argument("--load-profile", default=DEFAULT_LOAD_PROFILE)
    parser.add_argument("--load-manifest", default=None)
    parser.add_argument("--lag", type=int, default=DEFAULT_LAG)
    parser.add_argument("--step", type=int, default=DEFAULT_STEP)
    parser.add_argument("--edge-thres", type=float, default=DEFAULT_EDGE_THRES)
    parser.add_argument("--cleanup-wait", type=int, default=30)
    parser.add_argument("--min-valid-ratio", type=float, default=DEFAULT_MIN_VALID_RATIO)
    parser.add_argument("--min-istio-series", type=int, default=7)
    parser.add_argument("--restart-threshold", type=float, default=92.0)
    parser.add_argument("--minikube-cpus", type=int, default=DEFAULT_MINIKUBE_CPUS)
    parser.add_argument("--minikube-memory", type=int, default=DEFAULT_MINIKUBE_MEMORY)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = parse_plan(args.plan)
    exp_by_name = {exp["name"]: exp for exp in EXPERIMENTS}
    missing = sorted(set(plan) - set(exp_by_name))
    if missing:
        raise SystemExit(f"Unknown experiment(s): {', '.join(missing)}")

    manifest = load_gen_manifest(args.load_profile, args.load_manifest)
    run_args = run_args_from_cli(args)
    remove_empty_run_dirs(run_args.data_root)
    schedule = []
    for exp_name, count in plan.items():
        start = next_run_id(exp_name, run_args.data_root)
        for offset in range(count):
            schedule.append((exp_by_name[exp_name], start + offset))

    print("Guarded extended schedule:")
    print(f"Load profile: {args.load_profile}")
    print(f"Load generator: {manifest}")
    print(f"Data root: {run_args.data_root}")
    print(f"Minikube restart target: cpus={args.minikube_cpus} memory={args.minikube_memory}MB")
    for exp, run_id in schedule:
        print(f"  {exp['name']} run{run_id:02d}: baseline={args.baseline}s fault={args.fault}s")
    print(f"Total new runs: {len(schedule)}")
    if args.dry_run:
        return

    preflight(manifest, args.min_istio_series)
    for index, (exp, run_id) in enumerate(schedule, start=1):
        mem = minikube_mem_percent()
        if mem is not None:
            print(f"[resource] Minikube memory before run: {mem:.2f}%")
            if mem >= args.restart_threshold:
                restart_minikube(manifest, cpus=args.minikube_cpus, memory=args.minikube_memory)
                preflight(manifest, args.min_istio_series)

        print(f"[guarded] {index}/{len(schedule)} -> {exp['name']} run{run_id:02d}")
        preflight(manifest, args.min_istio_series)
        try:
            run_one(exp, run_id, run_args)
        finally:
            postflight(manifest, args.min_istio_series)

        out_dir = os.path.join(run_args.data_root, exp["name"], f"run{run_id:02d}")
        validate_run_output(out_dir, args)
        summarize(run_args.data_root)

    ensure_no_chaos()
    summarize(run_args.data_root)
    print("Guarded extended batch complete.")


if __name__ == "__main__":
    main()
