"""
Simple HTTP load test for SockShop (alternative to JMeter for quick testing).
Generates CSV results compatible with JMeter format.

Usage:
  python load_test.py --url http://localhost:30001 --users 50 --duration 60
"""

import argparse
import csv
import os
import random
import signal
import subprocess
import statistics
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


SOCKSHOP_ENDPOINTS = [
    {"method": "GET", "path": "/", "name": "Homepage"},
    {"method": "GET", "path": "/category.html", "name": "Category"},
    {"method": "GET", "path": "/detail.html?id=3395a43e-2d88-40de-b95f-e00e1502085b", "name": "Product-Detail"},
    {"method": "GET", "path": "/catalogue", "name": "Catalogue-API"},
    {"method": "GET", "path": "/basket.html", "name": "Shopping-Cart"},
]


class LoadTestResult:
    def __init__(self):
        self.lock = threading.Lock()
        self.results = []
    
    def add(self, timestamp, endpoint, elapsed, status, success):
        with self.lock:
            self.results.append({
                "timeStamp": int(timestamp * 1000),
                "label": endpoint["name"],
                "elapsed": int(elapsed * 1000),
                "responseCode": status,
                "success": "true" if success else "false",
                "threadName": str(threading.current_thread().name),
            })

    
    def save_csv(self, path):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timeStamp", "label", "elapsed", "responseCode", "success", "threadName"])
            writer.writeheader()
            writer.writerows(self.results)
    
    def summary(self):
        labels = {}
        for r in self.results:
            lb = r["label"]
            if lb not in labels:
                labels[lb] = []
            labels[lb].append(r["elapsed"])
        
        print("\n" + "=" * 80)
        print(f"{'Endpoint':<20} {'Count':>8} {'Avg(ms)':>10} {'Min(ms)':>10} {'Max(ms)':>10} {'Err%':>8}")
        print("-" * 80)
        total_count = 0
        total_errors = 0
        for name, times in sorted(labels.items()):
            errors = sum(1 for r in self.results if r["label"] == name and r["success"] == "false")
            total_count += len(times)
            total_errors += errors
            print(f"{name:<20} {len(times):>8} {statistics.mean(times):>10.1f} {min(times):>10.1f} {max(times):>10.1f} {errors/len(times)*100:>7.1f}%")
        print("-" * 80)
        all_times = [r["elapsed"] for r in self.results]
        print(f"{'TOTAL':<20} {total_count:>8} {statistics.mean(all_times):>10.1f} {min(all_times):>10.1f} {max(all_times):>10.1f} {total_errors/total_count*100:>7.1f}%")
        throughput = total_count / max(1, max(r["elapsed"] for r in self.results) / 1000) if all_times else 0
        print(f"{'Throughput':<20} {'':>8} {throughput:>10.1f} req/s")
        print("=" * 80)


def worker(base_url, endpoints, duration, result):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
        "Accept": "text/html,application/json,*/*",
    })
    
    start = time.time()
    while time.time() - start < duration:
        ep = random.choice(endpoints)
        url = base_url.rstrip("/") + ep["path"]
        t0 = time.time()
        try:
            if ep["method"] == "GET":
                r = session.get(url, timeout=10, allow_redirects=True)
            else:
                r = session.post(url, timeout=10)
            elapsed = time.time() - t0
            result.add(time.time(), ep, elapsed, r.status_code, r.ok)
        except Exception as e:
            elapsed = time.time() - t0
            result.add(time.time(), ep, 0, str(e)[:50], False)
        
        time.sleep(random.uniform(0.1, 0.5))


def run_load_test(base_url, num_users, duration):
    print("=" * 60)
    print(f"  SockShop Load Test")
    print(f"  URL:      {base_url}")
    print(f"  Users:    {num_users}")
    print(f"  Duration: {duration}s")
    print("=" * 60)
    
    result = LoadTestResult()
    
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(worker, base_url, SOCKSHOP_ENDPOINTS, duration, result)
                   for _ in range(num_users)]
        
        # Progress indicator
        start = time.time()
        while time.time() - start < duration:
            time.sleep(2)
            elapsed = time.time() - start
            with result.lock:
                count = len(result.results)
            print(f"  [{elapsed:>5.0f}s] Requests: {count}", end="\r")
        
        for f in as_completed(futures, timeout=10):
            f.result()
    
    print("\n")
    return result


def start_port_forward(port=30001):
    proc = subprocess.Popen(
        ["kubectl", "port-forward", "-n", "sock-shop", "svc/front-end", f"{port}:80"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
    time.sleep(3)
    return proc


def stop_port_forward(proc):
    if proc:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    parser = argparse.ArgumentParser(description="SockShop HTTP load test")
    parser.add_argument("--url", default="http://localhost:30001", help="Front-end URL")
    parser.add_argument("--users", "-u", type=int, default=10, help="Concurrent users")
    parser.add_argument("--duration", "-d", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--output", "-o", default=None, help="CSV output path")
    parser.add_argument("--no-pf", action="store_true", help="Skip starting kubectl port-forward")
    args = parser.parse_args()
    
    pf_proc = None
    if not args.no_pf:
        print("Starting kubectl port-forward (svc/front-end -> :30001)...")
        pf_proc = start_port_forward(30001)
    
    try:
        result = run_load_test(args.url, args.users, args.duration)
        result.summary()
        if args.output:
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            result.save_csv(args.output)
            print(f"\n  Results saved to {args.output}")
    finally:
        if pf_proc:
            stop_port_forward(pf_proc)
            print("Port-forward stopped.")


if __name__ == "__main__":
    main()
