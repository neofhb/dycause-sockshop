# SockShop Mesh Results (sockshop_mesh_extended)

## Load Profiles

| Load Profile | Rows |
|---|---:|
| legacy-compressed-v0 | 93 |
| legacy-compressed-v1 | 202 |

## Main Parameters

`lag=7`, `step=30`, `edge_thres=0.8`

| Experiment | Load Profile | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| el_e10 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e12 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run02 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run03 | True | carts(3) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run04 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run05 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run06 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run07 | True | carts(3) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run08 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run09 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run10 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e14 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e15 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e16 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 |
| el_e1 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run04 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run05 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run06 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run07 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run08 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run09 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e3 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run02 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run04 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run05 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run07 | True | payment(5) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run08 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run09 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run02 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run03 | True | orders(4) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run04 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run05 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run06 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run07 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run08 | True | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run09 | True | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run10 | True | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 |
| el_e7 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e8 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e9 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run04 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run06 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run07 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run08 | True | payment(5) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run09 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run02 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run04 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run05 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run02 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run04 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run07 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run08 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run09 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run04 | True | catalogue(2) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run05 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run06 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run07 | True | catalogue(2) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 |

## Main Result Rows

| Experiment | Load Profile | Group | Fault | Role | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| el_e10 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0085 | 0.0166 | 1.9372 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0079 | 0.0571 | 7.2313 |
| el_e12 | legacy-compressed-v1 | extended | network-delay | core | run01 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0355 | 0.1383 | 3.8912 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | carts(3) | True | 5 | 0.0000 | 1.0000 | 0.4286 | 0.0166 | 0.0195 | 1.1747 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run02 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0091 | 0.0149 | 1.6245 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run03 | carts(3) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0097 | 0.0222 | 2.3031 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run04 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0145 | 0.0140 | 0.9676 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run05 | carts(3) | True | 6 | 0.0000 | 0.0000 | 0.2857 | 0.0130 | 0.0138 | 1.0637 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run06 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0087 | 0.0281 | 3.2129 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run07 | carts(3) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0094 | 0.0182 | 1.9402 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run08 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0102 | 0.0185 | 1.8068 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run09 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0165 | 0.0155 | 0.9390 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run10 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0107 | 0.0151 | 1.4098 |
| el_e14 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0141 | 0.0196 | 1.3959 |
| el_e15 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | carts(3) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0292 | 0.0126 | 0.4309 |
| el_e16 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | carts(3) | True | 6 | 0.0000 | 0.0000 | 0.2857 | 0.0128 | 0.0284 | 2.2199 |
| el_e1 | legacy-compressed-v1 | extended | network-loss | core | run01 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0113 | 0.0090 | 0.7963 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0050 | 0.0028 | 0.5603 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run02 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0056 | 0.0016 | 0.2787 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run03 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0008 | 0.0013 | 1.6389 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run04 | payment(5) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0082 | 0.0019 | 0.2348 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run05 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0023 | 0.0025 | 1.0644 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run06 | payment(5) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0046 | 0.0027 | 0.5991 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run07 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0032 | 0.0028 | 0.8737 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run08 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0022 | 0.0056 | 2.5124 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run09 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0135 | 0.0039 | 0.2862 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run10 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0020 | 0.0024 | 1.1834 |
| el_e3 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0029 | 0.0027 | 0.9329 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | payment(5) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0028 | 0.0396 | 14.0981 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run02 | payment(5) | True | 3 | 0.0000 | 1.0000 | 0.7143 | 0.0047 | 0.0232 | 4.9382 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run03 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0039 | 0.0244 | 6.3114 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run04 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0053 | 0.0118 | 2.2109 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run05 | payment(5) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0023 | 0.0138 | 6.0902 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run06 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0057 | 0.0207 | 3.6107 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run07 | payment(5) | True | 6 | 0.0000 | 0.0000 | 0.2857 | 0.0021 | 0.0197 | 9.4293 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run08 | payment(5) | True | 7 | 0.0000 | 0.0000 | 0.1429 | 0.0022 | 0.0260 | 11.8712 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run09 | payment(5) | True | 7 | 0.0000 | 0.0000 | 0.1429 | 0.0020 | 0.0204 | 10.1998 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run10 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0023 | 0.0260 | 11.2312 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | orders(4) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0086 | 0.0612 | 7.1331 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run02 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0123 | 0.0886 | 7.2212 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run03 | orders(4) | True | 5 | 0.0000 | 1.0000 | 0.4286 | 0.0150 | 0.0593 | 3.9611 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run04 | orders(4) | True | 6 | 0.0000 | 0.0000 | 0.2857 | 0.0140 | 0.0833 | 5.9575 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run05 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0615 | 0.0796 | 1.2932 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run06 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0108 | 0.0687 | 6.3924 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run07 | orders(4) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0180 | 0.0511 | 2.8336 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run08 | orders(4) | True | 3 | 0.0000 | 1.0000 | 0.7143 | 0.0085 | 0.0827 | 9.7559 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run09 | orders(4) | True | 3 | 0.0000 | 1.0000 | 0.7143 | 0.0173 | 0.0459 | 2.6466 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run10 | orders(4) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0117 | 0.0500 | 4.2738 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | orders(4) | True | 7 | 0.0000 | 0.0000 | 0.1429 | 0.0159 | 0.1251 | 7.8506 |
| el_e7 | legacy-compressed-v1 | extended | network-loss | core | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0205 | 0.0169 | 0.8283 |
| el_e8 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0097 | 0.0109 | 1.1225 |
| el_e9 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0085 | 0.0126 | 1.4865 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0004 | 0.0008 | 2.0453 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run02 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0004 | 0.0012 | 3.2396 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run03 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0004 | 0.0025 | 5.5778 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run04 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0006 | 0.0013 | 2.2013 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run05 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0006 | 0.0013 | 2.3325 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run06 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0007 | 0.0016 | 2.1987 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run07 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0069 | 0.0064 | 0.9290 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run08 | payment(5) | True | 6 | 0.0000 | 0.0000 | 0.2857 | 0.0041 | 0.0088 | 2.1605 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run09 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0081 | 0.0083 | 1.0276 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run10 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0031 | 0.0035 | 1.1313 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0013 | 0.0011 | 0.8750 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run02 | user(7) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0017 | 0.0017 | 1.0109 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run03 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0016 | 0.0022 | 1.3348 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run04 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0037 | 0.0129 | 3.4688 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run05 | user(7) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0079 | 0.0051 | 0.6461 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run01 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0004 | 0.0007 | 1.4805 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run02 | payment(5) | True | 5 | 0.0000 | 1.0000 | 0.4286 | 0.0005 | 0.0009 | 1.7322 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run03 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0006 | 0.0009 | 1.3836 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run04 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0006 | 0.0011 | 1.9522 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run05 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0005 | 0.0009 | 1.5673 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run06 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0005 | 0.0009 | 1.6356 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run07 | payment(5) | True | 7 | 0.0000 | 0.0000 | 0.1429 | 0.0028 | 0.0031 | 1.0850 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run08 | payment(5) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0042 | 0.0073 | 1.7397 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run09 | payment(5) | True | 4 | 0.0000 | 1.0000 | 0.5714 | 0.0046 | 0.0040 | 0.8820 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run10 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0036 | 0.0028 | 0.7616 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 0.1401 | 129.9502 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 0.1393 | 96.2375 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | user(7) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 0.1391 | 101.6229 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0018 | 0.2406 | 134.4025 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0018 | 0.2424 | 132.3538 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0017 | 0.2423 | 138.7573 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run04 | catalogue(2) | True | 2 | 1.0000 | 1.0000 | 0.8571 | 0.0018 | 0.2415 | 132.5720 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run05 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0018 | 0.2416 | 137.3919 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run06 | catalogue(2) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0044 | 0.2106 | 47.3659 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run07 | catalogue(2) | True | 7 | 0.0000 | 0.0000 | 0.1429 | 0.0056 | 0.2109 | 37.9751 |

