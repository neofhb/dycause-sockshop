# Mesh Extended Legacy Data Quality

Scope: `data/sockshop_mesh_extended/`. This report checks collected data quality only; it does not select experiments by Top-K performance.

## Overall

- Run directories scanned: 87
- Quality-valid runs: 87/87
- Main-parameter DyCause successful rows: 87/87
- Lowest actual service valid ratio: 0.975
- Total missing points across all services/runs: 44
- Total zero points across all services/runs: 0

## By Load Profile

| load_profile         |   runs |   valid |   min_actual_valid_ratio |   missing_points |   zero_points |
|:---------------------|-------:|--------:|-------------------------:|-----------------:|--------------:|
| legacy-compressed-v0 |     23 |      23 |                    1     |                0 |             0 |
| legacy-compressed-v1 |     64 |      64 |                    0.975 |               44 |             0 |

## Raw Shape

| raw_shape   |   runs |
|:------------|-------:|
| 600x7       |     83 |
| 1200x7      |      4 |

## Runs Below 100% Actual Valid Ratio

| experiment   | run   | load_profile         |   min_valid_ratio |   missing_points_total |   zero_points_total | raw_shape   |
|:-------------|:------|:---------------------|------------------:|-----------------------:|--------------------:|:------------|
| el_e11       | run01 | legacy-compressed-v1 |          0.99     |                      6 |                   0 | 600x7       |
| el_e5        | run03 | legacy-compressed-v1 |          0.995    |                      3 |                   0 | 600x7       |
| el_e5        | run06 | legacy-compressed-v1 |          0.995    |                      3 |                   0 | 600x7       |
| el_e5        | run08 | legacy-compressed-v1 |          0.995    |                      3 |                   0 | 600x7       |
| mesh_e1      | run07 | legacy-compressed-v1 |          0.975    |                     15 |                   0 | 600x7       |
| mesh_e1      | run08 | legacy-compressed-v1 |          0.991667 |                      5 |                   0 | 600x7       |
| mesh_e2      | run04 | legacy-compressed-v1 |          0.985    |                      9 |                   0 | 600x7       |

## By Experiment

| experiment   |   runs |   valid |   min_actual_valid_ratio |   missing_points |   zero_points |
|:-------------|-------:|--------:|-------------------------:|-----------------:|--------------:|
| el_e1        |      1 |       1 |                    1     |                0 |             0 |
| el_e10       |      1 |       1 |                    1     |                0 |             0 |
| el_e11       |      1 |       1 |                    0.99  |                6 |             0 |
| el_e12       |      1 |       1 |                    1     |                0 |             0 |
| el_e13       |     10 |      10 |                    1     |                0 |             0 |
| el_e14       |      1 |       1 |                    1     |                0 |             0 |
| el_e15       |      1 |       1 |                    1     |                0 |             0 |
| el_e16       |      1 |       1 |                    1     |                0 |             0 |
| el_e2        |     10 |      10 |                    1     |                0 |             0 |
| el_e3        |      1 |       1 |                    1     |                0 |             0 |
| el_e4        |     10 |      10 |                    1     |                0 |             0 |
| el_e5        |     10 |      10 |                    0.995 |                9 |             0 |
| el_e6        |      1 |       1 |                    1     |                0 |             0 |
| el_e7        |      1 |       1 |                    1     |                0 |             0 |
| el_e8        |      1 |       1 |                    1     |                0 |             0 |
| el_e9        |      1 |       1 |                    1     |                0 |             0 |
| mesh_e1      |     10 |      10 |                    0.975 |               20 |             0 |
| mesh_e2      |      5 |       5 |                    0.985 |                9 |             0 |
| mesh_e3      |     10 |      10 |                    1     |                0 |             0 |
| mesh_e4      |      3 |       3 |                    1     |                0 |             0 |
| mesh_e5      |      7 |       7 |                    1     |                0 |             0 |