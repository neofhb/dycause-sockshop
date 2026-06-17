# SockShop Mesh Results (sockshop_mesh_final)

## Main Parameters

`lag=5`, `step=30`, `edge_thres=0.7`

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 |

## Main Result Rows

| Experiment | Group | Fault | Role | Run | Root | Quality | Root Rank | PR@2 | PR@5 | Acc | Baseline Mean | Fault Mean | Fault/Baseline |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | run01 | payment(5) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 0.0026 | 1.8589 |
| final_e2 | formal | network-delay | core | run01 | payment(5) | True | 3 | 0.0000 | 1.0000 | 0.7143 | 0.0023 | 0.0011 | 0.5089 |
| final_e3 | formal | network-loss | augmentation | run01 | payment(5) | True | 1 | 1.0000 | 1.0000 | 1.0000 | 0.0007 | 0.0010 | 1.4468 |
| final_e4 | formal | pod-kill | core | run01 | orders(4) | False | 3 | 0.0000 | 1.0000 | 0.7143 | 0.0176 | 0.0947 | 5.3911 |
| final_e5 | formal | network-delay | core | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.0883 | 0.1430 | 1.6191 |
| final_e6 | formal | network-loss | augmentation | run01 | orders(4) | True |  | 0.0000 | 0.0000 | 0.0000 | 0.1487 | 0.1022 | 0.6872 |
| final_e7 | formal | network-delay | supplementary | run01 | carts(3) | True | 5 | 0.0000 | 1.0000 | 0.4286 | 0.1109 | 0.1897 | 1.7103 |

## Aggregate Over Result Rows

| Experiment | Group | Fault | Role | Root | Result Rows | PR@1 | PR@2 | PR@5 | Acc Mean | Acc Std | Top-2 Hit |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| final_e1 | formal | pod-kill | core | payment(5) | 40 | 0.0000 | 0.0500 | 0.2500 | 0.1393 | 0.2545 | 0.0500 |
| final_e2 | formal | network-delay | core | payment(5) | 40 | 0.0000 | 0.0000 | 0.3000 | 0.2071 | 0.3178 | 0.0000 |
| final_e3 | formal | network-loss | augmentation | payment(5) | 40 | 0.0250 | 0.0250 | 0.0250 | 0.0250 | 0.1561 | 0.0250 |
| final_e5 | formal | network-delay | core | orders(4) | 21 | 0.0000 | 0.0000 | 0.0000 | 0.0136 | 0.0608 | 0.0000 |
| final_e6 | formal | network-loss | augmentation | orders(4) | 6 | 0.0000 | 0.0000 | 0.1667 | 0.2381 | 0.1963 | 0.0000 |
| final_e7 | formal | network-delay | supplementary | carts(3) | 6 | 0.0000 | 0.0000 | 0.3333 | 0.2857 | 0.2474 | 0.0000 |

## Runs

| Experiment | Group | Fault | Role | Run | Quality | Root | Root Rank | PR@1 | PR@2 | PR@5 | Acc | Params |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=20, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 2 | 0.0000 | 1.0000 | 1.0000 | 0.8571 | lag=3, step=20, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=3, step=20, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=3, step=30, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=60, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=60, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=7, step=60, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.8 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.4 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=60, edge=0.6 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=60, edge=0.7 |
| final_e1 | formal | pod-kill | core | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=60, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=30, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=5, step=60, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=60, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.8 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.4 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.6 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.7 |
| final_e2 | formal | network-delay | core | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=5, step=30, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=30, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=7, step=60, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=30, edge=0.8 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.4 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.6 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.7 |
| final_e3 | formal | network-loss | augmentation | run01 | True | payment(5) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=9, step=60, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=3, step=30, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=3, step=30, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | lag=3, step=30, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=30, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=60, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=60, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=60, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=30, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=7, step=60, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=9, step=30, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=30, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=30, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=30, edge=0.8 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=9, step=60, edge=0.4 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=9, step=60, edge=0.6 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=9, step=60, edge=0.7 |
| final_e4 | formal | pod-kill | core | run01 | False | orders(4) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=9, step=60, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.4 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.7 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.4 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.6 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.7 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=30, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.4 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.6 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.7 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=60, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.4 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.6 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.7 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.4 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.6 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.7 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.8 |
| final_e5 | formal | network-delay | core | run01 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=3, step=20, edge=0.6 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=3, step=20, edge=0.7 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=20, edge=0.7 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=5, step=30, edge=0.7 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=5, step=30, edge=0.8 |
| final_e6 | formal | network-loss | augmentation | run01 | True | orders(4) | 4 | 0.0000 | 0.0000 | 1.0000 | 0.5714 | lag=7, step=30, edge=0.8 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.6 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) |  | 0.0000 | 0.0000 | 0.0000 | 0.0000 | lag=3, step=20, edge=0.7 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) | 3 | 0.0000 | 0.0000 | 1.0000 | 0.7143 | lag=5, step=20, edge=0.7 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) | 5 | 0.0000 | 0.0000 | 1.0000 | 0.4286 | lag=5, step=30, edge=0.7 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=5, step=30, edge=0.8 |
| final_e7 | formal | network-delay | supplementary | run01 | True | carts(3) | 6 | 0.0000 | 0.0000 | 0.0000 | 0.2857 | lag=7, step=30, edge=0.8 |
