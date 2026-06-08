import json, subprocess, time
from urllib.parse import quote

query = 'rate(request_duration_seconds_sum{kubernetes_name="front-end",kubernetes_namespace="sock-shop"}[5s])'
encoded = quote(query, safe='')
end = int(time.time())
start = end - 120  

url = f"http://localhost:9090/api/v1/query_range?query={encoded}&start={start}&end={end}&step=15s"
print("Start:", start, "End:", end)

cmd = ["kubectl","exec","-n","monitoring","deploy/prometheus-deployment","--","wget","-qO-",url]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print("Return:", r.returncode)
if r.returncode == 0:
    d = json.loads(r.stdout)
    print("Status:", d.get("status"))
    results = d.get("data", {}).get("result", [])
    print("Result count:", len(results))
    if results:
        vals = results[0]["values"]
        print("Points:", len(vals), "Sample:", vals[:3])
else:
    print("Stderr:", r.stderr[:300])
