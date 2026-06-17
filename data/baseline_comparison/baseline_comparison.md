# DyCause vs Baselines

随机基线为期望命中率：单一真根因在候选集合中均匀随机排序时，Top-K 命中率为 `min(K, N) / N`。

## Aggregate

| Dataset | Method | Runs | Top-2 Hit | Top-5 Hit | Acc |
|---|---|---:|---:|---:|---:|
| sockshop_4svc | anomaly_z_mean_shift | 2 | 0.5000 | 1.0000 | 0.6250 |
| sockshop_4svc | dycause | 2 | 1.0000 | 1.0000 | 0.7500 |
| sockshop_4svc | pearson_entry_abs | 2 | 0.5000 | 1.0000 | 0.7500 |
| sockshop_4svc | random_expected | 2 | 0.6667 | 1.0000 | 0.7500 |
| sockshop_mesh_business | anomaly_z_mean_shift | 5 | 0.4000 | 1.0000 | 0.6857 |
| sockshop_mesh_business | dycause | 5 | 0.4000 | 0.4000 | 0.3428 |
| sockshop_mesh_business | pearson_entry_abs | 5 | 0.4000 | 1.0000 | 0.7714 |
| sockshop_mesh_business | random_expected | 5 | 0.3333 | 0.8333 | 0.6429 |
| sockshop_mesh_extended | anomaly_z_mean_shift | 87 | 0.6782 | 0.9080 | 0.8161 |
| sockshop_mesh_extended | dycause | 87 | 0.2184 | 0.3563 | 0.3103 |
| sockshop_mesh_extended | pearson_entry_abs | 87 | 0.3793 | 0.7586 | 0.6289 |
| sockshop_mesh_extended | random_expected | 87 | 0.3333 | 0.8333 | 0.6429 |

## Per Run

