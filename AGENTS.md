# AGENTS

## Repo layout
- `microservices-demo/` — upstream Sock Shop microservices demo (deployment manifests, Helm chart, Docker Compose).
- `scripts/` — Minikube management helpers (start/stop/open Sock Shop).
- `experiment/` — DyCause reproduction: data collection, chaos injection, experiment runner, tests, analysis.
- `data/sockshop/` — collected metric datasets for DyCause (e1, e2).
- `data/sockshop_mesh_extended/` — generated Istio Service Mesh datasets for DyCause (7 HTTP service nodes), including the former `sockshop_mesh` data.
- `dycause_rca/` — DyCause source code (cloned from GitHub, patched for Python 3.12 compatibility).
- `ISSTA21-DyCause.pdf` — the paper being reproduced.
- `README.md` — deployment and code guide.
- `EXPERIMENT_REPORT_PAPER.md` — final paper-style experiment report.

## Minikube helper scripts (`scripts/`)
- `start-sockshop.ps1` — starts Minikube (Docker driver, default 4 CPU / 7GB RAM), updates context, scales sock-shop deployments to 1.
- `enable-istio.ps1` — installs Istio minimal/default profile with Prometheus metrics merging, enables sidecar injection for `sock-shop`, excludes non-experiment backing services, restarts deployments, verifies metrics.
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

## Istio Service Mesh enhancement
- Enable with `scripts/enable-istio.ps1` after SockShop and monitoring are deployed.
- Uses Istio sidecar mode and existing Prometheus; do not deploy a second Istio addon Prometheus for the main pipeline.
- Main metric: `istio_request_duration_milliseconds_sum/count` with `reporter="destination"`, converted from ms to seconds. Use a 15s rate window by default; 5s produced intermittent NaN on low-volume windows.
- Main 7 HTTP service nodes:

| Index | Service |
|-------|---------|
| 0 | front-end |
| 1 | catalogue |
| 2 | carts |
| 3 | orders |
| 4 | payment |
| 5 | shipping |
| 6 | user |

- DyCause root arguments for mesh runs use the IDs printed by DyCause (1-based service IDs), while the frontend entry remains `0`: catalogue=`2`, payment=`5`, user=`7`.
- DB/RabbitMQ are excluded from the main DyCause input because they primarily expose TCP metrics, not HTTP/API latency.
- Mesh DyCause default after formal mesh_e1 sensitivity: `--lag 7 --step 30 --edge_thres 0.8`.
- Mesh scripts:
  - `experiment/collect_istio_latency.py` — collects 7-service Istio latency, plus `raw_prometheus.csv` and `quality.json`.
  - `experiment/run_mesh_experiments.py` — runs `mesh_e1`..`mesh_e5`, exports to `dycause_rca/data/<exp>_mesh_runXX/rawdata.xlsx`, optionally runs DyCause and sensitivity analysis.
  - `experiment/chaos/mesh-e3-network-delay-payment.yaml`, `mesh-e4-network-delay-user.yaml`, `mesh-e5-network-delay-catalogue.yaml` — 300ms NetworkDelay scenarios.
- Quick pipeline check:
  ```bash
  cd experiment
  python collect_istio_latency.py --duration 120 --output ../data/sockshop_mesh_extended/quick_check
  python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --baseline 120 --fault 120 --no-wait
  ```

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
kubectl delete pod load-gen -n sock-shop --ignore-not-found
kubectl apply -f experiment/load-gen-business.yaml
kubectl wait pod/load-gen -n sock-shop --for=condition=Ready --timeout=120s
```

`experiment/load-gen-business.yaml` uses front-end pages and front-end API proxy routes as the main traffic path, plus a low-frequency direct coverage probe every 5 loops to keep all 7 mesh latency nodes populated.

Business-load mesh experiment data must be written to `data/sockshop_mesh_business/` with `--dataset-prefix business_ --load-profile business-front-proxy-v1`. Main/direct-service mesh data lives in `data/sockshop_mesh_extended/`; do not infer old/new from run numbers.

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
