# SockShop Mesh Compressed Batch Results

Filter: baseline=300, fault=300, lag=7, step=30, edge_thres=0.8.

| Experiment | Runs | Valid | PR@1 | PR@2 | PR@5 | Acc mean | Acc std | Top-2 hit | Root ranks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| mesh_e1 | 5 | 5 | 0.8000 | 0.8000 | 0.8000 | 0.8000 | 0.4000 | 0.8000 | 1, -, 1, 1, 1 |
| mesh_e2 | 2 | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 1, - |
| mesh_e3 | 5 | 5 | 0.2000 | 0.4000 | 0.6000 | 0.4571 | 0.4180 | 0.4000 | 5, -, 2, 1, - |
| mesh_e4 | 2 | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -, - |
| mesh_e5 | 5 | 5 | 0.0000 | 0.2000 | 0.2000 | 0.1714 | 0.3428 | 0.2000 | -, -, -, 2, - |

## Runs

| Experiment | Run | Valid | Root | Root rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---:|---|---:|---:|---:|---:|---:|
| mesh_e1 | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run03 | True | payment(5) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | run04 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | run06 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e2 | run02 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e2 | run03 | True | user(7) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | run02 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |
| mesh_e3 | run03 | True | payment(5) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | run04 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e3 | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | run06 | True | payment(5) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | run02 | True | user(7) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | run03 | True | user(7) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run01 | True | catalogue(2) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run02 | True | catalogue(2) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run03 | True | catalogue(2) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | run04 | True | catalogue(2) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e5 | run05 | True | catalogue(2) | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
