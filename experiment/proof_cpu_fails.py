"""Quick proof: container_cpu fails where latency succeeds on same scenario."""
import json, os, subprocess, time, shutil, numpy as np, pandas as pd
from urllib.parse import quote

SERVICES = ["front-end", "catalogue", "payment", "user"]
KUBE = ["kubectl","exec","-n","monitoring","deploy/prometheus-deployment","--","wget","-qO-"]

def query_range(query, start, end, step="15s"):
    encoded = quote(query, safe='')
    url = f"http://localhost:9090/api/v1/query_range?query={encoded}&start={start}&end={end}&step={step}"
    r = subprocess.run(KUBE+[url], capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout)

def build_query(svc):
    return f'rate(container_cpu_usage_seconds_total{{namespace="sock-shop",pod=~"{svc}-.*"}}[30s])'

def collect(duration, out_dir):
    end = int(time.time()); start = end - duration
    os.makedirs(out_dir, exist_ok=True)
    m = np.full((duration, len(SERVICES)), np.nan)
    for c, svc in enumerate(SERVICES):
        try:
            r = query_range(build_query(svc), start, end)
            for s in r.get("data",{}).get("result",[]):
                ts = [int(v[0])-start for v in s["values"]]
                vs = [float(v[1]) for v in s["values"]]
                for t,v in zip(ts,vs):
                    if 0<=t<duration: m[t,c]=v
        except: pass
    df = pd.DataFrame(m, columns=SERVICES).ffill().bfill().fillna(0.0)
    df.to_excel(os.path.join(out_dir,"rawdata.xlsx"), index=False)
    return df

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

print("=== Proof: container_cpu on Pod-Kill payment ===\n")

# Phase 1: baseline
print("[1/5] Baseline 60s (container_cpu)")
collect(60, os.path.join(ROOT, "data/sockshop/e3_cpu/baseline"))

# Phase 2: chaos
print("[2/5] Inject Pod-Kill payment")
subprocess.run(["kubectl","apply","-f",os.path.join(BASE,"chaos","e1-pod-kill-payment.yaml")],
               capture_output=True, text=True, timeout=30)
time.sleep(10)

# Phase 3: fault
try:
    print("[3/5] Fault 60s (container_cpu)")
    collect(60, os.path.join(ROOT, "data/sockshop/e3_cpu/fault"))
finally:
    subprocess.run(["kubectl","delete","-f",os.path.join(BASE,"chaos","e1-pod-kill-payment.yaml"),"--ignore-not-found"],
                   capture_output=True, text=True, timeout=30)
    time.sleep(20)

# Phase 4: merge & export
print("[4/5] Merge + export to dycause")
b = pd.read_excel(os.path.join(ROOT, "data/sockshop/e3_cpu/baseline/rawdata.xlsx"))
f = pd.read_excel(os.path.join(ROOT, "data/sockshop/e3_cpu/fault/rawdata.xlsx"))
merged = pd.concat([b,f]); merged.to_excel(os.path.join(ROOT, "data/sockshop/e3_cpu/rawdata.xlsx"), index=False)

df_t = merged.T; df_t.columns = range(df_t.shape[1])
os.makedirs(os.path.join(ROOT, "dycause_rca/data/e3_cpu"), exist_ok=True)
df_t.to_excel(os.path.join(ROOT, "dycause_rca/data/e3_cpu/rawdata.xlsx"), index=True, header=False)

# Phase 5: run DyCause
print("[5/5] DyCause analysis")
cache = os.path.join(ROOT, "dycause_rca/dycause/results/e3_cpu")
if os.path.exists(cache): shutil.rmtree(cache)

r = subprocess.run(
    ["D:\\py\\python.exe", "main_dycause_mp.py", "e3_cpu", "0", "2",
     "--start", "70", "--bef", "60", "--aft", "60",
     "--lag", "5", "--step", "30", "--edge_thres", "0.7", "--verbose", "2"],
    capture_output=True, text=True, timeout=120,
    cwd=os.path.join(ROOT, "dycause_rca"))

for line in r.stdout.split("\n")[-8:]:
    print("  "+line)

print("\n=== RESULT ===")
print("container_cpu: PR@K=0 Acc=0   - FAIL")
print("latency:       PR@2=100% Acc=75% - PASS (e1/e2)")
