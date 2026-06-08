"""
DyCause experiment runner for SockShop.
4 Go services (front-end, catalogue, payment, user) - request_duration_seconds latency.
ChaosMesh fault injection (Pod-Kill).

Usage:
  python run_experiments.py --run-all
  python run_experiments.py --exp e1
"""

import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect_latency import collect

SERVICES = ["front-end", "catalogue", "payment", "user"]
CHAOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chaos")

EXPERIMENTS = [
    {"name": "e1", "yaml": "e1-pod-kill-payment.yaml", "root": ["payment"], "r_idx": [2], "desc": "Pod-Kill: payment"},
    {"name": "e2", "yaml": "e2-pod-kill-user.yaml",    "root": ["user"],    "r_idx": [3], "desc": "Pod-Kill: user"},
]


def run(exp, baseline=300, fault=300, delay=15):
    d = os.path.join("data", "sockshop", exp["name"])
    print(f"\n{'#'*50}\n# {exp['name']}: {exp['desc']}\n{'#'*50}")

    print("\n[Phase 1] BASELINE")
    collect(SERVICES, baseline, os.path.join(d, "baseline"))

    yaml = os.path.join(CHAOS_DIR, exp["yaml"])
    print(f"\n[Phase 2] Chaos: {exp['yaml']}")
    subprocess.run(["kubectl", "apply", "-f", yaml], capture_output=True, text=True, timeout=30)
    time.sleep(delay)

    try:
        print(f"\n[Phase 3] FAULT")
        collect(SERVICES, fault, os.path.join(d, "fault"))
    finally:
        print("\n[Cleanup]")
        subprocess.run(["kubectl", "delete", "-f", yaml, "--ignore-not-found"],
                       capture_output=True, text=True, timeout=30)
        time.sleep(30)

    import pandas as pd
    b = pd.read_excel(os.path.join(d, "baseline", "rawdata.xlsx"))
    f = pd.read_excel(os.path.join(d, "fault", "rawdata.xlsx"))
    merged = pd.concat([b, f], ignore_index=True)
    merged.to_excel(os.path.join(d, "rawdata.xlsx"), index=False)

    anomaly = baseline + delay
    meta = {
        "experiment": exp["name"],
        "desc": exp["desc"],
        "root_cause_indices": exp["r_idx"],
        "frontend_idx": 0,
        "services": SERVICES,
        "anomaly_start_second": anomaly,
        "dycause_cmd": (f"python main_dycause_mp.py {exp['name']} 0 {exp['r_idx'][0]} "
                        f"--start {anomaly} --bef {baseline} --aft {fault} "
                        f"--lag 5 --step 30 --edge_thres 0.7 --verbose 2")
    }
    with open(os.path.join(d, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)

    # Also copy to dycause_rca
    dycause_data = os.path.join("dycause_rca", "data", exp["name"])
    os.makedirs(dycause_data, exist_ok=True)
    df_t = merged.T
    df_t.columns = range(df_t.shape[1])
    df_t.to_excel(os.path.join(dycause_data, "rawdata.xlsx"), index=True, header=False)

    print(f"\n  Data: data/sockshop/{exp['name']}/rawdata.xlsx  ({merged.shape[0]}x{merged.shape[1]})")
    print(f"  Root idx: {exp['r_idx']}  Anomaly: {anomaly}s")
    print(f"  {meta['dycause_cmd']}")


def main():
    parser = argparse.ArgumentParser(description="Run SockShop DyCause experiments")
    parser.add_argument("--run-all", action="store_true", help="Run all experiments")
    parser.add_argument("--exp", default=None, help="Single experiment name (e1/e2)")
    parser.add_argument("--baseline", type=int, default=300)
    parser.add_argument("--fault", type=int, default=300)
    args = parser.parse_args()

    if args.exp:
        exp = next((e for e in EXPERIMENTS if e["name"] == args.exp), None)
        if exp:
            run(exp, baseline=args.baseline, fault=args.fault)
        else:
            print(f"Unknown experiment: {args.exp}")
            return
    elif args.run_all:
        for exp in EXPERIMENTS:
            try:
                run(exp, baseline=args.baseline, fault=args.fault)
            except Exception as ex:
                print(f"ERROR {exp['name']}: {ex}")
                yaml = os.path.join(CHAOS_DIR, exp["yaml"])
                subprocess.run(["kubectl", "delete", "-f", yaml, "--ignore-not-found"],
                               capture_output=True, text=True, timeout=30)
                time.sleep(30)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