## Aggregate Over Result Rows

| Experiment | Load Profile | Group | Fault | Role | Root | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | payment(5) | 6 | 0.6667 | 0.8333 | 0.8333 | 0.8095 | 0.3658 | 0.8333 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | user(7) | 3 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.4714 | 0.3333 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | payment(5) | 6 | 0.3333 | 0.5000 | 0.6667 | 0.5476 | 0.4319 | 0.5000 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | user(7) | 3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | catalogue(2) | 5 | 0.0000 | 0.2000 | 0.2000 | 0.1714 | 0.3428 | 0.2000 |
| el_e1 | legacy-compressed-v1 | extended | network-loss | core | payment(5) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e10 | legacy-compressed-v1 | extended | cpu-stress | exploratory | orders(4) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | carts(3) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e12 | legacy-compressed-v1 | extended | network-delay | core | carts(3) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | carts(3) | 10 | 0.1000 | 0.2000 | 0.3000 | 0.2571 | 0.3659 | 0.2000 |
| el_e14 | legacy-compressed-v1 | extended | network-corrupt | core | carts(3) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e15 | legacy-compressed-v1 | extended | network-duplicate | core | carts(3) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e16 | legacy-compressed-v1 | extended | cpu-stress | exploratory | carts(3) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | 0.0000 | 0.0000 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | payment(5) | 10 | 0.2000 | 0.3000 | 0.5000 | 0.4000 | 0.4228 | 0.3000 |
| el_e3 | legacy-compressed-v1 | extended | network-duplicate | core | payment(5) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | payment(5) | 10 | 0.0000 | 0.0000 | 0.3000 | 0.2429 | 0.2638 | 0.0000 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | orders(4) | 10 | 0.1000 | 0.2000 | 0.6000 | 0.4571 | 0.3546 | 0.2000 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | orders(4) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | 0.0000 | 0.0000 |
| el_e7 | legacy-compressed-v1 | extended | network-loss | core | orders(4) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e8 | legacy-compressed-v1 | extended | network-corrupt | core | orders(4) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| el_e9 | legacy-compressed-v1 | extended | network-duplicate | core | orders(4) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | payment(5) | 4 | 0.0000 | 0.0000 | 0.0000 | 0.0714 | 0.1237 | 0.0000 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | user(7) | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | payment(5) | 4 | 0.0000 | 0.2500 | 0.5000 | 0.3928 | 0.3407 | 0.2500 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | catalogue(2) | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0714 | 0.0714 | 0.0000 |

