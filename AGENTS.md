# AGENTS

## Repo layout
- `microservices-demo/` — upstream Sock Shop microservices demo (deployment manifests, Helm chart, Docker Compose).
- `scripts/` — Minikube management helpers (start/stop/open Sock Shop).
- `experiment/` — DyCause reproduction: data collection, chaos injection, experiment runner, tests, analysis.
- `data/sockshop/` — collected metric datasets for DyCause (e1, e2).
- `dycause_rca/` — DyCause source code (cloned from GitHub, patched for Python 3.12 compatibility).
- `ISSTA21-DyCause.pdf` — the paper being reproduced.
- `README.md` — deployment and code guide.
- `EXPERIMENT_REPORT.md` — results analysis and charts.

## Minikube helper scripts (`scripts/`)
- `start-sockshop.ps1` — starts Minikube (Docker driver), updates context, scales sock-shop deployments to 1.
- `stop-sockshop.ps1 -Soft` — scales all deployments to 0; without `-Soft` stops Minikube.
- `open-sockshop.ps1` — runs `minikube service front-end -n sock-shop --url`. Window must stay open.
- `.cmd` wrappers are convenience launchers for PowerShell.

## Kubernetes manifests
- Source: `microservices-demo/deploy/kubernetes/manifests/`.
- To deploy: `kubectl apply -f microservices-demo/deploy/kubernetes/manifests -n sock-shop`.

## Monitoring (Prometheus/Grafana)
- Manifests: `microservices-demo/deploy/kubernetes/manifests-monitoring/`.
- Apply in order: namespace (00) → Prometheus (01–10, 24–26) → Grafana (20–22) → import dashboards (23).
- NodePorts: Grafana `31300`, Prometheus `31090`.
- **Prometheus scrape interval**: Changed to `1s` in `04-prometheus-configmap.yaml` for optimal DyCause data density.
- Access Prometheus API from within cluster: `kubectl exec -n monitoring deploy/prometheus-deployment -- wget -qO- "http://localhost:9090/api/v1/..."`.
- **Do NOT use `kubectl port-forward`** — it hangs on Windows Docker driver. Use `kubectl exec` instead.

## ChaosMesh
- Installed via Helm in `chaos-testing` namespace: `chaos-mesh/chaos-mesh`.
- Chaos experiment YAMLs: `experiment/chaos/`.
- Dashboard: `kubectl port-forward -n chaos-testing svc/chaos-dashboard 2333:2333` (not needed for experiments).

## DyCause experiment pipeline

### Key finding
Only **request_duration_seconds latency** on Go services produces valid Granger causality signals.
Other metrics (container CPU, network, process CPU, throughput) did not work on SockShop.

### Service selection
4 Go services with latency metrics:

| Index | Service | PromQL |
|-------|---------|--------|
| 0 | front-end | `rate(request_duration_seconds_sum[5s]) / rate(request_duration_seconds_count[5s])` |
| 1 | catalogue | same |
| 2 | payment | same |
| 3 | user | same |

### Scripts (`experiment/`)
- `collect_latency.py` — queries Prometheus via kubectl exec, collects 4-service latency at 1s intervals.
- `run_experiments.py` — orchestrates full experiment: collect baseline → inject chaos → collect fault → merge → export to dycause_rca.
- `proof_cpu_fails.py` — quick proof: container_cpu on same payment Pod-Kill → PR@K=0, proving only latency works.
- `selenium_test.py` — Selenium automated front-end test.
- `load_test.py` — HTTP concurrent load test (JMeter alternative).
- `sockshop-jmeter.jmx` — JMeter performance test plan.
- `debug_query.py` — PromQL debugging tool.
- `analyze_data.py` — detailed baseline vs fault data analysis (means, std, correlations).

### Run an experiment
```bash
cd experiment
python run_experiments.py --run-all              # run all (e1, e2)
python run_experiments.py --exp e1               # single experiment
```

### Deploy load generator (required for traffic)
```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata: {name: load-gen, namespace: sock-shop}
spec:
  containers:
  - name: load
    image: curlimages/curl:8.6.0
    command: ["sh","-c"]
    args:
    - 'while true; do curl -so /dev/null http://front-end:80/; curl -so /dev/null http://front-end:80/category.html; curl -so /dev/null http://catalogue:80/catalogue; curl -so /dev/null -X POST http://payment:80/paymentAuth -H "Content-Type: application/json" -d "{\"amount\":1}"; curl -so /dev/null http://user:80/customers; sleep 0.2; done'
  restartPolicy: Never
EOF
```

### Experiments

| ID | Fault | Root Cause | DyCause Result |
|----|-------|------------|----------------|
| **e1** | Pod-Kill payment | payment (idx=2) | PR@2=100% Acc=75% |
| **e2** | Pod-Kill user | user (idx=3) | PR@2=100% Acc=75% |
| proof | Pod-Kill payment (container_cpu) | payment (idx=2) | PR@K=0 Acc=0 |

DyCause run command:
```bash
cd dycause_rca
python main_dycause_mp.py e1 0 2 --start 315 --bef 300 --aft 300 --lag 5 --step 30 --edge_thres 0.7 --verbose 2
python main_dycause_mp.py e2 0 3 --start 315 --bef 300 --aft 300 --lag 5 --step 30 --edge_thres 0.7 --verbose 2
```

## DyCause baseline comparison (Pymicro)

Pymicro is a 16-service simulated dataset included in DyCause. It uses latency metrics and achieves paper-level results:

| Dataset | Services | Metric | PR@2 | PR@5 | Acc |
|---------|:--:|------|------|------|------|
| Pymicro | 16 | latency | 100% | 100% | 93.75% |
| SockShop e1 | 4 | latency | 100% | 100% | 75.00% |
| SockShop e2 | 4 | latency | 100% | 100% | 75.00% |

Pymicro run command:
```bash
cd dycause_rca
python main_dycause_mp.py pymicro 16 1 --start 1200 --bef 100 --aft 0 --lag 9 --step 30 --num_sel 1 --edge_thres 0.8 --verbose 2 --mean arithmetic
```

## DyCause source code patches
- `main_dycause_mp.py:346` — added `None` guard for failed Granger pairs
- `dycause_lib/causal_graph_build.py:25` — `np.int` → `int` (numpy 2.x compatibility)
- `main_dycause_mp.py:402` — `sum(overlay_counts)` → `overlay_counts.sum()` (numpy 2.x compatibility)
- `main_dycause.py:352` — same fix for single-process version

## Git conventions
- Use normal `git push` (NOT `--force`). This preserves commit history.
- Use incremental commits for changes; do not squash or amend published history.
- Repository: `https://github.com/neofhb/dycause-sockshop`
- If push fails with HTTP 502, retry with token in URL:
  ```bash
  git remote set-url origin https://oauth2:<token>@github.com/neofhb/dycause-sockshop.git
  git push
  git remote set-url origin https://github.com/neofhb/dycause-sockshop.git
  ```
