"""
Run the formal SockShop + Istio batch once, with unattended monitoring.

This launcher wraps run_compressed_mesh_batch.py and adds:
  - one-shot defaults for the formal final_e1..final_e7 smoke plan
  - periodic heartbeat/status output to JSON
  - stall detection based on log inactivity
  - automatic chaos cleanup on failure/stall

Outputs under <data-root>:
  formal_once_stdout.log
  formal_once_stderr.log
  formal_once_status.json
  formal_once.pid
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime

from run_compressed_mesh_batch import minikube_mem_percent
from run_mesh_experiments import CHAOS_DIR, EXPERIMENTS, ROOT_DIR, delete_chaos


DEFAULT_PLAN = {
    "final_e1": 1,
    "final_e2": 1,
    "final_e3": 1,
    "final_e4": 1,
    "final_e5": 1,
    "final_e6": 1,
    "final_e7": 1,
}

DEFAULT_DATA_ROOT = os.path.join(ROOT_DIR, "data", "sockshop_mesh_final")
DEFAULT_DATASET_PREFIX = "final_"
DEFAULT_LOAD_PROFILE = "business-final-v3"


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def plan_to_text(plan):
    return ",".join(f"{name}={count}" for name, count in plan.items())


def parse_plan(text):
    plan = {}
    for item in text.split(","):
        name, count = item.split("=", 1)
        plan[name.strip()] = int(count)
    return plan


def read_tail_lines(path, limit=40):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read().splitlines()[-limit:]


def write_json(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def cleanup_all_chaos():
    for exp in EXPERIMENTS:
        delete_chaos(os.path.join(CHAOS_DIR, exp["yaml"]))


def clear_formal_outputs(data_root):
    for name in os.listdir(data_root):
        path = os.path.join(data_root, name)
        if name.startswith("final_e") and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        elif name in {"summary.csv", "results.md"} and os.path.isfile(path):
            os.remove(path)

    dycause_data_root = os.path.join(ROOT_DIR, "dycause_rca", "data")
    if os.path.isdir(dycause_data_root):
        for name in os.listdir(dycause_data_root):
            path = os.path.join(dycause_data_root, name)
            if name.startswith("final_") and os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)

    dycause_result_root = os.path.join(ROOT_DIR, "dycause_rca", "dycause", "results")
    if os.path.isdir(dycause_result_root):
        for name in os.listdir(dycause_result_root):
            path = os.path.join(dycause_result_root, name)
            if name.startswith("final_") and os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)


def latest_match(lines, pattern):
    compiled = re.compile(pattern)
    for line in reversed(lines):
        match = compiled.search(line)
        if match:
            return match
    return None


def parse_progress(stdout_path):
    lines = read_tail_lines(stdout_path, limit=120)
    progress = {
        "current_batch_index": None,
        "total_batches": None,
        "current_experiment": "",
        "current_run": "",
        "current_phase": "",
        "remaining_seconds": None,
        "last_quality_valid": None,
        "last_dataset": "",
        "last_data_shape": "",
        "tail": lines[-20:],
    }

    batch = latest_match(lines, r"\[batch\]\s+(\d+)/(\d+)\s+->\s+(\S+)\s+(run\d+)")
    if batch:
        progress["current_batch_index"] = int(batch.group(1))
        progress["total_batches"] = int(batch.group(2))
        progress["current_experiment"] = batch.group(3)
        progress["current_run"] = batch.group(4)

    if latest_match(lines, r"\[Phase 4\] DyCause"):
        progress["current_phase"] = "dycause"
    elif latest_match(lines, r"\[Cleanup\]"):
        progress["current_phase"] = "cleanup"
    elif latest_match(lines, r"\[Phase 3\] FAULT"):
        progress["current_phase"] = "fault"
    elif latest_match(lines, r"\[Phase 2\] Chaos"):
        progress["current_phase"] = "chaos"
    elif latest_match(lines, r"\[Phase 1\] BASELINE"):
        progress["current_phase"] = "baseline"

    remaining = latest_match(lines, r"(baseline|fault):\s+(\d+)s remaining")
    if remaining:
        progress["current_phase"] = remaining.group(1)
        progress["remaining_seconds"] = int(remaining.group(2))

    quality = latest_match(lines, r"Quality valid:\s+(True|False)")
    if quality:
        progress["last_quality_valid"] = quality.group(1) == "True"

    dataset = latest_match(lines, r"DyCause dataset:\s+(\S+)")
    if dataset:
        progress["last_dataset"] = dataset.group(1)

    data_shape = latest_match(lines, r"Data:\s+.+\((\d+x\d+)\)")
    if data_shape:
        progress["last_data_shape"] = data_shape.group(1)

    return progress


def build_batch_command(args, batch_script):
    return [
        sys.executable,
        "-u",
        batch_script,
        "--plan",
        args.plan,
        "--baseline",
        str(args.baseline),
        "--fault",
        str(args.fault),
        "--delay",
        str(args.delay),
        "--rate-window",
        args.rate_window,
        "--data-root",
        args.data_root,
        "--dataset-prefix",
        args.dataset_prefix,
        "--load-profile",
        args.load_profile,
        "--lag",
        str(args.lag),
        "--step",
        str(args.step),
        "--edge-thres",
        str(args.edge_thres),
        "--restart-threshold",
        str(args.restart_threshold),
    ]


def monitor_run(proc, stdout_path, stderr_path, status_path, pid_path, args):
    started_at = now_iso()
    last_stdout_mtime = os.path.getmtime(stdout_path) if os.path.exists(stdout_path) else time.time()

    write_json(
        status_path,
        {
            "state": "running",
            "started_at": started_at,
            "updated_at": now_iso(),
            "pid": proc.pid,
            "status_file": status_path,
            "stdout_log": stdout_path,
            "stderr_log": stderr_path,
            "plan": args.plan,
            "data_root": args.data_root,
            "dataset_prefix": args.dataset_prefix,
            "load_profile": args.load_profile,
        },
    )

    while True:
        rc = proc.poll()
        stdout_exists = os.path.exists(stdout_path)
        if stdout_exists:
            current_mtime = os.path.getmtime(stdout_path)
            if current_mtime > last_stdout_mtime:
                last_stdout_mtime = current_mtime
        else:
            current_mtime = last_stdout_mtime

        progress = parse_progress(stdout_path)
        mem = minikube_mem_percent()
        status = {
            "state": "running" if rc is None else ("completed" if rc == 0 else "failed"),
            "started_at": started_at,
            "updated_at": now_iso(),
            "pid": proc.pid,
            "returncode": rc,
            "status_file": status_path,
            "stdout_log": stdout_path,
            "stderr_log": stderr_path,
            "pid_file": pid_path,
            "plan": args.plan,
            "data_root": args.data_root,
            "dataset_prefix": args.dataset_prefix,
            "load_profile": args.load_profile,
            "stall_seconds": args.stall_seconds,
            "check_interval": args.check_interval,
            "minikube_mem_percent": mem,
            "seconds_since_stdout_update": int(time.time() - current_mtime),
            **progress,
        }
        write_json(status_path, status)

        if rc is not None:
            return rc

        if time.time() - current_mtime >= args.stall_seconds:
            status["state"] = "stalled"
            status["stalled_at"] = now_iso()
            write_json(status_path, status)
            proc.terminate()
            try:
                proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                proc.kill()
            cleanup_all_chaos()
            return 124

        time.sleep(args.check_interval)


def main():
    parser = argparse.ArgumentParser(description="Run the formal SockShop mesh smoke batch unattended")
    parser.add_argument("--plan", default=plan_to_text(DEFAULT_PLAN))
    parser.add_argument("--baseline", type=int, default=300)
    parser.add_argument("--fault", type=int, default=300)
    parser.add_argument("--delay", type=int, default=15)
    parser.add_argument("--rate-window", default="15s")
    parser.add_argument("--data-root", default=DEFAULT_DATA_ROOT)
    parser.add_argument("--dataset-prefix", default=DEFAULT_DATASET_PREFIX)
    parser.add_argument("--load-profile", default=DEFAULT_LOAD_PROFILE)
    parser.add_argument("--lag", type=int, default=5)
    parser.add_argument("--step", type=int, default=30)
    parser.add_argument("--edge-thres", type=float, default=0.8)
    parser.add_argument("--restart-threshold", type=float, default=92.0)
    parser.add_argument("--check-interval", type=int, default=30)
    parser.add_argument("--stall-seconds", type=int, default=900)
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    parse_plan(args.plan)

    data_root = os.path.abspath(args.data_root)
    os.makedirs(data_root, exist_ok=True)
    args.data_root = data_root

    batch_script = os.path.join(os.path.dirname(__file__), "run_compressed_mesh_batch.py")
    stdout_path = os.path.join(data_root, "formal_once_stdout.log")
    stderr_path = os.path.join(data_root, "formal_once_stderr.log")
    status_path = os.path.join(data_root, "formal_once_status.json")
    pid_path = os.path.join(data_root, "formal_once.pid")
    cmd = build_batch_command(args, batch_script)

    if args.dry_run:
        print("Formal unattended batch command:")
        print(" ".join(cmd))
        print(f"Status file: {status_path}")
        print(f"Stdout log : {stdout_path}")
        print(f"Stderr log : {stderr_path}")
        return

    if args.fresh:
        clear_formal_outputs(data_root)

    for path in (stdout_path, stderr_path, status_path, pid_path):
        if os.path.exists(path):
            os.remove(path)

    with open(stdout_path, "w", encoding="utf-8") as stdout_handle, open(
        stderr_path, "w", encoding="utf-8"
    ) as stderr_handle:
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT_DIR,
            stdout=stdout_handle,
            stderr=stderr_handle,
        )
        with open(pid_path, "w", encoding="utf-8") as handle:
            handle.write(str(proc.pid))

        rc = monitor_run(proc, stdout_path, stderr_path, status_path, pid_path, args)

    if rc == 0:
        print("Formal unattended batch completed successfully.")
        print(f"Status file: {status_path}")
        return

    if rc == 124:
        raise SystemExit(
            f"Formal unattended batch stalled. See status/logs under {data_root}"
        )

    raise SystemExit(f"Formal unattended batch failed with rc={rc}. See {status_path}")


if __name__ == "__main__":
    main()
