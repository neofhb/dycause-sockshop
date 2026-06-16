# SockShop Current Experiment Report

## 当前数据版本说明

当前仓库同时保留四类实验数据：

| 口径 | 路径 | 说明 |
|---|---|---|
| baseline reproduction | `data/sockshop/` | 原始 4 节点复现，作为历史基线 |
| enhanced reproduction | `data/sockshop_mesh_business/` | 当前 7 节点 business-front-proxy 主线 |
| object-selection refinement | `data/sockshop_mesh_candidate/` | 新实验对象筛选结果 |
| legacy archived batch | `data/archive/sockshop_mesh_legacy_direct_service/` | 旧 direct-service mesh 与旧压缩批次 |

当前主线不再引用旧 `sockshop_mesh` 结果。旧压缩批次和旧 direct-service mesh 数据只作为历史对照保存。

## 7 节点 business-front-proxy 主线结果

当前主参数为：

- `lag=5`
- `step=30`
- `edge_thres=0.8`
- `rate_window=15s`

当前主线数据根为 `data/sockshop_mesh_business/`。已完成的 5 个场景中，`payment` 相关场景可以稳定进入 Top-2：

| Experiment | Fault | Root | Root Rank | PR@2 | PR@5 | Acc |
|---|---|---|---:|---:|---:|---:|
| mesh_e1 | Pod-Kill payment | payment | 2 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e3 | NetworkDelay 300ms payment | payment | 2 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e2 | Pod-Kill user | user | — | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | NetworkDelay 300ms user | user | — | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | NetworkDelay 300ms catalogue | catalogue | — | 0.0000 | 0.0000 | 0.0000 |

结论：`payment` 是当前 7 节点主线中最稳定、最适合 DyCause 的 SockShop 对象；`user` 与 `catalogue` 不适合作为正式主实验对象。

## 候选对象筛选结果

候选筛选使用 checkout 导向负载 `business-checkout-v2`，数据根为 `data/sockshop_mesh_candidate/`。首轮 4 个候选场景均完成 1 次正式采集，数据质量全部为 `600 x 7` 且 100% 有效。

| Experiment | Fault | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---|---:|---:|---:|---:|---:|
| mesh_e6 | NetworkDelay 300ms orders | orders | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e7 | NetworkDelay 300ms carts | carts | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e8 | NetworkDelay 300ms shipping | shipping | — | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e9 | Pod-Kill orders | orders | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |

结论：`orders` 与 `carts` 在当前 service mesh + checkout 流量下表现非常强，已经比 `user`、`catalogue` 更接近正式主实验对象；`shipping` 暂时不适合。

## 当前推荐正式实验对象

当前推荐的正式主实验对象为：

- `payment`
- `orders`
- `carts`

它们分别覆盖支付、下单、购物车三个路径节点，并且已经在 business/candidate 两条当前主线上证明能够产生可追踪的延迟传播结构。

`shipping` 保留为负例；`user` 和 `catalogue` 归入失败案例分析，不再作为主结果核心对象。

## Negative Cases / Threat To Validity

当前失败案例主要分为两类：

1. `user` 相关场景：
   `user` 在当前业务流量中的占比偏弱，Pod-Kill 后还可能表现为请求失败更快返回，而不是延迟逐级传播，因此 DyCause 很难回溯到它。

2. `catalogue` 与 `shipping` 相关场景：
   即便故障本身明显，`front-end` 与根因服务可能近乎同步抬升，导致 Granger 很难从 1Hz + 15s rate window 的序列中稳定分出先后顺序。

这些负例并不说明 service mesh 采集失败，而是说明“实验对象选择”本身会显著影响 DyCause 的表现。

## 下一步短重复验证计划

下一步应优先补跑以下三个候选对象的短重复：

- `mesh_e6` orders delay：再补 3 次
- `mesh_e7` carts delay：再补 3 次
- `mesh_e9` orders pod-kill：再补 3 次

成功标准：

- 至少 `2/3` 次进入 Top-2
- 每次 `quality_valid=true`
- `PR@5=1` 持续保持

若验证通过，最终正式主实验对象即确定为 `payment + orders + carts`。