## Aggregate By Service And Fault

| Load Profile | Root | Fault | Result Rows | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---|---|---:|---:|---:|---:|---:|---:|
| legacy-compressed-v0 | catalogue | network-delay | 5 | 0.2000 | 0.2000 | 0.1714 | 0.3428 | 0.2000 |
| legacy-compressed-v0 | payment | network-delay | 6 | 0.5000 | 0.6667 | 0.5476 | 0.4319 | 0.5000 |
| legacy-compressed-v0 | payment | pod-kill | 6 | 0.8333 | 0.8333 | 0.8095 | 0.3658 | 0.8333 |
| legacy-compressed-v0 | user | network-delay | 3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v0 | user | pod-kill | 3 | 0.3333 | 0.3333 | 0.3333 | 0.4714 | 0.3333 |
| legacy-compressed-v1 | carts | cpu-stress | 1 | 0.0000 | 0.0000 | 0.2857 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | carts | network-corrupt | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | carts | network-delay | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | carts | network-duplicate | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | carts | network-loss | 10 | 0.2000 | 0.3000 | 0.2571 | 0.3659 | 0.2000 |
| legacy-compressed-v1 | carts | pod-kill | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | catalogue | network-delay | 2 | 0.0000 | 0.0000 | 0.0714 | 0.0714 | 0.0000 |
| legacy-compressed-v1 | orders | cpu-stress | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | orders | network-corrupt | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | orders | network-delay | 1 | 0.0000 | 0.0000 | 0.1429 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | orders | network-duplicate | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | orders | network-loss | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | orders | pod-kill | 10 | 0.2000 | 0.6000 | 0.4571 | 0.3546 | 0.2000 |
| legacy-compressed-v1 | payment | cpu-stress | 10 | 0.0000 | 0.3000 | 0.2429 | 0.2638 | 0.0000 |
| legacy-compressed-v1 | payment | network-corrupt | 10 | 0.3000 | 0.5000 | 0.4000 | 0.4228 | 0.3000 |
| legacy-compressed-v1 | payment | network-delay | 4 | 0.2500 | 0.5000 | 0.3928 | 0.3407 | 0.2500 |
| legacy-compressed-v1 | payment | network-duplicate | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | payment | network-loss | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| legacy-compressed-v1 | payment | pod-kill | 4 | 0.0000 | 0.0000 | 0.0714 | 0.1237 | 0.0000 |
| legacy-compressed-v1 | user | pod-kill | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 |

