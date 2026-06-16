# SockShop Mesh Results

## Main Parameters

`lag=7`, `step=30`, `edge_thres=0.8`

| Experiment | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---:|---|---:|---:|---:|---:|---:|
| mesh_e1 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e1 | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | run04 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run06 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e2 | run02 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e2 | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | run02 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |
| mesh_e3 | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | run04 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e3 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | run02 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run02 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run03 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run04 | True | catalogue(2) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e5 | run05 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Aggregate Over Result Rows

| Experiment | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---:|---:|---:|---:|---:|---:|---:|
| mesh_e1 | 30 | 0.1333 | 0.2000 | 0.3000 | 0.2619 | 0.4059 | 0.2000 |
| mesh_e2 | 26 | 0.0385 | 0.0385 | 0.0385 | 0.0385 | 0.1923 | 0.0385 |
| mesh_e3 | 6 | 0.3333 | 0.5000 | 0.6667 | 0.5476 | 0.4319 | 0.5000 |
| mesh_e4 | 26 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | 5 | 0.0000 | 0.2000 | 0.2000 | 0.1714 | 0.3428 | 0.2000 |

## Runs

| Experiment | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.7 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e1 | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e1 | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.6 |
| mesh_e1 | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=60, edge=0.8 |
| mesh_e1 | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | run04 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | run06 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| mesh_e2 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| mesh_e2 | run02 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run02 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run04 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| mesh_e4 | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| mesh_e4 | run02 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | run02 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | run03 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | run04 | True | catalogue(2) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e5 | run05 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
