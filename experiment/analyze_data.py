"""Detailed data analysis for e1/e2 experiments."""
import pandas as pd, numpy as np, json, os

def analyze(exp):
    df = pd.read_excel(f'data/sockshop/{exp}/rawdata.xlsx')
    meta = json.load(open(f'data/sockshop/{exp}/metadata.json'))
    half = len(df) // 2
    b_df, f_df = df.iloc[:half], df.iloc[half:]
    cols = list(df.columns)
    
    print(f"\n{'='*60}")
    print(f"  {exp}: {meta.get('desc','')}")
    print(f"  Services: {cols}")
    print(f"  Root cause idx: {meta['root_cause_indices']}")
    print(f"{'='*60}")
    
    # 1. Descriptive stats
    print(f"\n--- Baseline vs Fault Statistics ---")
    print(f"{'':<14} {'Baseline(mean/std)':>25} {'Fault(mean/std)':>25} {'Std Change':>12}")
    for s in cols:
        bm, bs = b_df[s].mean(), b_df[s].std()
        fm, fs = f_df[s].mean(), f_df[s].std()
        change = (fs/bs - 1) * 100 if bs > 0 else 0
        print(f"{s:<14} {bm:10.6f}/{bs:10.6f}  {fm:10.6f}/{fs:10.6f}  {change:+9.1f}%")
    
    # 2. Anomaly window snapshot (rows 310-325)
    print(f"\n--- Anomaly Window (rows 310-325, anomaly at 315) ---")
    window = df.iloc[310:326]
    print(f"{'Row':>4}", end="")
    for s in cols:
        print(f" {s[:6]:>10}", end="")
    print()
    for i in range(len(window)):
        r = window.iloc[i]
        marker = " <<< ANOMALY" if 310+i == 315 else ""
        print(f"{310+i:4d}", end="")
        for s in cols:
            v = r[s]
            highlight = "*" if abs(v - b_df[s].mean()) > 3 * b_df[s].std() else " "
            print(f" {highlight}{v:9.6f}", end="")
        print(marker)
    
    # 3. Missing/gap data points (indicating pod restart)
    print(f"\n--- Data Gaps (pod restart indicator) ---")
    for s in cols:
        zeros = (f_df[s] == 0).sum()
        baseline_zeros = (b_df[s] == 0).sum()
        if zeros > baseline_zeros:
            print(f"  {s:<14}: baseline {baseline_zeros} zeros, fault {zeros} zeros (pod restart)")
    
    # 4. Top correlated pairs before/after
    print(f"\n--- Correlation Matrix (Baseline / Fault) ---")
    b_corr = b_df.corr()
    f_corr = f_df.corr()
    for i, s1 in enumerate(cols):
        for j, s2 in enumerate(cols):
            if i < j:
                bc = b_corr.loc[s1, s2]
                fc = f_corr.loc[s1, s2]
                change = fc - bc
                if abs(change) > 0.05:
                    print(f"  {s1} <-> {s2}: {bc:+.3f} -> {fc:+.3f} (delta={change:+.3f})")

if __name__ == "__main__":
    analyze("e1")
    analyze("e2")