| Dataset | Experiment | Run | Root | Method | Rank | Top-2 | Top-5 | Acc | Top Services |
|---|---|---|---|---|---:|---:|---:|---:|---|
| sockshop_4svc | e1 | single | payment | random_expected | expected | 0.6667 | 1.0000 | 0.7500 | random permutation |
| sockshop_4svc | e1 | single | payment | dycause | 2 | 1.0000 | 1.0000 | 0.7500 |  |
| sockshop_4svc | e1 | single | payment | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.5000 | user > catalogue > payment |
| sockshop_4svc | e1 | single | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.7500 | user > payment > catalogue |
| sockshop_4svc | e2 | single | user | random_expected | expected | 0.6667 | 1.0000 | 0.7500 | random permutation |
| sockshop_4svc | e2 | single | user | dycause | 2 | 1.0000 | 1.0000 | 0.7500 |  |
| sockshop_4svc | e2 | single | user | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | user > catalogue > payment |
| sockshop_4svc | e2 | single | user | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.5000 | catalogue > payment > user |
| sockshop_mesh_business | mesh_e1 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_business | mesh_e1 | run01 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_business | mesh_e1 | run01 | payment | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | user > catalogue > payment > orders > carts > shipping |
| sockshop_mesh_business | mesh_e1 | run01 | payment | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | catalogue > orders > carts > user > payment > shipping |
| sockshop_mesh_business | mesh_e2 | run01 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_business | mesh_e2 | run01 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_business | mesh_e2 | run01 | user | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | orders > shipping > carts > catalogue > user > payment |
| sockshop_mesh_business | mesh_e2 | run01 | user | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | shipping > carts > orders > user > payment > catalogue |
| sockshop_mesh_business | mesh_e3 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_business | mesh_e3 | run01 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_business | mesh_e3 | run01 | payment | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | user > carts > payment > shipping > catalogue > orders |
| sockshop_mesh_business | mesh_e3 | run01 | payment | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | shipping > carts > user > orders > payment > catalogue |
| sockshop_mesh_business | mesh_e4 | run01 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_business | mesh_e4 | run01 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_business | mesh_e4 | run01 | user | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | user > orders > payment > carts > shipping > catalogue |
| sockshop_mesh_business | mesh_e4 | run01 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > orders > carts > catalogue > shipping |
| sockshop_mesh_business | mesh_e5 | run01 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_business | mesh_e5 | run01 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_business | mesh_e5 | run01 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > carts > orders > shipping > payment > user |
| sockshop_mesh_business | mesh_e5 | run01 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > carts > orders > payment > shipping > user |
| sockshop_mesh_extended | el_e1 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e1 | run01 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e1 | run01 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > catalogue > carts > orders > shipping |
| sockshop_mesh_extended | el_e1 | run01 | payment | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | carts > orders > catalogue > user > payment > shipping |
| sockshop_mesh_extended | el_e10 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e10 | run01 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e10 | run01 | orders | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | payment > catalogue > orders > carts > user > shipping |
| sockshop_mesh_extended | el_e10 | run01 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > catalogue > user > carts > shipping > payment |
| sockshop_mesh_extended | el_e11 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e11 | run01 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e11 | run01 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > user > payment > shipping > orders > carts |
| sockshop_mesh_extended | el_e11 | run01 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > catalogue > user > payment > orders > shipping |
| sockshop_mesh_extended | el_e12 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e12 | run01 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e12 | run01 | carts | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | orders > catalogue > user > payment > carts > shipping |
| sockshop_mesh_extended | el_e12 | run01 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > payment > catalogue > shipping > user > orders |
| sockshop_mesh_extended | el_e13 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run01 | carts | dycause | 5 | 0.0000 | 1.0000 | 0.4286 |  |
| sockshop_mesh_extended | el_e13 | run01 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > user > orders > payment > shipping > carts |
| sockshop_mesh_extended | el_e13 | run01 | carts | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | orders > user > shipping > payment > catalogue > carts |
| sockshop_mesh_extended | el_e13 | run02 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run02 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run02 | carts | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | orders > shipping > catalogue > user > carts > payment |
| sockshop_mesh_extended | el_e13 | run02 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > user > shipping > catalogue > orders > payment |
| sockshop_mesh_extended | el_e13 | run03 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run03 | carts | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | el_e13 | run03 | carts | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | orders > user > catalogue > carts > shipping > payment |
| sockshop_mesh_extended | el_e13 | run03 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > payment > shipping > catalogue > user > orders |
| sockshop_mesh_extended | el_e13 | run04 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run04 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run04 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > user > payment > shipping > orders > carts |
| sockshop_mesh_extended | el_e13 | run04 | carts | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | payment > user > shipping > orders > catalogue > carts |
| sockshop_mesh_extended | el_e13 | run05 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run05 | carts | dycause | 6 | 0.0000 | 0.0000 | 0.2857 |  |
| sockshop_mesh_extended | el_e13 | run05 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | orders > shipping > user > catalogue > payment > carts |
| sockshop_mesh_extended | el_e13 | run05 | carts | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | payment > catalogue > user > shipping > carts > orders |
| sockshop_mesh_extended | el_e13 | run06 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run06 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run06 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > orders > payment > user > shipping > carts |
| sockshop_mesh_extended | el_e13 | run06 | carts | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | payment > catalogue > carts > orders > user > shipping |
| sockshop_mesh_extended | el_e13 | run07 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run07 | carts | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | el_e13 | run07 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | user > orders > payment > catalogue > shipping > carts |
| sockshop_mesh_extended | el_e13 | run07 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > shipping > user > catalogue > payment > orders |
| sockshop_mesh_extended | el_e13 | run08 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run08 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run08 | carts | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | orders > catalogue > user > payment > carts > shipping |
| sockshop_mesh_extended | el_e13 | run08 | carts | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | user > carts > shipping > orders > payment > catalogue |
| sockshop_mesh_extended | el_e13 | run09 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run09 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run09 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | user > payment > orders > shipping > catalogue > carts |
| sockshop_mesh_extended | el_e13 | run09 | carts | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | user > shipping > payment > catalogue > orders > carts |
| sockshop_mesh_extended | el_e13 | run10 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e13 | run10 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e13 | run10 | carts | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | user > orders > catalogue > carts > shipping > payment |
| sockshop_mesh_extended | el_e13 | run10 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > catalogue > orders > shipping > payment > user |
| sockshop_mesh_extended | el_e14 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e14 | run01 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e14 | run01 | carts | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | payment > shipping > carts > orders > user > catalogue |
| sockshop_mesh_extended | el_e14 | run01 | carts | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | shipping > carts > catalogue > user > orders > payment |
| sockshop_mesh_extended | el_e15 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e15 | run01 | carts | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e15 | run01 | carts | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | catalogue > user > payment > orders > carts > shipping |
| sockshop_mesh_extended | el_e15 | run01 | carts | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | orders > payment > carts > catalogue > user > shipping |
| sockshop_mesh_extended | el_e16 | run01 | carts | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e16 | run01 | carts | dycause | 6 | 0.0000 | 0.0000 | 0.2857 |  |
| sockshop_mesh_extended | el_e16 | run01 | carts | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | user > orders > catalogue > shipping > payment > carts |
| sockshop_mesh_extended | el_e16 | run01 | carts | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | carts > shipping > user > payment > catalogue > orders |
| sockshop_mesh_extended | el_e2 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run01 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | el_e2 | run01 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > user > shipping > carts > orders |
| sockshop_mesh_extended | el_e2 | run01 | payment | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | shipping > carts > user > payment > catalogue > orders |
| sockshop_mesh_extended | el_e2 | run02 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run02 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | el_e2 | run02 | payment | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | catalogue > orders > user > payment > carts > shipping |
| sockshop_mesh_extended | el_e2 | run02 | payment | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | shipping > orders > carts > catalogue > payment > user |
| sockshop_mesh_extended | el_e2 | run03 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run03 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e2 | run03 | payment | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | shipping > carts > orders > user > payment > catalogue |
| sockshop_mesh_extended | el_e2 | run03 | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > orders > shipping > catalogue > carts |
| sockshop_mesh_extended | el_e2 | run04 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run04 | payment | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | el_e2 | run04 | payment | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | user > orders > catalogue > payment > shipping > carts |
| sockshop_mesh_extended | el_e2 | run04 | payment | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | orders > catalogue > payment > shipping > user > carts |
| sockshop_mesh_extended | el_e2 | run05 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run05 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | el_e2 | run05 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > orders > user > carts > shipping |
| sockshop_mesh_extended | el_e2 | run05 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > catalogue > orders > user > shipping |
| sockshop_mesh_extended | el_e2 | run06 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run06 | payment | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | el_e2 | run06 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > carts > orders > catalogue > shipping |
| sockshop_mesh_extended | el_e2 | run06 | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | carts > payment > shipping > user > orders > catalogue |
| sockshop_mesh_extended | el_e2 | run07 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run07 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e2 | run07 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > shipping > orders > user > carts |
| sockshop_mesh_extended | el_e2 | run07 | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | shipping > payment > orders > catalogue > carts > user |
| sockshop_mesh_extended | el_e2 | run08 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run08 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e2 | run08 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | orders > payment > shipping > catalogue > carts > user |
| sockshop_mesh_extended | el_e2 | run08 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > user > shipping > orders > carts |
| sockshop_mesh_extended | el_e2 | run09 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run09 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e2 | run09 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > orders > catalogue > shipping > carts |
| sockshop_mesh_extended | el_e2 | run09 | payment | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | carts > catalogue > user > payment > orders > shipping |
| sockshop_mesh_extended | el_e2 | run10 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e2 | run10 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e2 | run10 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | carts > catalogue > user > shipping > orders > payment |
| sockshop_mesh_extended | el_e2 | run10 | payment | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | carts > shipping > user > payment > catalogue > orders |
| sockshop_mesh_extended | el_e3 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e3 | run01 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e3 | run01 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > orders > user > shipping > carts |
| sockshop_mesh_extended | el_e3 | run01 | payment | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | carts > shipping > orders > user > catalogue > payment |
| sockshop_mesh_extended | el_e4 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run01 | payment | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | el_e4 | run01 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > user > orders > carts > shipping |
| sockshop_mesh_extended | el_e4 | run01 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > user > catalogue > orders > carts > shipping |
| sockshop_mesh_extended | el_e4 | run02 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run02 | payment | dycause | 3 | 0.0000 | 1.0000 | 0.7143 |  |
| sockshop_mesh_extended | el_e4 | run02 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | shipping > catalogue > user > orders > carts > payment |
| sockshop_mesh_extended | el_e4 | run02 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > orders > user > catalogue > shipping |
| sockshop_mesh_extended | el_e4 | run03 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run03 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e4 | run03 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | orders > user > shipping > catalogue > carts > payment |
| sockshop_mesh_extended | el_e4 | run03 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > user > catalogue > orders > shipping |
| sockshop_mesh_extended | el_e4 | run04 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run04 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e4 | run04 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > orders > user > shipping > carts > payment |
| sockshop_mesh_extended | el_e4 | run04 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > shipping > user > carts > orders |
| sockshop_mesh_extended | el_e4 | run05 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run05 | payment | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | el_e4 | run05 | payment | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | user > orders > carts > catalogue > payment > shipping |
| sockshop_mesh_extended | el_e4 | run05 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > user > shipping > catalogue > orders > carts |
| sockshop_mesh_extended | el_e4 | run06 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run06 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e4 | run06 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | orders > shipping > user > catalogue > carts > payment |
| sockshop_mesh_extended | el_e4 | run06 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > orders > shipping > user > catalogue |
| sockshop_mesh_extended | el_e4 | run07 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run07 | payment | dycause | 6 | 0.0000 | 0.0000 | 0.2857 |  |
| sockshop_mesh_extended | el_e4 | run07 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > orders > carts > user > shipping > payment |
| sockshop_mesh_extended | el_e4 | run07 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > carts > orders > user > shipping |
| sockshop_mesh_extended | el_e4 | run08 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run08 | payment | dycause | 7 | 0.0000 | 0.0000 | 0.1429 |  |
| sockshop_mesh_extended | el_e4 | run08 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | user > catalogue > carts > orders > shipping > payment |
| sockshop_mesh_extended | el_e4 | run08 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > orders > user > carts > shipping |
| sockshop_mesh_extended | el_e4 | run09 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run09 | payment | dycause | 7 | 0.0000 | 0.0000 | 0.1429 |  |
| sockshop_mesh_extended | el_e4 | run09 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > carts > shipping > orders > user > payment |
| sockshop_mesh_extended | el_e4 | run09 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > carts > catalogue > shipping > user |
| sockshop_mesh_extended | el_e4 | run10 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e4 | run10 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e4 | run10 | payment | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | catalogue > orders > user > shipping > carts > payment |
| sockshop_mesh_extended | el_e4 | run10 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > user > catalogue > shipping > carts |
| sockshop_mesh_extended | el_e5 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run01 | orders | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | el_e5 | run01 | orders | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | catalogue > user > orders > carts > payment > shipping |
| sockshop_mesh_extended | el_e5 | run01 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > payment > user > catalogue > carts > shipping |
| sockshop_mesh_extended | el_e5 | run02 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run02 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e5 | run02 | orders | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | user > catalogue > shipping > orders > payment > carts |
| sockshop_mesh_extended | el_e5 | run02 | orders | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | user > orders > catalogue > shipping > carts > payment |
| sockshop_mesh_extended | el_e5 | run03 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run03 | orders | dycause | 5 | 0.0000 | 1.0000 | 0.4286 |  |
| sockshop_mesh_extended | el_e5 | run03 | orders | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | catalogue > user > carts > orders > payment > shipping |
| sockshop_mesh_extended | el_e5 | run03 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > carts > payment > catalogue > shipping > user |
| sockshop_mesh_extended | el_e5 | run04 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run04 | orders | dycause | 6 | 0.0000 | 0.0000 | 0.2857 |  |
| sockshop_mesh_extended | el_e5 | run04 | orders | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | carts > catalogue > user > payment > orders > shipping |
| sockshop_mesh_extended | el_e5 | run04 | orders | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | carts > user > catalogue > orders > payment > shipping |
| sockshop_mesh_extended | el_e5 | run05 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run05 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e5 | run05 | orders | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | user > catalogue > shipping > payment > orders > carts |
| sockshop_mesh_extended | el_e5 | run05 | orders | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | carts > orders > user > shipping > catalogue > payment |
| sockshop_mesh_extended | el_e5 | run06 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run06 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e5 | run06 | orders | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > orders > catalogue > payment > shipping > carts |
| sockshop_mesh_extended | el_e5 | run06 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > carts > payment > user > catalogue > shipping |
| sockshop_mesh_extended | el_e5 | run07 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run07 | orders | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | el_e5 | run07 | orders | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | catalogue > user > orders > payment > shipping > carts |
| sockshop_mesh_extended | el_e5 | run07 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > payment > carts > user > catalogue > shipping |
| sockshop_mesh_extended | el_e5 | run08 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run08 | orders | dycause | 3 | 0.0000 | 1.0000 | 0.7143 |  |
| sockshop_mesh_extended | el_e5 | run08 | orders | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | user > catalogue > shipping > orders > payment > carts |
| sockshop_mesh_extended | el_e5 | run08 | orders | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | catalogue > user > orders > shipping > payment > carts |
| sockshop_mesh_extended | el_e5 | run09 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run09 | orders | dycause | 3 | 0.0000 | 1.0000 | 0.7143 |  |
| sockshop_mesh_extended | el_e5 | run09 | orders | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | payment > catalogue > user > carts > orders > shipping |
| sockshop_mesh_extended | el_e5 | run09 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > payment > catalogue > carts > shipping > user |
| sockshop_mesh_extended | el_e5 | run10 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e5 | run10 | orders | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | el_e5 | run10 | orders | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | user > catalogue > orders > shipping > payment > carts |
| sockshop_mesh_extended | el_e5 | run10 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > user > catalogue > shipping > carts > payment |
| sockshop_mesh_extended | el_e6 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e6 | run01 | orders | dycause | 7 | 0.0000 | 0.0000 | 0.1429 |  |
| sockshop_mesh_extended | el_e6 | run01 | orders | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | shipping > catalogue > user > payment > carts > orders |
| sockshop_mesh_extended | el_e6 | run01 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > carts > catalogue > user > shipping > payment |
| sockshop_mesh_extended | el_e7 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e7 | run01 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e7 | run01 | orders | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | user > catalogue > payment > shipping > orders > carts |
| sockshop_mesh_extended | el_e7 | run01 | orders | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | payment > catalogue > user > shipping > orders > carts |
| sockshop_mesh_extended | el_e8 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e8 | run01 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e8 | run01 | orders | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | orders > user > payment > carts > catalogue > shipping |
| sockshop_mesh_extended | el_e8 | run01 | orders | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | shipping > carts > payment > orders > catalogue > user |
| sockshop_mesh_extended | el_e9 | run01 | orders | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | el_e9 | run01 | orders | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | el_e9 | run01 | orders | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > orders > catalogue > payment > carts > shipping |
| sockshop_mesh_extended | el_e9 | run01 | orders | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | orders > user > catalogue > shipping > carts > payment |
| sockshop_mesh_extended | mesh_e1 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run01 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | mesh_e1 | run01 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > orders > user > catalogue > shipping |
| sockshop_mesh_extended | mesh_e1 | run01 | payment | anomaly_z_mean_shift | 4 | 0.0000 | 1.0000 | 0.5714 | shipping > catalogue > user > payment > carts > orders |
| sockshop_mesh_extended | mesh_e1 | run02 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run02 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run02 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | carts > payment > shipping > user > catalogue > orders |
| sockshop_mesh_extended | mesh_e1 | run02 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > carts > orders > user > shipping |
| sockshop_mesh_extended | mesh_e1 | run03 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run03 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run03 | payment | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | user > catalogue > orders > payment > carts > shipping |
| sockshop_mesh_extended | mesh_e1 | run03 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > user > orders > carts > shipping |
| sockshop_mesh_extended | mesh_e1 | run04 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run04 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run04 | payment | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | shipping > catalogue > payment > user > carts > orders |
| sockshop_mesh_extended | mesh_e1 | run04 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > shipping > catalogue > user > orders |
| sockshop_mesh_extended | mesh_e1 | run05 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run05 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run05 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > user > catalogue > shipping > orders |
| sockshop_mesh_extended | mesh_e1 | run05 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > catalogue > shipping > user > carts |
| sockshop_mesh_extended | mesh_e1 | run06 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run06 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run06 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > orders > carts > catalogue > shipping |
| sockshop_mesh_extended | mesh_e1 | run06 | payment | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | catalogue > shipping > payment > orders > carts > user |
| sockshop_mesh_extended | mesh_e1 | run07 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run07 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run07 | payment | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | catalogue > user > carts > orders > payment > shipping |
| sockshop_mesh_extended | mesh_e1 | run07 | payment | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | carts > user > catalogue > orders > shipping > payment |
| sockshop_mesh_extended | mesh_e1 | run08 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run08 | payment | dycause | 6 | 0.0000 | 0.0000 | 0.2857 |  |
| sockshop_mesh_extended | mesh_e1 | run08 | payment | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | orders > shipping > user > catalogue > payment > carts |
| sockshop_mesh_extended | mesh_e1 | run08 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > shipping > catalogue > carts > user |
| sockshop_mesh_extended | mesh_e1 | run09 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run09 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run09 | payment | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | user > catalogue > carts > orders > payment > shipping |
| sockshop_mesh_extended | mesh_e1 | run09 | payment | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | shipping > orders > carts > user > catalogue > payment |
| sockshop_mesh_extended | mesh_e1 | run10 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e1 | run10 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e1 | run10 | payment | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | catalogue > user > orders > payment > shipping > carts |
| sockshop_mesh_extended | mesh_e1 | run10 | payment | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | carts > orders > user > catalogue > shipping > payment |
| sockshop_mesh_extended | mesh_e2 | run01 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e2 | run01 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e2 | run01 | user | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | payment > carts > orders > user > catalogue > shipping |
| sockshop_mesh_extended | mesh_e2 | run01 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > orders > catalogue > carts > shipping |
| sockshop_mesh_extended | mesh_e2 | run02 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e2 | run02 | user | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e2 | run02 | user | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | payment > orders > catalogue > carts > shipping > user |
| sockshop_mesh_extended | mesh_e2 | run02 | user | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | payment > orders > shipping > catalogue > user > carts |
| sockshop_mesh_extended | mesh_e2 | run03 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e2 | run03 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e2 | run03 | user | pearson_entry_abs | 5 | 0.0000 | 1.0000 | 0.4286 | payment > shipping > carts > orders > user > catalogue |
| sockshop_mesh_extended | mesh_e2 | run03 | user | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | catalogue > orders > payment > shipping > user > carts |
| sockshop_mesh_extended | mesh_e2 | run04 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e2 | run04 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e2 | run04 | user | pearson_entry_abs | 3 | 0.0000 | 1.0000 | 0.7143 | orders > payment > user > catalogue > carts > shipping |
| sockshop_mesh_extended | mesh_e2 | run04 | user | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | shipping > user > carts > orders > payment > catalogue |
| sockshop_mesh_extended | mesh_e2 | run05 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e2 | run05 | user | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e2 | run05 | user | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | orders > catalogue > carts > user > payment > shipping |
| sockshop_mesh_extended | mesh_e2 | run05 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > catalogue > shipping > carts > orders > payment |
| sockshop_mesh_extended | mesh_e3 | run01 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run01 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e3 | run01 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > orders > carts > user > shipping |
| sockshop_mesh_extended | mesh_e3 | run01 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > catalogue > orders > shipping > user |
| sockshop_mesh_extended | mesh_e3 | run02 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run02 | payment | dycause | 5 | 0.0000 | 1.0000 | 0.4286 |  |
| sockshop_mesh_extended | mesh_e3 | run02 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > catalogue > shipping > user > orders > carts |
| sockshop_mesh_extended | mesh_e3 | run02 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > catalogue > carts > user > shipping |
| sockshop_mesh_extended | mesh_e3 | run03 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run03 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e3 | run03 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > catalogue > user > orders > shipping |
| sockshop_mesh_extended | mesh_e3 | run03 | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | carts > payment > orders > shipping > catalogue > user |
| sockshop_mesh_extended | mesh_e3 | run04 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run04 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | mesh_e3 | run04 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > orders > shipping > catalogue > user |
| sockshop_mesh_extended | mesh_e3 | run04 | payment | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | shipping > payment > user > catalogue > orders > carts |
| sockshop_mesh_extended | mesh_e3 | run05 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run05 | payment | dycause | 1 | 1.0000 | 1.0000 | 1.0000 |  |
| sockshop_mesh_extended | mesh_e3 | run05 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > user > orders > catalogue > carts > shipping |
| sockshop_mesh_extended | mesh_e3 | run05 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > carts > user > catalogue > shipping |
| sockshop_mesh_extended | mesh_e3 | run06 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run06 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e3 | run06 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > shipping > catalogue > orders > carts > user |
| sockshop_mesh_extended | mesh_e3 | run06 | payment | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | payment > carts > catalogue > orders > user > shipping |
| sockshop_mesh_extended | mesh_e3 | run07 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run07 | payment | dycause | 7 | 0.0000 | 0.0000 | 0.1429 |  |
| sockshop_mesh_extended | mesh_e3 | run07 | payment | pearson_entry_abs | 4 | 0.0000 | 1.0000 | 0.5714 | orders > carts > catalogue > payment > shipping > user |
| sockshop_mesh_extended | mesh_e3 | run07 | payment | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | shipping > orders > payment > user > carts > catalogue |
| sockshop_mesh_extended | mesh_e3 | run08 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run08 | payment | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | mesh_e3 | run08 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | user > payment > catalogue > orders > shipping > carts |
| sockshop_mesh_extended | mesh_e3 | run08 | payment | anomaly_z_mean_shift | 3 | 0.0000 | 1.0000 | 0.7143 | user > catalogue > payment > carts > orders > shipping |
| sockshop_mesh_extended | mesh_e3 | run09 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run09 | payment | dycause | 4 | 0.0000 | 1.0000 | 0.5714 |  |
| sockshop_mesh_extended | mesh_e3 | run09 | payment | pearson_entry_abs | 2 | 1.0000 | 1.0000 | 0.8571 | catalogue > payment > orders > shipping > user > carts |
| sockshop_mesh_extended | mesh_e3 | run09 | payment | anomaly_z_mean_shift | 6 | 0.0000 | 0.0000 | 0.2857 | user > shipping > orders > carts > catalogue > payment |
| sockshop_mesh_extended | mesh_e3 | run10 | payment | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e3 | run10 | payment | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e3 | run10 | payment | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | payment > orders > shipping > catalogue > user > carts |
| sockshop_mesh_extended | mesh_e3 | run10 | payment | anomaly_z_mean_shift | 5 | 0.0000 | 1.0000 | 0.4286 | carts > orders > user > catalogue > payment > shipping |
| sockshop_mesh_extended | mesh_e4 | run01 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e4 | run01 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e4 | run01 | user | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | user > orders > catalogue > payment > shipping > carts |
| sockshop_mesh_extended | mesh_e4 | run01 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > catalogue > orders > carts > shipping |
| sockshop_mesh_extended | mesh_e4 | run02 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e4 | run02 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e4 | run02 | user | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > catalogue > orders > carts > shipping |
| sockshop_mesh_extended | mesh_e4 | run02 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > shipping > catalogue > orders > carts |
| sockshop_mesh_extended | mesh_e4 | run03 | user | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e4 | run03 | user | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e4 | run03 | user | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > catalogue > orders > carts > shipping |
| sockshop_mesh_extended | mesh_e4 | run03 | user | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | user > payment > catalogue > carts > shipping > orders |
| sockshop_mesh_extended | mesh_e5 | run01 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run01 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e5 | run01 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > shipping > user > carts > orders |
| sockshop_mesh_extended | mesh_e5 | run01 | catalogue | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | payment > catalogue > shipping > user > carts > orders |
| sockshop_mesh_extended | mesh_e5 | run02 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run02 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e5 | run02 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > orders > carts > shipping > user |
| sockshop_mesh_extended | mesh_e5 | run02 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > orders > carts > shipping > user |
| sockshop_mesh_extended | mesh_e5 | run03 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run03 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e5 | run03 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > carts > orders > user > shipping |
| sockshop_mesh_extended | mesh_e5 | run03 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > orders > user > carts > shipping |
| sockshop_mesh_extended | mesh_e5 | run04 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run04 | catalogue | dycause | 2 | 1.0000 | 1.0000 | 0.8571 |  |
| sockshop_mesh_extended | mesh_e5 | run04 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > orders > payment > shipping > carts > user |
| sockshop_mesh_extended | mesh_e5 | run04 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > payment > orders > shipping > user > carts |
| sockshop_mesh_extended | mesh_e5 | run05 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run05 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e5 | run05 | catalogue | pearson_entry_abs | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > orders > payment > carts > user > shipping |
| sockshop_mesh_extended | mesh_e5 | run05 | catalogue | anomaly_z_mean_shift | 2 | 1.0000 | 1.0000 | 0.8571 | payment > catalogue > orders > shipping > user > carts |
| sockshop_mesh_extended | mesh_e5 | run06 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run06 | catalogue | dycause |  | 0.0000 | 0.0000 | 0.0000 |  |
| sockshop_mesh_extended | mesh_e5 | run06 | catalogue | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | user > orders > shipping > payment > carts > catalogue |
| sockshop_mesh_extended | mesh_e5 | run06 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > carts > user > orders > shipping > payment |
| sockshop_mesh_extended | mesh_e5 | run07 | catalogue | random_expected | expected | 0.3333 | 0.8333 | 0.6429 | random permutation |
| sockshop_mesh_extended | mesh_e5 | run07 | catalogue | dycause | 7 | 0.0000 | 0.0000 | 0.1429 |  |
| sockshop_mesh_extended | mesh_e5 | run07 | catalogue | pearson_entry_abs | 6 | 0.0000 | 0.0000 | 0.2857 | payment > orders > shipping > user > carts > catalogue |
| sockshop_mesh_extended | mesh_e5 | run07 | catalogue | anomaly_z_mean_shift | 1 | 1.0000 | 1.0000 | 1.0000 | catalogue > orders > carts > user > payment > shipping |
