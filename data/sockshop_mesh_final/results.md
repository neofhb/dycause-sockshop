# SockShop Mesh Results (sockshop_mesh_final)

## Main Parameters

`lag=5`, `step=30`, `edge_thres=0.8`

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Main Result Rows

| Experiment | Group | Fault | Role | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | run01 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 0.0026 | 1.8589 |

## Aggregate Over Result Rows

| Experiment | Group | Fault | Role | Root | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | payment(5) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Runs

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