## Runs

| Experiment | Load Profile | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| el_e10 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=5, step=60, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=5, step=60, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| el_e11 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| el_e12 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=3, step=20, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=3, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=60, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=5, step=60, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=30, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run02 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run03 | True | carts(3) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run04 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run05 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run06 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run07 | True | carts(3) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run08 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run09 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e13 | legacy-compressed-v1 | extended | network-loss | core | run10 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e14 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e15 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e16 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| el_e1 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=20, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=20, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=20, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=30, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=30, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=3, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=60, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=60, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=60, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=20, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=60, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=5, step=60, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=60, edge=0.6 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=60, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run04 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run05 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run06 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run07 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run08 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run09 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e2 | legacy-compressed-v1 | extended | network-corrupt | core | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e3 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=20, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=20, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=30, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=30, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=60, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=60, edge=0.4 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=60, edge=0.6 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run02 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run04 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run05 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run07 | True | payment(5) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run08 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run09 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.8 |
| el_e4 | legacy-compressed-v1 | extended | cpu-stress | exploratory | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=20, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=3, step=20, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=3, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=60, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run02 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run03 | True | orders(4) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run04 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run05 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run06 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run07 | True | orders(4) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run08 | True | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run09 | True | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.8 |
| el_e5 | legacy-compressed-v1 | extended | pod-kill | core | run10 | True | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=20, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=20, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=20, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=30, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=30, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=30, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=60, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=3, step=60, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=3, step=60, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=20, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=20, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=30, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=30, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=30, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=60, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=5, step=60, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.8 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=60, edge=0.4 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=60, edge=0.6 |
| el_e6 | legacy-compressed-v1 | extended | network-delay | core | run01 | True | orders(4) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=60, edge=0.8 |
| el_e7 | legacy-compressed-v1 | extended | network-loss | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e8 | legacy-compressed-v1 | extended | network-corrupt | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| el_e9 | legacy-compressed-v1 | extended | network-duplicate | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.7 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.6 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=60, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run02 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run04 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v0 | legacy | pod-kill | main-reference | run06 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run07 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run08 | True | payment(5) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run09 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e1 | legacy-compressed-v1 | business | pod-kill | main-reference | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run02 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v0 | legacy | pod-kill | negative-case | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run04 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e2 | legacy-compressed-v1 | business | pod-kill | negative-case | run05 | True | user(7) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run02 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run03 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run04 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run05 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v0 | legacy | network-delay | main-reference | run06 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run07 | True | payment(5) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run08 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run09 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| mesh_e3 | legacy-compressed-v1 | business | network-delay | main-reference | run10 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e4 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | True | user(7) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run01 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run02 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run03 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run04 | True | catalogue(2) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v0 | legacy | network-delay | negative-case | run05 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run06 | True | catalogue(2) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| mesh_e5 | legacy-compressed-v1 | business | network-delay | negative-case | run07 | True | catalogue(2) | 7 | 0.0000 | 0.0000 | 0.0000 | 0.1429 | lag=7, step=30, edge=0.8 |
