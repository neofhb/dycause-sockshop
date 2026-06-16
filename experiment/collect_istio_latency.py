"""
Collect Istio destination workload latency for SockShop HTTP services.

The output format matches collect_latency.py:
  - columns are services
  - rows are one-second samples
  - rawdata.xlsx is ready for merge/export by run_mesh_experiments.py

Istio metric:
  istio_request_duration_milliseconds_sum/count, reporter="destination"
The script converts milliseconds to seconds for consistency with the existing
request_duration_seconds data.
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from urllib.parse import quote

import numpy as np
import pandas as pd


SERVICES = [
    "front-end",
    "catalogue",
    "carts",
    "orders",
    "payment",
    "shipping",
    "user",
]


def kubectl_exec(url, timeout=30):
    result = subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            "monitoring",
            "deploy/prometheus-deployment",
            "--",
            "wget",
            "-qO-",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def query_range(query, start, end, step="1s"):
    encoded = quote(query, safe="")
    url = (
        "http://localhost:9090/api/v1/query_range?"
        f"query={encoded}&start={start}&end={end}&step={step}"
    )
    return json.loads(kubectl_exec(url))


def build_query(service, namespace="sock-shop", rate_window="15s"):
    labels = (
        f'reporter="destination",'
        f'destination_workload_namespace="{namespace}",'
        f'destination_workload="{service}"'
    )
    return (
        f"(sum(rate(istio_request_duration_milliseconds_sum{{{labels}}}[{rate_window}])) "
        f"/ sum(rate(istio_request_duration_milliseconds_count{{{labels}}}[{rate_window}]))) "
        f"/ 1000"
    )


def quality_for(values, expected_points):
    finite = np.isfinite(values)
    valid_points = int(np.sum(finite))
    zero_points = int(np.sum(values[finite] == 0.0))
    missing_points = int(expected_points - valid_points)
    valid_ratio = valid_points / expected_points if expected_points else 0.0
    return {
        "expected_points": int(expected_points),
        "valid_points": valid_points,
        "missing_points": missing_points,
        "zero_points": zero_points,
        "valid_ratio": valid_ratio,
    }


def collect(
    services,
    duration,
    out_dir,
    namespace="sock-shop",
    step="1s",
    rate_window="15s",
    min_valid_ratio=0.95,
):
    end = int(time.time())
    start = end - duration
    os.makedirs(out_dir, exist_ok=True)

    print(f"[{datetime.now()}] Istio latency: {len(services)} svc x {duration}s")
    matrix = np.full((duration, len(services)), np.nan)
    raw_quality = {}

    for col, service in enumerate(services):
        print(f"  [{col + 1}/{len(services)}] {service:<14}", end=" ", flush=True)
        try:
            response = query_range(
                build_query(service, namespace=namespace, rate_window=rate_window),
                start,
                end,
                step,
            )
            results = response.get("data", {}).get("result", [])
            if results:
                for series in results:
                    for timestamp, value in series.get("values", []):
                        idx = int(float(timestamp)) - start
                        value = float(value)
                        if 0 <= idx < duration and np.isfinite(value):
                            matrix[idx, col] = value
                raw_quality[service] = quality_for(matrix[:, col], duration)
                print(
                    f"OK ({raw_quality[service]['valid_points']}/{duration}, "
                    f"{raw_quality[service]['valid_ratio']:.1%})"
                )
            else:
                raw_quality[service] = quality_for(matrix[:, col], duration)
                print("NO DATA")
        except Exception as exc:
            raw_quality[service] = quality_for(matrix[:, col], duration)
            print(f"ERR: {str(exc)[:80]}")

    raw_df = pd.DataFrame(matrix, columns=services)
    filled_df = raw_df.ffill().bfill().fillna(0.0)
    filled_df.to_excel(os.path.join(out_dir, "rawdata.xlsx"), index=False)
    raw_df.to_csv(os.path.join(out_dir, "raw_prometheus.csv"), index=False)

    valid = all(q["valid_ratio"] >= min_valid_ratio for q in raw_quality.values())
    quality = {
        "collector": "collect_istio_latency.py",
        "namespace": namespace,
        "services": services,
        "duration_seconds": int(duration),
        "step": step,
        "rate_window": rate_window,
        "start_epoch": int(start),
        "end_epoch": int(end),
        "min_valid_ratio": min_valid_ratio,
        "valid": valid,
        "service_quality": raw_quality,
    }
    with open(os.path.join(out_dir, "quality.json"), "w", encoding="utf-8") as handle:
        json.dump(quality, handle, indent=2)

    print(f"  Saved ({filled_df.shape[0]}x{filled_df.shape[1]}) valid={valid}")
    return filled_df, quality


def parse_services(value):
    if not value:
        return SERVICES
    return [item.strip() for item in value.split(",") if item.strip()]


def main():
    parser = argparse.ArgumentParser(description="Collect Istio destination latency for SockShop")
    parser.add_argument("--output", "-o", default="data/sockshop_mesh/default")
    parser.add_argument("--duration", "-d", type=int, default=120)
    parser.add_argument("--namespace", default="sock-shop")
    parser.add_argument("--services", default=",".join(SERVICES))
    parser.add_argument("--step", default="1s")
    parser.add_argument("--rate-window", default="15s")
    parser.add_argument("--min-valid-ratio", type=float, default=0.95)
    args = parser.parse_args()

    collect(
        parse_services(args.services),
        args.duration,
        args.output,
        namespace=args.namespace,
        step=args.step,
        rate_window=args.rate_window,
        min_valid_ratio=args.min_valid_ratio,
    )


if __name__ == "__main__":
    main()
