"""
Run the compressed SockShop Istio mesh experiment batch.

Plan:
  - business-front-proxy-v1 is the current mainline compressed batch
  - business-checkout-v2 is the candidate-object screening batch
  - business-final-v3 is the formal balanced batch for final_e* experiments
  - legacy direct-service batch has been archived
  - 300s baseline + 300s fault, 15s rate window, main DyCause params

The script starts from the next available runXX directory and writes the normal
per-run outputs plus <data-root>/summary.csv and results.md.
"""

import argparse
import os
import re
import subprocess
import sys
import time
from types import SimpleNamespace

from run_mesh_experiments import CHAOS_DIR, ROOT_DIR, EXPERIMENTS, delete_chaos, run_one


DEFAULT_PLAN = {
    "mesh_e1": 5,
    "mesh_e3": 5,
    "mesh_e5": 5,
    "mesh_e2": 2,
    "mesh_e4": 2,
}

LOAD_GEN_MANIFESTS = {
    "business-front-proxy-v1": os.path.join(os.path.dirname(__file__), "load-gen-business.yaml"),
    "business-checkout-v2": os.path.join(os.path.dirname(__file__), "load-gen-checkout.yaml"),
    "business-final-v3": os.path.join(os.path.dirname(__file__), "load-gen-final.yaml"),
}
DEFAULT_DATA_ROOT = os.path.join(ROOT_DIR, "data", "sockshop_mesh_business")
DEFAULT_LOAD_PROFILE = "business-front-proxy-v1"
DEFAULT_DATASET_PREFIX = "business_"


def run_cmd(args, timeout=60, input_text=None, check=True):
    result = subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed\n{result.stderr.strip()}")
    return result


def minikube_mem_percent():
    result = run_cmd(
        ["docker", "stats", "minikube", "--no-stream", "--format", "{{.MemPerc}}"],
        timeout=30,
        check=False,
    )
    if result.returncode != 0:
        return None
    match = re.search(r"([0-9.]+)%", result.stdout)
    return float(match.group(1)) if match else None


def next_run_id(exp_name, data_root):
    exp_dir = os.path.join(data_root, exp_name)
    if not os.path.isdir(exp_dir):
        return 1
    ids = []
    for name in os.listdir(exp_dir):
        match = re.fullmatch(r"run(\d+)", name)
        if match:
            ids.append(int(match.group(1)))
    return max(ids, default=0) + 1


def ensure_no_chaos():
    for exp in EXPERIMENTS:
        delete_chaos(os.path.join(CHAOS_DIR, exp["yaml"]))
    result = run_cmd(["kubectl", "get", "podchaos,networkchaos", "-A"], timeout=30, check=False)
    print(result.stdout.strip() or result.stderr.strip())


def load_gen_manifest(load_profile, explicit_manifest=None):
    if explicit_manifest:
        return os.path.abspath(explicit_manifest)
    if load_profile not in LOAD_GEN_MANIFESTS:
        known = ", ".join(sorted(LOAD_GEN_MANIFESTS))
        raise RuntimeError(f"Unknown load profile: {load_profile}. Choose one of: {known}")
    return LOAD_GEN_MANIFESTS[load_profile]


def ensure_load_gen(manifest):
    if not os.path.exists(manifest):
        raise RuntimeError(f"Load generator manifest not found: {manifest}")
    run_cmd(["kubectl", "delete", "pod", "load-gen", "-n", "sock-shop", "--ignore-not-found"], timeout=60)
    run_cmd(["kubectl", "apply", "-f", manifest], timeout=60)
    run_cmd(["kubectl", "wait", "pod/load-gen", "-n", "sock-shop", "--for=condition=Ready", "--timeout=120s"], timeout=140)


def check_prereqs(manifest):
    run_cmd(["kubectl", "get", "deploy", "-n", "sock-shop"], timeout=30)
    ensure_load_gen(manifest)
    run_cmd(
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
        timeout=30,
    )
    ensure_no_chaos()


