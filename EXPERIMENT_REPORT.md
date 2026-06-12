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

DyCause 从 12 条理论边中发现 4 条 Granger 显著边。
e1（payment 根因）和 e2（user 根因）共享同一因果链：**user→payment→catalogue→front-end**，e1 额外发现 **user→catalogue**。
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
