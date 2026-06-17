# Main Repeat Overview

Main params: `lag=7`, `step=30`, `edge_thres=0.8`; load profile: `legacy-compressed-v1` for new runs.

| Experiment | Root | Fault | Runs | Top-2 | Top-2 Rate | Top-5 | Top-5 Rate | Acc Mean | Acc Std | Min Quality |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mesh_e1 | payment | pod-kill | 10 | 5 | 0.500 | 5 | 0.500 | 0.5143 | 0.4912 | 0.975 |
| mesh_e3 | payment | network-delay | 10 | 4 | 0.400 | 6 | 0.600 | 0.4857 | 0.4270 | 1.000 |
| mesh_e2 | user | pod-kill | 5 | 2 | 0.400 | 2 | 0.400 | 0.4000 | 0.5477 | 0.985 |
| el_e2 | payment | network-corrupt | 8 | 3 | 0.375 | 5 | 0.625 | 0.5000 | 0.4452 | 1.000 |
| el_e5 | orders | pod-kill | 7 | 2 | 0.286 | 3 | 0.429 | 0.3673 | 0.4194 | 0.995 |
| el_e13 | carts | network-loss | 5 | 1 | 0.200 | 2 | 0.400 | 0.3429 | 0.4116 | 1.000 |
| mesh_e5 | catalogue | network-delay | 7 | 1 | 0.143 | 1 | 0.143 | 0.1429 | 0.3194 | 1.000 |
| el_e4 | payment | cpu-stress | 5 | 0 | 0.000 | 3 | 0.600 | 0.3714 | 0.3440 | 1.000 |
| el_e16 | carts | cpu-stress | 1 | 0 | 0.000 | 0 | 0.000 | 0.2857 | 0.0000 | 1.000 |
| el_e6 | orders | network-delay | 1 | 0 | 0.000 | 0 | 0.000 | 0.1429 | 0.0000 | 1.000 |
| mesh_e4 | user | network-delay | 3 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e1 | payment | network-loss | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e10 | orders | cpu-stress | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e11 | carts | pod-kill | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 0.990 |
| el_e12 | carts | network-delay | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e14 | carts | network-corrupt | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e15 | carts | network-duplicate | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e3 | payment | network-duplicate | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e7 | orders | network-loss | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e8 | orders | network-corrupt | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
| el_e9 | orders | network-duplicate | 1 | 0 | 0.000 | 0 | 0.000 | 0.0000 | 0.0000 | 1.000 |