def restart_minikube(manifest):
    print("[resource] Restarting Minikube to release memory before continuing.")
    ensure_no_chaos()
    run_cmd(["minikube", "stop"], timeout=240, check=False)
    run_cmd(["minikube", "start"], timeout=360)
    run_cmd(["kubectl", "wait", "deploy", "--all", "-n", "sock-shop", "--for=condition=Available", "--timeout=300s"], timeout=330)
    ensure_load_gen(manifest)
    check_prereqs(manifest)


def summarize(data_root):
    run_cmd(
        [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "summarize_mesh_results.py"),
            "--data-root",
            data_root,
            "--main-lag",
            "5",
            "--main-step",
            "30",
            "--main-edge-thres",
            "0.8",
        ],
        timeout=60,
    )


def parse_plan(plan_text):
    plan = {}
    for item in plan_text.split(","):
        name, count = item.split("=", 1)
        plan[name.strip()] = int(count)
    return plan


def main():
    parser = argparse.ArgumentParser(description="Run compressed mesh batch with resource checks")
    parser.add_argument("--plan", default=",".join(f"{k}={v}" for k, v in DEFAULT_PLAN.items()))
    parser.add_argument("--baseline", type=int, default=300)
    parser.add_argument("--fault", type=int, default=300)
    parser.add_argument("--delay", type=int, default=15)
    parser.add_argument("--rate-window", default="15s")
    parser.add_argument("--data-root", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset-prefix", default=DEFAULT_DATASET_PREFIX)
    parser.add_argument("--load-profile", default=DEFAULT_LOAD_PROFILE)
    parser.add_argument("--load-manifest", default=None)
    parser.add_argument("--lag", type=int, default=5)
    parser.add_argument("--step", type=int, default=30)
    parser.add_argument("--edge-thres", type=float, default=0.8)
    parser.add_argument("--restart-threshold", type=float, default=92.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = parse_plan(args.plan)
    exp_by_name = {exp["name"]: exp for exp in EXPERIMENTS}
    missing = sorted(set(plan) - set(exp_by_name))
    if missing:
        raise SystemExit(f"Unknown experiment(s): {', '.join(missing)}")
    manifest = load_gen_manifest(args.load_profile, args.load_manifest)

    run_args = SimpleNamespace(
        baseline=args.baseline,
        fault=args.fault,
        delay=args.delay,
        rate_window=args.rate_window,
        cleanup_wait=30,
        min_valid_ratio=0.95,
        run_dycause=True,
        sensitivity=False,
        no_wait=False,
        data_root=os.path.abspath(args.data_root),
        dataset_prefix=args.dataset_prefix,
        load_profile=args.load_profile,
        dycause_params={"lag": args.lag, "step": args.step, "edge_thres": args.edge_thres},
    )

    schedule = []
    for exp_name, count in plan.items():
        start = next_run_id(exp_name, run_args.data_root)
        for offset in range(count):
            schedule.append((exp_by_name[exp_name], start + offset))

    print("Compressed batch schedule:")
    print(f"Load profile: {args.load_profile}")
    print(f"Load generator: {manifest}")
    for exp, run_id in schedule:
        print(f"  {exp['name']} run{run_id:02d}: baseline={args.baseline}s fault={args.fault}s")
    print(f"Total new runs: {len(schedule)}")
    if args.dry_run:
        return

    check_prereqs(manifest)
    for index, (exp, run_id) in enumerate(schedule, start=1):
        mem = minikube_mem_percent()
        if mem is not None:
            print(f"[resource] Minikube memory before run: {mem:.2f}%")
            if mem >= args.restart_threshold:
                restart_minikube(manifest)
        print(f"[batch] {index}/{len(schedule)} -> {exp['name']} run{run_id:02d}")
        try:
            run_one(exp, run_id, run_args)
        except Exception:
            ensure_no_chaos()
            raise
        summarize(run_args.data_root)
        time.sleep(10)

    ensure_no_chaos()
    summarize(run_args.data_root)
    print("Compressed batch complete.")


if __name__ == "__main__":
    main()
