# Selected Sensitivity Results

Selected runs: `el_e2, el_e5, el_e4, el_e13, el_e6, el_e11`.

## Best Parameter Aggregates

| lag | step | edge | rows | PR@2 hits | PR@5 hits | Top-2 rate | Top-5 rate | Acc mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 30 | 0.8 | 6 | 2 | 4 | 0.333 | 0.667 | 0.5238 |
| 7 | 30 | 0.6 | 6 | 2 | 4 | 0.333 | 0.667 | 0.5000 |
| 3 | 60 | 0.6 | 6 | 2 | 2 | 0.333 | 0.333 | 0.3095 |
| 5 | 60 | 0.8 | 6 | 1 | 4 | 0.167 | 0.667 | 0.4286 |
| 5 | 30 | 0.8 | 6 | 1 | 3 | 0.167 | 0.500 | 0.4048 |
| 3 | 20 | 0.8 | 6 | 1 | 3 | 0.167 | 0.500 | 0.3810 |
| 3 | 30 | 0.8 | 6 | 1 | 3 | 0.167 | 0.500 | 0.3810 |
| 3 | 20 | 0.6 | 6 | 1 | 3 | 0.167 | 0.500 | 0.3809 |
| 5 | 20 | 0.8 | 6 | 1 | 3 | 0.167 | 0.500 | 0.3809 |
| 3 | 60 | 0.8 | 6 | 1 | 3 | 0.167 | 0.500 | 0.3333 |
| 7 | 60 | 0.8 | 6 | 1 | 2 | 0.167 | 0.333 | 0.3095 |
| 7 | 60 | 0.6 | 6 | 1 | 2 | 0.167 | 0.333 | 0.2619 |

## Best Per Experiment

| experiment | root | fault | best params | root rank | PR@2 | PR@5 | Acc |
|---|---|---|---|---:|---:|---:|---:|
| el_e2 | payment | network-corrupt | lag=7, step=30, edge=0.8 | 1 | 1.0000 | 1.0000 | 1.0000 |
| el_e5 | orders | pod-kill | lag=3, step=20, edge=0.8 | 1 | 1.0000 | 1.0000 | 1.0000 |
| el_e4 | payment | cpu-stress | lag=5, step=20, edge=0.8 | 3 | 0.0000 | 1.0000 | 0.7143 |
| el_e13 | carts | network-loss | lag=5, step=30, edge=0.8 | 3 | 0.0000 | 1.0000 | 0.7143 |
| el_e6 | orders | network-delay | lag=3, step=60, edge=0.8 | 4 | 0.0000 | 1.0000 | 0.5714 |
| el_e11 | carts | pod-kill | lag=5, step=20, edge=0.4 | 4 | 0.0000 | 1.0000 | 0.5714 |
