"""
Collect request_duration_seconds latency from SockShop Go services via Prometheus.
4 services: front-end, catalogue, payment, user.
Queries: rate(sum[5s]) / rate(count[5s]) = average latency (sec).
"""
import argparse, json, subprocess, time, os
from urllib.parse import quote
import numpy as np
import pandas as pd
from datetime import datetime

SERVICES = ["front-end", "catalogue", "payment", "user"]

def kubectl_exec(url):
    r = subprocess.run(["kubectl","exec","-n","monitoring","deploy/prometheus-deployment","--","wget","-qO-",url],
                       capture_output=True, text=True, timeout=30)
    if r.returncode != 0: raise RuntimeError(r.stderr.strip())
    return r.stdout

def query_range(query, start, end, step="1s"):
    encoded = quote(query, safe='')
    url = f"http://localhost:9090/api/v1/query_range?query={encoded}&start={start}&end={end}&step={step}"
    return json.loads(kubectl_exec(url))

def build_query(svc):
    return (f'rate(request_duration_seconds_sum{{kubernetes_name="{svc}",'
            f'kubernetes_namespace="sock-shop"}}[5s]) / '
            f'rate(request_duration_seconds_count{{kubernetes_name="{svc}",'
            f'kubernetes_namespace="sock-shop"}}[5s])')

def collect(services, duration, out_dir):
    end = int(time.time())
    start = end - duration
    os.makedirs(out_dir, exist_ok=True)
    print(f"[{datetime.now()}] {len(services)} svc x {duration}s")
    m = np.full((duration, len(services)), np.nan)
    for c, svc in enumerate(services):
        print(f"  [{c+1}/{len(services)}] {svc:<14}", end=" ", flush=True)
        try:
            r = query_range(build_query(svc), start, end, "1s")
            vals = r.get("data",{}).get("result",[])
            if vals:
                for s in vals:
                    ts = [int(v[0])-start for v in s["values"]]
                    vs = [float(v[1]) for v in s["values"]]
                    for t,v in zip(ts,vs):
                        if 0<=t<duration and not np.isnan(v) and not np.isinf(v):
                            m[t,c]=v
                print(f"OK ({int(np.sum(~np.isnan(m[:,c])))}/{duration})")
            else: print("NO DATA")
        except Exception as e: print(f"ERR: {str(e)[:40]}")
    df = pd.DataFrame(m,columns=services).ffill().bfill().fillna(0.0)
    df.to_excel(os.path.join(out_dir,"rawdata.xlsx"), index=False)
    print(f"  Saved ({df.shape[0]}x{df.shape[1]})")
    return df

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output","-o",default="data/sockshop/default")
    p.add_argument("--duration","-d",type=int,default=600)
    args = p.parse_args()
    collect(SERVICES, args.duration, args.output)

if __name__=="__main__": main()
