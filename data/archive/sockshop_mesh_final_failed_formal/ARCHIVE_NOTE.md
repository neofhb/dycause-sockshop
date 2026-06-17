# Final Formal Archive Note

This directory contains the later `final_e*` formal batch that used the `business-final-v3` load profile.

It is archived because its DyCause performance was weaker than the earlier compressed mesh batch:

- original main params `lag=5, step=30, edge_thres=0.8`: Top-2 0/6 valid runs
- tuned best complete params `lag=5, step=30, edge_thres=0.7`: Top-2 1/6 valid runs

The active mesh experiment line has been restored to `data/sockshop_mesh_extended/`, which contains the legacy compressed batch with stronger `payment` results.
