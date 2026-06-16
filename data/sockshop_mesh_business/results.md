# SockShop Mesh Results

## Main Parameters

`lag=5`, `step=30`, `edge_thres=0.8`

| Experiment | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---:|---|---:|---:|---:|---:|---:|
| mesh_e1 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Candidate Screening

| Experiment | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mesh_e1 | run01 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0017 | 0.0039 | 2.2827 |
| mesh_e2 | run01 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0024 | 0.0017 | 0.7309 |
| mesh_e3 | run01 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0015 | 0.0016 | 1.0426 |
| mesh_e4 | run01 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 0.1559 | 108.2532 |
| mesh_e5 | run01 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0019 | 0.2499 | 128.2287 |

## Aggregate Over Result Rows

| Experiment | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---:|---:|---:|---:|---:|---:|---:|
| mesh_e1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | 0.0000 | 1.0000 |
| mesh_e2 | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | 24 | 0.0000 | 0.1667 | 0.8333 | 0.5297 | 0.2591 | 0.1667 |
| mesh_e4 | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Runs

| Experiment | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| mesh_e1 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=30, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=20, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=20, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=30, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=30, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=60, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=20, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=30, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=30, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=30, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=60, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=60, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=60, edge=0.4 |
| mesh_e3 | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=60, edge=0.6 |
| mesh_e3 | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e5 | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
