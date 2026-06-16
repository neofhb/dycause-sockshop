# DyCause on SockShop — 微服务根因分析复现

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-3776AB.svg)](https://www.python.org/)

在 [Sock Shop](https://microservices-demo.github.io/) 微服务系统上复现 ISSTA'21 论文 **"Faster, Deeper, Easier: Crowdsourcing Diagnosis of Microservice Kernel Failure from User Space"**。

**DyCause** 通过**滑动窗口 Granger 因果区间检验**发现服务间动态因果关系，构建依赖图，反向 BFS 搜索定位故障根因。

## 实验结果一览

原始 4 节点 baseline reproduction 仍然保留：

| 数据集 | 故障 | 根因 | PR@2 | PR@5 | Acc |
|------|------|------|------|------|-----|
| SockShop 4-node e1 | Pod-Kill payment | payment | **100%** | 100% | 75.00% |
| SockShop 4-node e2 | Pod-Kill user | user | **100%** | 100% | 75.00% |
| Pymicro 基准 | 延迟注入 | service 1 | 100% | 100% | 93.75% |

当前 Istio 7 节点主线与候选筛选结果如下：

| 数据根 | 实验 | 根因 | 结果 |
|------|------|------|------|
| `sockshop_mesh_business` | `mesh_e1` | payment Pod-Kill | Top-2 |
| `sockshop_mesh_business` | `mesh_e3` | payment NetworkDelay | Top-2 |
| `sockshop_mesh_candidate` | `mesh_e6` | orders NetworkDelay | Rank 1 |
| `sockshop_mesh_candidate` | `mesh_e7` | carts NetworkDelay | Rank 1 |
| `sockshop_mesh_candidate` | `mesh_e9` | orders Pod-Kill | Rank 2 |

> 当前主线分析：[EXPERIMENT_REPORT_CURRENT.md](EXPERIMENT_REPORT_CURRENT.md)  
> 历史报告保留：[EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)

## 环境要求

- Docker Desktop
- Minikube v1.38+
- kubectl、Helm 3、istioctl（运行 Service Mesh 增强实验时需要）
- Python 3.12 + `pandas numpy openpyxl matplotlib`

## 快速开始

### 1. 部署 SockShop 微服务系统

```bash
# 克隆 SockShop 部署清单
git clone https://github.com/microservices-demo/microservices-demo.git

# 启动 Minikube
# Service Mesh 增强实验建议至少 4 CPU / 7GB 内存
minikube start --driver=docker --cpus=4 --memory=7168

# 创建命名空间并部署全部服务
kubectl create ns sock-shop
kubectl apply -f microservices-demo/deploy/kubernetes/manifests -n sock-shop

# 等待所有 Pod 就绪
kubectl wait --for=condition=Available deploy --all -n sock-shop --timeout=300s
kubectl get pods -n sock-shop
```

### 2. 部署监控 + 混沌工程

```bash
# Prometheus + Grafana（抓取间隔已改为 1s）
kubectl create -f microservices-demo/deploy/kubernetes/manifests-monitoring

# ChaosMesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-testing --create-namespace
```

### 3. 部署负载生成器

```bash
kubectl delete pod load-gen -n sock-shop --ignore-not-found
kubectl apply -f experiment/load-gen-business.yaml
kubectl wait pod/load-gen -n sock-shop --for=condition=Ready --timeout=120s
```

`load-gen-business.yaml` 以 front-end 页面和 front-end API proxy 路径为主，并每 5 轮执行一次低频 direct coverage probe，避免 7 个 mesh latency 节点因低流量缺样。

候选对象筛选实验使用 checkout 链路更重的负载：

```bash
kubectl delete pod load-gen -n sock-shop --ignore-not-found
kubectl apply -f experiment/load-gen-checkout.yaml
kubectl wait pod/load-gen -n sock-shop --for=condition=Ready --timeout=120s
```

`load-gen-checkout.yaml` 提高 carts、orders、shipping 的连续请求占比，用于筛选更适合 DyCause 的新实验对象。

### 4. 运行实验

```bash
cd experiment
pip install pandas numpy openpyxl matplotlib

# 运行全部实验（约 22 分钟）
python run_experiments.py --run-all

# 或单个实验
python run_experiments.py --exp e1
```

### 5. 运行 Service Mesh 增强实验

原始实验只使用 SockShop 中 4 个原生暴露 `request_duration_seconds` 的 Go 服务。为增加数据节点并更贴近 DyCause 的用户空间 API proxy 思想，可以启用 Istio sidecar mode，采集 7 个 HTTP 服务的 destination latency：

```text
front-end, catalogue, carts, orders, payment, shipping, user
```

启用 Istio：

```powershell
# 在仓库根目录运行
.\scripts\check-mesh-prereqs.ps1 -PythonExe D:\py\python.exe
.\scripts\enable-istio.ps1
```

如果刚通过 `winget install Istio.Istio` 安装，当前终端可能还没刷新 PATH，可把 `istioctl.exe` 完整路径传给 `-IstioctlExe`。

验证单次 120 秒采集：

```bash
cd experiment
python collect_istio_latency.py --duration 120 --output ../data/sockshop_mesh_business/smoke
```

Istio 采集默认使用 `--rate-window 15s`。在当前 SockShop 负载下，5s 窗口容易因为低流量窗口产生间歇性 `NaN`。

运行 mesh 实验：

```bash
# 单个场景，先跑 1 次冒烟；--no-wait 只验证管线，不代表正式实验采样语义
python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --baseline 120 --fault 120 --no-wait

# 当前 business 主线：payment 相关正式场景
python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --run-dycause
python run_mesh_experiments.py --exp mesh_e3 --repeat 1 --run-dycause

# 参数敏感性分析
python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --run-dycause --sensitivity

# 汇总 business 主线的 run
python summarize_mesh_results.py

# 当前 business 主线压缩批量方案
python run_compressed_mesh_batch.py

# 候选对象筛选：orders/carts/shipping，每个先跑 1 次
python run_compressed_mesh_batch.py \
  --plan mesh_e6=1,mesh_e7=1,mesh_e8=1,mesh_e9=1 \
  --data-root ../data/sockshop_mesh_candidate \
  --dataset-prefix candidate_ \
  --load-profile business-checkout-v2
```

输出位置：

```text
原始 4 节点 baseline reproduction:
  data/sockshop/

当前 7 节点 business-front-proxy 主线:
  data/sockshop_mesh_business/<exp>/runXX/
  dycause_rca/data/business_<exp>_mesh_runXX/rawdata.xlsx

候选 checkout load:
  data/sockshop_mesh_candidate/<exp>/runXX/
  dycause_rca/data/candidate_<exp>_mesh_runXX/rawdata.xlsx

历史 direct-service mesh 归档:
  data/archive/sockshop_mesh_legacy_direct_service/
```

当前主线默认参数为 `lag=5, step=30, edge_thres=0.8`，Istio 查询窗口为 `rate_window=15s`。`metadata.json` 会记录 `load_profile`、`data_root` 和 `dataset_prefix`；旧 direct-service mesh 数据已归档到 `data/archive/sockshop_mesh_legacy_direct_service/`。

候选实验编号从 `mesh_e6` 开始：`mesh_e6=orders delay`、`mesh_e7=carts delay`、`mesh_e8=shipping delay`、`mesh_e9=orders pod-kill`。当前 `mesh_e2/e4/e5` 保留为 user/catalogue 相关负例，不复用编号。

手动单跑新 load 数据示例：

```bash
python run_mesh_experiments.py --exp mesh_e3 --repeat 1 \
  --baseline 300 --fault 300 --run-dycause \
  --data-root ../data/sockshop_mesh_business \
  --dataset-prefix business_ \
  --load-profile business-front-proxy-v1
```

### 6. 运行 DyCause 分析

```bash
cd dycause_rca

# e1: Pod-Kill payment（根因索引=2）
python main_dycause_mp.py e1 0 2 \
  --start 315 --bef 300 --aft 300 \
  --lag 5 --step 30 --edge_thres 0.7 --verbose 2

# e2: Pod-Kill user（根因索引=3）
python main_dycause_mp.py e2 0 3 \
  --start 315 --bef 300 --aft 300 \
  --lag 5 --step 30 --edge_thres 0.7 --verbose 2

# Pymicro 论文基准对比
python main_dycause_mp.py pymicro 16 1 \
  --start 1200 --bef 100 --aft 0 \
  --lag 9 --step 30 --num_sel 1 \
  --edge_thres 0.8 --verbose 2 --mean arithmetic

# business 主线：mesh_e1 run01，payment Pod-Kill（DyCause 根因编号=5）
python main_dycause_mp.py business_mesh_e1_mesh_run01 0 5 \
  --start 315 --bef 300 --aft 300 \
  --lag 5 --step 30 --edge_thres 0.8 --verbose 2

# candidate 主线：mesh_e6 run01，orders NetworkDelay（DyCause 根因编号=4）
python main_dycause_mp.py candidate_mesh_e6_mesh_run01 0 4 \
  --start 315 --bef 300 --aft 300 \
  --lag 5 --step 30 --edge_thres 0.8 --verbose 2
```

## 项目结构

```
├── experiment/                # 实验脚本
│   ├── collect_latency.py     #   通过 kubectl exec 采集延迟指标
│   ├── collect_istio_latency.py #  采集 Istio destination latency（7 节点）
│   ├── run_experiments.py     #   实验编排器
│   ├── run_mesh_experiments.py #   Istio Service Mesh 实验编排器
│   ├── proof_cpu_fails.py     #   对照实验（容器CPU失败证明）
│   ├── generate_figures.py    #   生成统计图表
│   ├── analyze_data.py        #   数据统计分析
│   ├── selenium_test.py       #   Selenium 浏览器测试
│   ├── load_test.py           #   HTTP 并发负载测试
│   ├── sockshop-jmeter.jmx    #   JMeter 测试计划
│   ├── debug_query.py         #   PromQL 调试工具
│   └── chaos/                 #   ChaosMesh 故障定义
├── data/sockshop/             # 实验数据
│   ├── e1/                    #   Pod-Kill payment
│   └── e2/                    #   Pod-Kill user
├── data/sockshop_mesh_business/  # 当前 Istio 7 节点主线
├── data/sockshop_mesh_candidate/ # 候选对象筛选数据
├── data/archive/                # 历史 mesh 数据归档
├── dycause_rca/               # DyCause 源码（已打 Python 3.12 补丁）
├── scripts/                   # Minikube 启停脚本
├── README.md                  # 本文件
├── AGENTS.md                  # 技术细节
├── EXPERIMENT_REPORT_CURRENT.md # 当前主线结果与筛选结论
└── EXPERIMENT_REPORT.md       # 历史实验报告
```

## 算法原理

原始实验中，4 个 Go 服务通过 Prometheus（1s 抓取）暴露 `request_duration_seconds` 延迟指标。增强实验中，Istio sidecar 通过 `istio_request_duration_milliseconds` 暴露 7 个 HTTP 服务的 destination latency。当前 mesh 主线采用的 DyCause 参数为 `--lag 5 --step 30 --edge_thres 0.8`，这是 business-front-proxy 和 candidate 筛选中都表现稳定的组合。ChaosMesh 注入 Pod-Kill 或 NetworkDelay 故障。DyCause 执行：

1. **Granger 因果检验** — 对每对服务 (i→j) 进行滑动窗口因果检验
2. **依赖图构建** — 自适应阈值筛选显著因果边
3. **反向 BFS 根因分析** — 从前端入口沿依赖图反向搜索根因路径

## 关键发现

**只有请求级延迟指标能产生有效的 Granger 因果信号。** 原始实验使用应用自身的 `request_duration_seconds`，Service Mesh 增强实验使用 Istio 的 `istio_request_duration_milliseconds`。其他指标（容器CPU、网络流量、进程CPU、吞吐量）全部失败（见 `proof_cpu_fails.py`）。

DB、RabbitMQ 暂不放入主实验节点：它们主要产生 TCP 指标，和 DyCause 主实验所需的 HTTP/API 请求延迟口径不同，可作为后续扩展或对照分析。

## 注意事项

**Windows Docker 驱动下 `kubectl port-forward` 会卡死**，所有 Prometheus 查询改用集群内部执行：

```bash
kubectl exec -n monitoring deploy/prometheus-deployment -- wget -qO- "http://localhost:9090/api/v1/..."
```

## Python 3.12 兼容性

DyCause 原始代码针对 Python 3.7 + numpy 1.17。本仓库已修复三处不兼容：

| 文件 | 修改 |
|------|------|
| `causal_graph_build.py:25` | `np.int` → `int` |
| `main_dycause_mp.py:402` | `sum(arr)` → `arr.sum()` |
| `main_dycause_mp.py:346` | 增加 `None` 守卫处理 Granger 失败 |

## 许可证

本项目包含来自 [PanYicheng/dycause_rca](https://github.com/PanYicheng/dycause_rca) 的代码，遵循 Apache 2.0 许可证。

## 参考文献

> Yicheng Pan, Meng Ma, Xinrui Jiang, and Ping Wang. 2021. *Faster, Deeper, Easier: Crowdsourcing Diagnosis of Microservice Kernel Failure from User Space*. ISSTA '21, ACM. [DOI: 10.1145/3460319.3464805](https://doi.org/10.1145/3460319.3464805)
