# DyCause on SockShop — 微服务根因分析复现

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-3776AB.svg)](https://www.python.org/)

在 [Sock Shop](https://microservices-demo.github.io/) 微服务系统上复现 ISSTA'21 论文 **"Faster, Deeper, Easier: Crowdsourcing Diagnosis of Microservice Kernel Failure from User Space"**。

**DyCause** 通过**滑动窗口 Granger 因果区间检验**发现服务间动态因果关系，构建依赖图，反向 BFS 搜索定位故障根因。

## 实验结果一览

| 实验 | 故障 | 根因 | PR@2 | PR@5 | Acc |
|------|------|------|------|------|-----|
| e1 | Pod-Kill payment | payment | **100%** | 100% | 75.00% |
| e2 | Pod-Kill user | user | **100%** | 100% | 75.00% |
| Pymicro 基准 | 延迟注入 | service 1 | 100% | 100% | 93.75% |

> 详细分析：[EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md)

## 环境要求

- Docker Desktop
- Minikube v1.38+
- kubectl、Helm 3
- Python 3.12 + `pandas numpy openpyxl matplotlib`

## 快速开始

### 1. 部署 SockShop 微服务系统

```bash
# 克隆 SockShop 部署清单
git clone https://github.com/microservices-demo/microservices-demo.git

# 启动 Minikube
minikube start --driver=docker

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
    - 'while true; do
        curl -so /dev/null http://front-end:80/;
        curl -so /dev/null http://front-end:80/category.html;
        curl -so /dev/null http://catalogue:80/catalogue;
        curl -so /dev/null -X POST http://payment:80/paymentAuth
          -H "Content-Type: application/json" -d "{\"amount\":1}";
        curl -so /dev/null http://user:80/customers;
        sleep 0.2;
      done'
  restartPolicy: Never
EOF
```

### 4. 运行实验

```bash
cd experiment
pip install pandas numpy openpyxl matplotlib

# 运行全部实验（约 22 分钟）
python run_experiments.py --run-all

# 或单个实验
python run_experiments.py --exp e1
```

### 5. 运行 DyCause 分析

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
```

## 项目结构

```
├── experiment/                # 实验脚本
│   ├── collect_latency.py     #   通过 kubectl exec 采集延迟指标
│   ├── run_experiments.py     #   实验编排器
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
├── dycause_rca/               # DyCause 源码（已打 Python 3.12 补丁）
├── scripts/                   # Minikube 启停脚本
├── README.md                  # 本文件
├── AGENTS.md                  # 技术细节
└── EXPERIMENT_REPORT.md       # 完整实验结果与分析
```

## 算法原理

4 个 Go 服务通过 Prometheus（1s 抓取）暴露 `request_duration_seconds` 延迟指标。ChaosMesh 注入 Pod-Kill 故障。DyCause 执行：

1. **Granger 因果检验** — 对每对服务 (i→j) 进行滑动窗口因果检验
2. **依赖图构建** — 自适应阈值筛选显著因果边
3. **反向 BFS 根因分析** — 从前端入口沿依赖图反向搜索根因路径

## 关键发现

**只有应用级请求延迟（`request_duration_seconds`）能产生有效的 Granger 因果信号。** 其他指标（容器CPU、网络流量、进程CPU、吞吐量）全部失败（见 `proof_cpu_fails.py`）。

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
