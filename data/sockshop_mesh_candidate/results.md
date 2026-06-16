# SockShop Mesh Results (sockshop_mesh_candidate)

## Main Parameters

`lag=5`, `step=30`, `edge_thres=0.8`

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| mesh_e6 |  |  |  | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e7 |  |  |  | run01 | True | carts(3) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e8 |  |  |  | run01 | True | shipping(6) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e9 |  |  |  | run01 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |

## Main Result Rows

| Experiment | Group | Fault | Role | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mesh_e6 |  |  |  | run01 | orders(4) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0048 | 0.1182 | 24.6051 |
| mesh_e7 |  |  |  | run01 | carts(3) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0061 | 0.1464 | 24.0286 |
| mesh_e8 |  |  |  | run01 | shipping(6) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0016 | 0.0012 | 0.7531 |
| mesh_e9 |  |  |  | run01 | orders(4) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0040 | 0.0259 | 6.4925 |

## Aggregate Over Result Rows

| Experiment | Group | Fault | Role | Root | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| mesh_e6 |  |  |  | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| mesh_e7 |  |  |  | carts(3) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| mesh_e8 |  |  |  | shipping(6) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e9 |  |  |  | orders(4) | 1 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | 0.0000 | 1.0000 |

## Runs

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| mesh_e6 |  |  |  | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=5, step=30, edge=0.8 |
| mesh_e7 |  |  |  | run01 | True | carts(3) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=5, step=30, edge=0.8 |
| mesh_e8 |  |  |  | run01 | True | shipping(6) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e9 |  |  |  | run01 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=30, edge=0.8 |
