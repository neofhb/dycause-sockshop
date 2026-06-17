# Algorithm Effect Under Main Parameters

Scope: quality-valid and DyCause-successful runs in `data/sockshop_mesh_extended/summary.csv`. Main parameters: `lag=7`, `step=30`, `edge_thres=0.8`.

## Overall

- All valid main-param runs: n=87, Top-1=13.8%, Top-2=21.8%, Top-5=35.6%, Acc=0.310 +/- 0.393
- Repeated groups only (>=5 runs): n=67, Top-1=14.9%, Top-2=25.4%, Top-5=43.3%, Acc=0.367 +/- 0.400
- Currently selected effective groups (`mesh_e1, mesh_e3, el_e2, el_e5, el_e4, el_e13`): n=60, Top-1=16.7%, Top-2=26.7%, Top-5=46.7%, Acc=0.393 +/- 0.403

## By Experiment

| experiment   | root      | fault_type        | load_profile         |   runs |   top1 |   top2 |   top5 | pr1_rate   | pr2_rate   | pr5_rate   |   acc_mean |   acc_std |   rank_mean |   rank_min |   rank_max |
|:-------------|:----------|:------------------|:---------------------|-------:|-------:|-------:|-------:|:-----------|:-----------|:-----------|-----------:|----------:|------------:|-----------:|-----------:|
| mesh_e1      | payment   | pod-kill          | legacy-compressed-v0 |      6 |      4 |      5 |      5 | 66.7%      | 83.3%      | 83.3%      |      0.81  |     0.401 |       1.2   |          1 |          2 |
| mesh_e3      | payment   | network-delay     | legacy-compressed-v0 |      6 |      2 |      3 |      4 | 33.3%      | 50.0%      | 66.7%      |      0.548 |     0.473 |       2.25  |          1 |          5 |
| mesh_e2      | user      | pod-kill          | legacy-compressed-v1 |      2 |      1 |      1 |      1 | 50.0%      | 50.0%      | 50.0%      |      0.5   |     0.707 |       1     |          1 |          1 |
| mesh_e2      | user      | pod-kill          | legacy-compressed-v0 |      3 |      1 |      1 |      1 | 33.3%      | 33.3%      | 33.3%      |      0.333 |     0.577 |       1     |          1 |          1 |
| el_e2        | payment   | network-corrupt   | legacy-compressed-v1 |     10 |      2 |      3 |      5 | 20.0%      | 30.0%      | 50.0%      |      0.4   |     0.446 |       2.4   |          1 |          4 |
| mesh_e3      | payment   | network-delay     | legacy-compressed-v1 |      4 |      0 |      1 |      2 | 0.0%       | 25.0%      | 50.0%      |      0.393 |     0.393 |       4.333 |          2 |          7 |
| el_e5        | orders    | pod-kill          | legacy-compressed-v1 |     10 |      1 |      2 |      6 | 10.0%      | 20.0%      | 60.0%      |      0.457 |     0.374 |       3.429 |          1 |          6 |
| el_e13       | carts     | network-loss      | legacy-compressed-v1 |     10 |      1 |      2 |      3 | 10.0%      | 20.0%      | 30.0%      |      0.257 |     0.386 |       3.5   |          1 |          6 |
| mesh_e5      | catalogue | network-delay     | legacy-compressed-v0 |      5 |      0 |      1 |      1 | 0.0%       | 20.0%      | 20.0%      |      0.171 |     0.383 |       2     |          2 |          2 |
| el_e4        | payment   | cpu-stress        | legacy-compressed-v1 |     10 |      0 |      0 |      3 | 0.0%       | 0.0%       | 30.0%      |      0.243 |     0.278 |       5.167 |          3 |          7 |
| el_e16       | carts     | cpu-stress        | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.286 |     0     |       6     |          6 |          6 |
| el_e6        | orders    | network-delay     | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.143 |     0     |       7     |          7 |          7 |
| mesh_e5      | catalogue | network-delay     | legacy-compressed-v1 |      2 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.071 |     0.101 |       7     |          7 |          7 |
| mesh_e1      | payment   | pod-kill          | legacy-compressed-v1 |      4 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.071 |     0.143 |       6     |          6 |          6 |
| mesh_e4      | user      | network-delay     | legacy-compressed-v0 |      3 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e1        | payment   | network-loss      | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e10       | orders    | cpu-stress        | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e11       | carts     | pod-kill          | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e12       | carts     | network-delay     | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e14       | carts     | network-corrupt   | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e15       | carts     | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e3        | payment   | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e7        | orders    | network-loss      | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e8        | orders    | network-corrupt   | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |
| el_e9        | orders    | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |     nan     |        nan |        nan |

## Stable Positive Candidates

| experiment   | root    | fault_type   | load_profile         |   runs |   top1 |   top2 |   top5 | pr1_rate   | pr2_rate   | pr5_rate   |   acc_mean |   acc_std |   rank_mean |   rank_min |   rank_max |
|:-------------|:--------|:-------------|:---------------------|-------:|-------:|-------:|-------:|:-----------|:-----------|:-----------|-----------:|----------:|------------:|-----------:|-----------:|
| mesh_e1      | payment | pod-kill     | legacy-compressed-v0 |      6 |      4 |      5 |      5 | 66.7%      | 83.3%      | 83.3%      |       0.81 |     0.401 |         1.2 |          1 |          2 |

## Negative Cases (Top-5 = 0)

| experiment   | root      | fault_type        | load_profile         |   runs |   top1 |   top2 |   top5 | pr1_rate   | pr2_rate   | pr5_rate   |   acc_mean |   acc_std |   rank_mean |   rank_min |   rank_max |
|:-------------|:----------|:------------------|:---------------------|-------:|-------:|-------:|-------:|:-----------|:-----------|:-----------|-----------:|----------:|------------:|-----------:|-----------:|
| el_e16       | carts     | cpu-stress        | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.286 |     0     |           6 |          6 |          6 |
| el_e6        | orders    | network-delay     | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.143 |     0     |           7 |          7 |          7 |
| mesh_e5      | catalogue | network-delay     | legacy-compressed-v1 |      2 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.071 |     0.101 |           7 |          7 |          7 |
| mesh_e1      | payment   | pod-kill          | legacy-compressed-v1 |      4 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0.071 |     0.143 |           6 |          6 |          6 |
| mesh_e4      | user      | network-delay     | legacy-compressed-v0 |      3 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e1        | payment   | network-loss      | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e10       | orders    | cpu-stress        | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e11       | carts     | pod-kill          | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e12       | carts     | network-delay     | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e14       | carts     | network-corrupt   | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e15       | carts     | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e3        | payment   | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e7        | orders    | network-loss      | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e8        | orders    | network-corrupt   | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |
| el_e9        | orders    | network-duplicate | legacy-compressed-v1 |      1 |      0 |      0 |      0 | 0.0%       | 0.0%       | 0.0%       |      0     |     0     |         nan |        nan |        nan |