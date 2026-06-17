# DyCause on SockShop

SockShop 微服务系统上的 DyCause 根因定位复现实验。项目包含原始 4 服务 baseline、Istio 7 服务扩展数据、ChaosMesh 故障注入脚本、DyCause 调试/对比脚本，以及最终论文式实验报告。

最终报告：[EXPERIMENT_REPORT_PAPER.md](EXPERIMENT_REPORT_PAPER.md)

## 核心结论

- 当前主线数据集：`data/sockshop_mesh_extended/`
- 当前主参数：`lag=7`、`step=30`、`edge_thres=0.8`、`rate_window=15s`
- 当前有效 run：87/87
- 原始 DyCause 在全部有效 run 上：Top-1 13.8%，Top-2 21.8%，Top-5 35.6%，Acc 0.310
- 对比实验显示：SockShop Extended 上 Pearson 和 z-shift 强于原始 DyCause；但 `pymicro` 上 path/backtrace 机制仍然有效
- 关键解释：SockShop 中 path candidate 稀疏，root 只有 42/87 个 case 出现在 top paths，39/87 个 case 有非零 path score

## 快速运行

启动 SockShop：

```powershell
.\scripts\start-sockshop.ps1
```

启用 Istio：

```powershell
.\scripts\enable-istio.ps1
```

部署负载生成器：

```bash
kubectl delete pod load-gen -n sock-shop --ignore-not-found
kubectl apply -f experiment/load-gen-legacy-compressed.yaml
kubectl wait pod/load-gen -n sock-shop --for=condition=Ready --timeout=120s
```

采集一次 Istio latency：

```bash
cd experiment
python collect_istio_latency.py --duration 120 --output ../data/sockshop_mesh_extended/quick_check
```

运行 mesh 实验：

```bash
cd experiment
python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --baseline 300 --fault 300 --run-dycause
```

生成当前论文报告图表：

```bash
python experiment/generate_paper_report_figures.py
```

## 目录结构

```text
microservices-demo/              upstream Sock Shop deployment files
scripts/                         Minikube and Istio helper scripts
experiment/                      data collection, chaos, runners, analysis
experiment/figures/paper_report/ report figures
data/sockshop/                   original 4-service SockShop datasets
data/sockshop_mesh_extended/     current 7-service Istio mesh datasets
data/baseline_comparison/        baseline comparison summaries
debug_results*/                  DyCause scoring and path debug outputs
dycause_rca/                     patched DyCause source
EXPERIMENT_REPORT_PAPER.md       final paper-style experiment report
```

## Notes

- Windows Docker driver 下不要使用 `kubectl port-forward` 查询 Prometheus；使用 `kubectl exec` 从集群内部访问 Prometheus API。
- `external/` 是本地外部仓库目录，已加入 `.gitignore`，不提交。
- 旧的过程报告已删除，最终结论以 `EXPERIMENT_REPORT_PAPER.md` 为准。
