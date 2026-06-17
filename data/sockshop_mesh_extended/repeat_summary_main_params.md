# Repeat Summary Main Params

Main params: `lag=7`, `step=30`, `edge_thres=0.8`.

| Experiment | Root | Fault | Runs | Top-2 | Top-2 Rate | Top-5 | Top-5 Rate | Acc Mean | Acc Std | Ranks |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| el_e2 | payment | network-corrupt | 5 | 3 | 0.600 | 4 | 0.800 | 0.6857 | 0.3769 | 1,1,,4,2 |
| el_e5 | orders | pod-kill | 5 | 1 | 0.200 | 2 | 0.400 | 0.3429 | 0.3681 | 1,,5,6, |
| el_e4 | payment | cpu-stress | 3 | 0 | 0.000 | 2 | 0.667 | 0.4286 | 0.3086 | 4,3, |
| el_e13 | carts | network-loss | 3 | 1 | 0.333 | 2 | 0.667 | 0.4762 | 0.4096 | 5,,1 |
