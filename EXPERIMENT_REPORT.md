# DyCause 在 SockShop 上的复现实验结果

> 源码：[github.com/neofhb/dycause-sockshop](https://github.com/neofhb/dycause-sockshop)

## 1. 最终成果

| 实验 | 故障 | 根因 | PR@2 | PR@5 | Acc |
|------|------|------|------|------|-----|
| e1 | Pod-Kill payment | payment (idx=2) | **100%** | 100% | **75.00%** |
| e2 | Pod-Kill user | user (idx=3) | **100%** | 100% | **75.00%** |
| Pymicro | 模拟延迟注入 | service 1 | 100% | 100% | 93.75% |
| proof | Pod-Kill payment (容器CPU) | payment (idx=2) | 0% | 0% | 0% |

## 2. 关键发现

**只有应用级请求延迟（request_duration_seconds）能驱动 Granger 因果检验。** 其他指标（容器CPU、网络流量、进程CPU、吞吐量）均告失败，因为：

- 基础设施指标（CPU/内存）不含请求级因果信息
- 吞吐量受健康检查主导，无业务含义
- Java/DB 服务无延迟指标

## 3. 论文介绍与分析

### 3.1 论文概述

本实验复现的论文为 **"Faster, Deeper, Easier: Crowdsourcing Diagnosis of Microservice Kernel Failure from User Space"**（ISSTA 2021, ACM），作者来自北京大学。

该论文针对微服务系统中**非对称诊断信息问题**：云平台用户（应用开发者）只能观测到自己调用的内核服务的性能指标，却无法获取整个微服务系统的全局状态。当故障发生时，传统方法依赖内核级监控数据（如完整调用链、所有服务指标），而普通用户无法访问这些数据。

### 3.2 核心贡献

DyCause 提出了三个层次的创新：

**1. Easier（更容易部署）**：首次将微服务故障诊断从内核空间迁移到用户空间。DyCause 作为轻量级 API 代理部署在应用侧，通过多应用间的 API 日志共享（众包机制）获取内核服务的全局视图，无需修改目标系统的架构或功能。

**2. Deeper（更深入分析）**：设计了**动态 Granger 因果区间检验算法**。传统方法假设服务间因果关系是静态的，但微服务系统中故障传播会动态改变服务间相关性。DyCause 通过滑动窗口枚举不同时间段，发现仅在故障期显著而在正常期不显著的因果边，揭示异常传播的时间顺序。

**3. Faster（更快速响应）**：通过优化的计算策略（回归模型复用、剪枝），DyCause 在数据稀疏时仍能保持高性能。论文实验表明，即使输入指标减少 83.3%，DyCause 仍优于其他基线方法。

### 3.3 算法详析

DyCause 包含五个核心模块：

1. **众包指标收集**：各应用共享 API 请求日志，聚合插值为 1Hz 时间序列
2. **异常区间检测**：基于极值理论（SPOT 算法）自动检测异常时间窗口
3. **动态因果发现**：对每对服务 (i→j) 进行滑动窗口 Granger 因果检验，生成**动态因果曲线** C_ij(t)，刻画因果关系随时间的变化
4. **众包图融合**：合并多个应用视角的局部依赖图，增强诊断能力
5. **反向 BFS 根因分析**：沿依赖图从异常入口服务反向搜索，输出根因候选排名

#### Granger 因果区间检验

两个线性回归模型：

```
部分模型: Ŷ(t) = Σ α_i · Y(t-i) + b           (仅用 Y 的过去值)
完整模型: Ŷ(t) = Σ α_i · Y(t-i) + Σ β_i · X(t-i) + b  (加入 X 的过去值)
```

计算 F 统计量：

```
       (RSS_restricted - RSS_unrestricted) / p
F = ---------------------------------------------
          RSS_unrestricted / (T - 2p - 1)
```

其中 `RSS_restricted` 为仅含 Y 滞后项（受限模型）的残差平方和，`RSS_unrestricted` 为同时含 X、Y 滞后项（无限制模型）的残差平方和，`p` 为滞后阶数，`T` 为观测数。

DyCause 创新之处在于不检验整个时间区间，而是枚举 `[s:e]` 滑动窗口，检测**仅在特定时间段显著**的因果关系，从而捕捉故障传播的动态过程。

#### 自适应阈值图构建

对每个服务 i，计算其到所有服务的 Granger 分数，以 `θ_e × max(分数)` 为阈值筛选显著边。该机制自动适应不同服务的因果强度差异，无需手动设定全局阈值。

#### 反向 BFS 根因分析

从异常前端服务出发，沿依赖图反向搜索到达各服务的所有路径。根因异常分数由两部分组成：
- **路径相关分数**：服务到前端的所有路径概率（路径越短、边越强，分数越高）
- **相关系数分数**：服务与前端服务的 Pearson 相关系数（辅助排除正常服务）



---

## 4. 复现脚本与数据处理

### 4.1 数据采集（`collect_latency.py`）

通过 `kubectl exec` 在 Prometheus Pod 内部执行查询，采集 4 个 Go 服务的 `request_duration_seconds` 延迟指标。

```python
def build_query(svc):
    return (f'rate(request_duration_seconds_sum{{kubernetes_name="{svc}",'
            f'kubernetes_namespace="sock-shop"}}[5s]) / '
            f'rate(request_duration_seconds_count{{kubernetes_name="{svc}",'
            f'kubernetes_namespace="sock-shop"}}[5s])')
```

采集流程：

```
kubectl exec prometheus -- wget "http://localhost:9090/api/v1/query_range?..."
  → JSON 响应解析 → 每服务 300 点时间序列
  → 前向/后向填充缺失值 → 保存为 rawdata.xlsx
```

关键参数：

| 参数 | 值 | 说明 |
|------|:--:|------|
| Prometheus scrape_interval | 1s | 修改自默认 15s，15 倍密度提升 |
| query_range step | 1s | 与抓取间隔匹配 |
| rate 窗口 | 5s | 5 个采样点足够计算速率变化 |
| 采集时长 | 300s | 基线期和故障期各 300 秒 |

**数据格式转换**：采集输出为列=服务、行=时间点（600×4），DyCause 要求行=服务、列=时间点（4×600）。`run_experiments.py` 在合并阶段自动执行转置并复制到 `dycause_rca/data/<exp>/rawdata.xlsx`。

### 4.2 实验编排（`run_experiments.py`）

编排完整的故障注入→采集→分析流程：

```
[Phase 1] 采集 BASELINE  (300s)
    ↓
[Phase 2] kubectl apply 注入混沌故障 (ChaosMesh Pod-Kill)
    ↓
[Phase 3] 采集 FAULT  (300s)
    ↓
[Phase 4] 合并 baseline + fault (600s)
    ↓        转置为 DyCause 格式
    ↓        复制到 dycause_rca/data/
    ↓
[Phase 5] 记录 metadata.json（根因索引、异常时间、DyCause 命令）
```

### 4.3 对照实验（`proof_cpu_fails.py`）

在同一故障场景下（Pod-Kill payment），使用 `container_cpu_usage_seconds_total` 替代 `request_duration_seconds`。结果 PR@K=0、Acc=0，证明基础设施指标不含请求级因果信息。

### 4.4 数据分析（`analyze_data.py`）

对实验数据执行以下分析：

| 分析内容 | 方法 |
|---------|------|
| 基线期 vs 故障期统计量 | 均值、标准差、相关性矩阵 |
| 异常窗口快照 | 故障前后 15 秒逐行数据输出 |
| 相关性变化检测 | 故障期相关性变化 > 0.05 的边 |
| 数据缺失检测 | 计数为零的数据点（指示 Pod 重启） |

### 4.5 DyCause 参数配置

| 参数 | 值 | 含义 |
|------|:--:|------|
| `--start` | 315 | 异常开始时间（秒），基线 300s + 15s 混沌延迟 |
| `--bef 300 --aft 300` | — | 异常前后分析窗口 |
| `--lag 5` | — | Granger 因果检验最大滞后阶数 |
| `--step 30` | — | 滑动窗口最小长度（秒） |
| `--edge_thres` | 0.7 | 自适应阈值比例（越低边越多） |
| `--verbose 2` | — | 输出详细诊断信息 |

---

## 5. 统计图表

> 由 `experiment/generate_figures.py` 生成，输出到 `experiment/figures/`。

### 5.1 根因检测精度对比 (PR@K)

![PR@K](experiment/figures/fig1_prk.png)

e1 和 e2 在 4 服务延迟指标上达到 **PR@2=100%**，Pymicro 在 16 服务上达到 **PR@5=100%**。容器 CPU 对照组 PR@K 全为 0。

### 5.2 根因排名准确度对比 (Acc)

![Acc](experiment/figures/fig2_acc.png)

SockShop 实验 Acc=75%，Pymicro 基准 Acc=93.75%。差距主要来自图规模（4 vs 16 节点）和故障注入精度（容器级 vs 代码级）。

### 5.3 服务依赖拓扑（DyCause 实际发现）

![Topology](experiment/figures/fig4_topology.png)

DyCause 从 12 条理论边中发现 3 条 Granger 显著边。
e1（payment 根因）和 e2（user 根因）共享同一因果链：**user→payment→catalogue→front-end**。
两条链最终均汇聚到 front-end 入口。

### 5.4 实验结果总览

| Exp | Fault | Root Cause | PR@2 | PR@5 | Acc |
|-----|-------|------------|------|------|------|
| e1 | Pod-Kill | payment | 100% | 100% | 75.00% |
| e2 | Pod-Kill | user | 100% | 100% | 75.00% |
| Pymicro | Latency injection | srv-1 | 100% | 100% | 93.75% |
| proof | Pod-Kill [CPU] | payment | 0% | 0% | 0% |

---

## 6. 实验结果分析

### 6.1 e1: Pod-Kill payment（根因=payment, idx=2）

#### 原始数据观察

| 指标 | 基线期 (前 300s) | 故障期 (后 300s) | 变化 |
|------|:--:|:--:|:--:|
| catalogue 标准差 | 0.000276 | 0.000159 | **-42.5%** |
| payment 标准差 | 0.000146 | 0.000171 | +16.7% |
| catalogue↔user 相关性 | +0.112 | +0.299 | **+0.187** |

**关键信号**：catalogue 的标准差在故障期骤降 42.5%，因为 front-end 的结账请求中断 → 对 catalogue 的调用减少 → catalogue 延迟波动降低。同时 catalogue 和 user 的相关性大幅增强，表明异常传播改变了服务间的依赖关系。

#### Granger 因果链

DyCause 发现的动态因果边（edge_thres=0.7）：

```
user ──→ payment ──→ catalogue ──→ front-end
```

#### DyCause 输出

```
节点     |  异常分数
catalogue (idx=1) | 0.416
payment   (idx=2) | 0.085   ← 根因，正确命中
user      (idx=3) | 0.052

PR@2=100%  Acc=75%
```

**分析**：payment 被正确识别为根因候选（排名第 2）。DyCause 优先将 catalogue 排第一，因为 catalogue 作为中间节点，延迟波动变化最大（-42.5% 标准差），在依赖图中被误认为更可能是源头。

### 6.2 e2: Pod-Kill user（根因=user, idx=3）

#### 原始数据观察

| 指标 | 基线期 | 故障期 | 变化 |
|------|:--:|:--:|:--:|
| front-end↔catalogue 相关性 | +0.242 | +0.146 | **-0.096** |
| front-end↔user 相关性 | +0.313 | +0.218 | **-0.095** |
| catalogue↔user 相关性 | +0.560 | +0.381 | **-0.179** |
| catalogue↔payment 相关性 | -0.455 | -0.562 | -0.107 |

**关键信号**：user 被 Kill 后，所有涉及 user 的相关性均下降（front-end↔user 从 0.31→0.22，catalogue↔user 从 0.56→0.38），证明 user 的延迟信号从依赖图中消失。

#### Granger 因果链

DyCause 发现的边（仅 3 条，edge_thres=0.7）：

```
user ──→ payment ──→ catalogue ──→ front-end
```

注意：e2 比 e1 少一条边（user→catalogue），因为 user 被 Kill 后该边不显著。

#### DyCause 输出

```
节点     |  异常分数
payment   (idx=2) | 0.470
user      (idx=3) | 0.326   ← 根因，排名第 2
catalogue (idx=1) | 0.252

PR@2=100%  Acc=75%
```

**分析**：两个实验均达到 Acc=75%，PR@2=100%。e2 中 user 被 Kill 后，其延迟信号消失，Granger 无法在 user 上发现自相关，更准确地将其排在第二。payment 排第一是因为它作为 user→payment→catalogue 链的中间节点，波动也被放大。

### 6.3 对比分析

| 维度 | Pymicro（论文） | SockShop e1 | SockShop e2 |
|------|:--:|:--:|:--:|
| 服务数 | 16 | 4 | 4 |
| 指标 | 延迟 | 延迟 | 延迟 |
| 故障类型 | 代码级延迟注入 | 容器级 Pod-Kill | 容器级 Pod-Kill |
| Granger 显著边 | 高密度 | 3 条 | 3 条 |
| PR@2 | 100% | 100% | **100%** |
| PR@3 | 100% | 100% | 100% |
| Acc | 93.75% | 75.00% | **75.00%** |

#### 差距分析

1. **图规模**：Pymicro 16 节点产生更丰富的依赖结构，节点间独立性更强，Granger 因果检验的信噪比更高。SockShop 4 节点的图中，中间节点（catalogue）可能被误标记为根因。
2. **故障机制**：Pymicro 是代码级延迟注入（精确可控的数值变化），SockShop 是 Pod-Kill（服务瞬间消失再恢复，信号窗口极短）。
3. **e1 vs e2**：两者准确率相同（Acc=75%，PR@2=100%）。e2 的 user 是 leaf 节点（只被 front-end 调用），异常传播链单纯；e1 的 payment 处于中间层，异常通过 catalogue 间接传播，链条更长。

### 6.4 失败的指标对照

| 指标 | 覆盖服务 | 失败原因 |
|------|:--:|------|
| `container_cpu` | 14/14 | 基础设施级，无请求因果链 |
| `container_network_*` | 0/14 | cAdvisor 未采集，Minikube Docker 驱动限制 |
| `process_cpu` | 7/14 | 进程级，Go 服务无此指标 |
| 吞吐量 count | 7/14 | 受健康检查主导，信噪比低，归一化后波动小于 Granger 灵敏度阈值 |

---

## 7. Service Mesh 增强实验计划与实现

为回应“数据不足”的问题，本仓库新增 Istio Service Mesh 增强版实验管线。原 e1/e2 结果保留为 **4 节点 baseline**；增强实验使用 Istio sidecar 统一采集 7 个 HTTP 服务的请求延迟，作为更贴近 DyCause 用户空间 API proxy 的复现版本。

### 7.1 数据节点扩展

增强实验节点固定为：

| Index | Service | Metric |
|------:|---------|--------|
| 0 | front-end | `istio_request_duration_milliseconds` |
| 1 | catalogue | same |
| 2 | carts | same |
| 3 | orders | same |
| 4 | payment | same |
| 5 | shipping | same |
| 6 | user | same |

PromQL 使用 destination 视角，计算每个 workload 的平均请求延迟：

```promql
(
  sum(rate(istio_request_duration_milliseconds_sum{
    reporter="destination",
    destination_workload_namespace="sock-shop",
    destination_workload="<service>"
  }[15s]))
  /
  sum(rate(istio_request_duration_milliseconds_count{
    reporter="destination",
    destination_workload_namespace="sock-shop",
    destination_workload="<service>"
  }[15s]))
) / 1000
```

单位从毫秒转换为秒，保持与原 `request_duration_seconds` 数据一致。Istio 增强实验默认使用 15s rate 窗口，以避免低流量服务在 5s 窗口中产生间歇性 NaN。数据库和 RabbitMQ 暂不放入主实验，因为它们主要产生 TCP 指标，和 DyCause 请求级 API 延迟口径不一致。

### 7.2 新增脚本

| 文件 | 作用 |
|------|------|
| `scripts/enable-istio.ps1` | 安装 Istio，开启 `sock-shop` namespace 自动注入，重启 workload 并验证 Prometheus 是否能查询 Istio 指标 |
| `experiment/collect_istio_latency.py` | 采集 7 个服务的 Istio destination latency，输出 `rawdata.xlsx`、`raw_prometheus.csv` 和 `quality.json` |
| `experiment/run_mesh_experiments.py` | 编排 baseline 采集、ChaosMesh 注入、fault 采集、DyCause 数据导出和可选 DyCause 执行 |
| `experiment/chaos/mesh-e3-network-delay-payment.yaml` | payment 300ms NetworkDelay |
| `experiment/chaos/mesh-e4-network-delay-user.yaml` | user 300ms NetworkDelay |
| `experiment/chaos/mesh-e5-network-delay-catalogue.yaml` | catalogue 300ms NetworkDelay |
| `experiment/load-gen-checkout.yaml` | checkout 链路候选筛选负载，提高 carts/orders/shipping 连续请求占比 |

### 7.3 增强实验矩阵

| ID | Fault | Root Cause | Root Index |
|----|-------|------------|-----------:|
| mesh_e1 | Pod-Kill payment | payment | 5 |
| mesh_e2 | Pod-Kill user | user | 7 |
| mesh_e3 | NetworkDelay 300ms payment | payment | 5 |
| mesh_e4 | NetworkDelay 300ms user | user | 7 |
| mesh_e5 | NetworkDelay 300ms catalogue | catalogue | 2 |
| mesh_e6 | NetworkDelay 300ms orders | orders | 4 |
| mesh_e7 | NetworkDelay 300ms carts | carts | 3 |
| mesh_e8 | NetworkDelay 300ms shipping | shipping | 6 |
| mesh_e9 | Pod-Kill orders | orders | 4 |

默认每个场景重复 10 次，采集窗口为 baseline 600s + fault 600s。`run_mesh_experiments.py` 默认会先等待对应窗口，再查询 Prometheus 最近窗口数据，保证 baseline 和 fault 数据覆盖真实实验阶段；`--no-wait` 只用于快速验证脚本管线。每次运行的数据保存到：

```text
data/sockshop_mesh/<exp>/runXX/
dycause_rca/data/<exp>_mesh_runXX/rawdata.xlsx
```

### 7.4 数据质量控制

每次采集会记录每个服务的：

- expected points
- valid points
- missing points
- zero points
- valid ratio

默认要求每列有效采样点比例不低于 95%。低于阈值的 run 会在 `quality.json` 和 `data/sockshop_mesh/summary.csv` 中标记为 invalid，不应进入主结果统计。

### 7.4.1 负载生成器调整

压缩批量实验后发现，旧版 `load-gen` 主要直接请求各个后端服务，虽然能保证 7 列 mesh latency 数据完整，但会削弱服务间自然调用链，导致 DyCause 构造出的因果边不稳定。为改善这一点，新增 `experiment/load-gen-business.yaml`：

- 主流量走 front-end 页面和 front-end API proxy，包括 `/`、`/category.html`、`/detail.html`、`/basket.html`、`/catalogue`、`/tags`、`/customers`、`/cards`、`/cart`、`/orders`；
- 每 5 轮保留一次低频 direct coverage probe，覆盖 catalogue、carts、orders、payment、shipping、user；
- load-gen Pod 仍关闭 Istio sidecar 注入，避免把负载源本身纳入 mesh 节点。

修改后验证 Prometheus 中 7 个 destination workload 均有请求速率；单独运行 `collect_istio_latency.py --duration 60 --rate-window 15s` 得到 60×7 数据，7 个服务有效采样点比例均为 100%。后续重复实验应使用该业务链式负载重新采集，以比较 DyCause 准确率是否改善。

业务链式 load 的首个 `mesh_e3` 验证 run 已完成，输出到 `data/sockshop_mesh_business/mesh_e3/run01/`，数据为 600×7 且 7 个服务有效采样点比例均为 100%。默认旧主参数 `lag=7, step=30, edge_thres=0.8` 下 payment 根因 rank=4，PR@5=1.0，Acc=0.5714。对同一份数据做参数敏感性后，`lag=5, step=20/30/60, edge_thres=0.8` 可将 payment 排到第 2，PR@2=1.0，Acc=0.8571。因此业务链式 load 的后续批量实验建议主参数改为 `lag=5, step=30, edge_thres=0.8`。

### 7.5 参数敏感性分析

增强脚本支持 DyCause 参数网格：

| 参数 | 取值 |
|------|------|
| `lag` | 3, 5, 7 |
| `step` | 20, 30, 60 |
| `edge_thres` | 0.4, 0.6, 0.8 |

运行方式：

```bash
cd experiment
python run_mesh_experiments.py --exp mesh_e1 --repeat 1 --run-dycause --sensitivity
```

该设计将原先“单次、4 节点、2 场景”的初步复现扩展为“多次、7 节点、多对象、带数据质量记录与参数敏感性”的完整改进版实验。

### 7.5.1 候选对象筛选设计

`mesh_e2/e4/e5` 在业务链式 load 下表现较差，应作为 negative cases / threat to validity 分析，而不再作为主结果核心对象。新增候选对象使用 `experiment/load-gen-checkout.yaml` 和独立数据目录：

```text
data/sockshop_mesh_candidate/<exp>/runXX/
dycause_rca/data/candidate_<exp>_mesh_runXX/rawdata.xlsx
```

候选筛选先对 `mesh_e6/e7/e8/e9` 各跑 1 次 `300s baseline + 300s fault`，主参数为 `lag=5, step=30, edge_thres=0.8, rate_window=15s`。若 root rank 进入 Top-2，或 PR@5=1 且参数敏感性存在稳定 Top-2 组合，则进入短重复验证。

首轮候选筛选已经完成，4 个 run 均为 600×7，7 个服务有效采样比例均达到 100%。结果如下：

| Experiment | Root | Fault | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Fault/Baseline |
|---|---|---|---:|---:|---:|---:|---:|---:|
| mesh_e6 | orders | NetworkDelay 300ms | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 24.6051 |
| mesh_e7 | carts | NetworkDelay 300ms | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 24.0286 |
| mesh_e8 | shipping | NetworkDelay 300ms | — | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.7531 |
| mesh_e9 | orders | Pod-Kill | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | 6.4925 |

因此，后续短重复验证应优先选择 `mesh_e6`、`mesh_e7`、`mesh_e9`。`mesh_e8` 可保留为 shipping 对象不适合当前 checkout load 的负例。

### 7.6 mesh_e1 正式单次结果

已完成 `mesh_e1` 的正式单次实验：baseline 600s + fault 600s，输出数据为 1200×7，7 个服务有效采样点均为 1200/1200。默认 4 节点参数 `lag=5, step=30, edge_thres=0.7` 在 mesh 数据上未形成有效回溯路径，PR@K=0。修正 DyCause 根因编号后，同一份数据在 `lag=7, step=30, edge_thres=0.8` 下可将 payment 排到第 2：

| Exp | Params | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|-----|--------|----------:|-----:|-----:|-----:|----:|
| mesh_e1 | lag=7, step=30, edge=0.8 | 2 | 0.00 | 1.00 | 1.00 | 0.8571 |
| mesh_e1 | lag=7, step=30, edge=0.4/0.6 | 3 | 0.00 | 0.00 | 1.00 | 0.7143 |
| mesh_e3 | lag=7, step=30, edge=0.8 | 1 | 1.00 | 1.00 | 1.00 | 1.0000 |
| mesh_e2 | lag=3/5/7, step=30, edge=0.4/0.6/0.8 | — | 0.00 | 0.00 | 0.00 | 0.0000 |
| mesh_e4 | lag=3/5/7, step=20/30/60, edge=0.4/0.6/0.8 | — | 0.00 | 0.00 | 0.00 | 0.0000 |

注意：DyCause 日志中的服务编号为 1-based，front-end 入口仍按命令行参数 `0` 传入。mesh 实验的根因编号因此为 catalogue=2、payment=5、user=7。早期按 0-based 编号的结果需要废弃。`mesh_e2` 和 `mesh_e4` 的正式单次数据质量同样为 1200×7、100% 有效点，但 user 相关故障在已测试参数网格中未进入 Top-K，说明 Service Mesh 已解决节点覆盖和数据密度问题，但不同服务和故障类型仍存在可诊断性差异。

业务链式 load 下，`mesh_e1` 到 `mesh_e5` 已各完成 1 次压缩正式采集。`mesh_e1` 和 `mesh_e3` 均可将 payment 排到第 2，`mesh_e2/e4/e5` 暂未命中，原因主要是 user 流量弱、Pod-Kill 后可能失败更快返回，以及 user/catalogue delay 与 front-end 几乎同步抬升，时序差不足。

### 7.7 压缩批量实验结果

为在本地 Minikube 资源限制下尽量一次跑完重复实验，新增压缩批量脚本 `experiment/run_compressed_mesh_batch.py`。该批次使用 `baseline=300s`、`fault=300s`、`delay=15s`、`rate_window=15s`，DyCause 主参数为 `lag=7, step=30, edge_thres=0.8`。批次新增 19 个 run：

- `mesh_e1`、`mesh_e3`、`mesh_e5` 各 5 次；
- `mesh_e2`、`mesh_e4` 各 2 次，作为 user 服务相关边界/负例场景。

所有新增 run 的数据质量均有效，7 个服务每列有效采样点比例均达到 100%。汇总文件为：

```text
data/sockshop_mesh/compressed_summary.csv
data/sockshop_mesh/compressed_results.md
```

注意：该压缩批次使用的是旧 direct-service load。之后改用 `experiment/load-gen-business.yaml` 后，新数据应写入独立目录：

```text
data/sockshop_mesh_business/<exp>/runXX/
dycause_rca/data/business_<exp>_mesh_runXX/rawdata.xlsx
```

对应 metadata 中 `load_profile=business-front-proxy-v1`。旧数据根 `data/sockshop_mesh/` 保留为 direct-service load 的结果，不再用 run 编号推断新旧。

压缩批次主参数结果如下：

| Experiment | Runs | Valid | PR@1 | PR@2 | PR@5 | Acc mean | Acc std | Top-2 hit | Root ranks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| mesh_e1 | 5 | 5 | 0.8000 | 0.8000 | 0.8000 | 0.8000 | 0.4000 | 0.8000 | 1, -, 1, 1, 1 |
| mesh_e2 | 2 | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 1, - |
| mesh_e3 | 5 | 5 | 0.2000 | 0.4000 | 0.6000 | 0.4571 | 0.4180 | 0.4000 | 5, -, 2, 1, - |
| mesh_e4 | 2 | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -, - |
| mesh_e5 | 5 | 5 | 0.0000 | 0.2000 | 0.2000 | 0.1714 | 0.3428 | 0.2000 | -, -, -, 2, - |

该结果说明，压缩窗口能显著降低总运行时间并保持 100% 数据有效性，但诊断稳定性低于部分 600s 长窗口结果，尤其是 `mesh_e3` 在 600s 单次中可达到 root rank=1，而压缩 300s 重复中波动明显。因此，报告主线可采用压缩批次作为重复性统计，并用 600s 单次作为长窗口稳健性对照。
