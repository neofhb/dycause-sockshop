"""
Generate statistical charts for DyCause SockShop experiment README.
Output: experiment/figures/*.png
"""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 150,
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
})

# ─── Data ────────────────────────────────────────────────

experiments = ['e1\n(payment)', 'e2\n(user)', 'Pymicro\n(baseline)', 'proof\n(cpu)']
pr_at = {
    'PR@2': [100, 100, 100, 0],
    'PR@5': [100, 100, 100, 0],
}
acc_values = [75, 75, 93.75, 0]
colors = ['#2ecc71', '#2ecc71', '#3498db', '#e74c3c']

metric_trial_labels = ['container_cpu', 'network', 'throughput', 'mixed', 'latency']
metric_trial_acc = [35.71, 0, 0, 21.43, 75]
metric_trial_colors = ['#e74c3c', '#e74c3c', '#e74c3c', '#f39c12', '#2ecc71']


# ─── Figure 1: PR@K comparison ──────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(experiments))
w = 0.3
bars1 = ax.bar(x - w/2, pr_at['PR@2'], w, label='PR@2', color='#2ecc71', edgecolor='white')
bars2 = ax.bar(x + w/2, pr_at['PR@5'], w, label='PR@5', color='#3498db', edgecolor='white')

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{int(bar.get_height())}%', ha='center', fontsize=10, fontweight='bold')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{int(bar.get_height())}%', ha='center', fontsize=10, fontweight='bold')

ax.set_ylabel('PR@K (%)')
ax.set_title('Root Cause Detection Precision (PR@K)')
ax.set_xticks(x)
ax.set_xticklabels(experiments)
ax.set_ylim(0, 120)
ax.legend(loc='upper right')
ax.axhline(y=100, color='gray', linestyle='--', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig1_prk.png'), bbox_inches='tight')
plt.close()
print("Saved fig1_prk.png")


# ─── Figure 2: Acc comparison ────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(experiments, acc_values, color=colors, edgecolor='white', width=0.5)
for bar, val in zip(bars, acc_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{val:.2f}%', ha='center', fontsize=11, fontweight='bold')

ax.set_ylabel('Accuracy (%)')
ax.set_title('Root Cause Ranking Accuracy (Acc)')
ax.set_ylim(0, 110)
ax.axhline(y=93.75, color='#3498db', linestyle='--', alpha=0.5, label='Pymicro baseline')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig2_acc.png'), bbox_inches='tight')
plt.close()
print("Saved fig2_acc.png")


# ─── Figure 3: Metric type comparison ────────────────────

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(metric_trial_labels, metric_trial_acc, color=metric_trial_colors, edgecolor='white', width=0.5)
ax.axhline(y=75, color='#2ecc71', linestyle='--', alpha=0.5, label='Target: latency')
ax.axhline(y=35.71, color='#f39c12', linestyle='--', alpha=0.5, label='Best non-latency')

for bar, val in zip(bars, metric_trial_acc):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
    else:
        ax.text(bar.get_x() + bar.get_width()/2, 3,
                '0%', ha='center', fontsize=10, fontweight='bold', color='white')

ax.set_ylabel('Best Acc (%)')
ax.set_title('Metric Type vs DyCause Accuracy')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig3_metrics.png'), bbox_inches='tight')
plt.close()
print("Saved fig3_metrics.png")


# ─── Figure 4: DyCause discovered topology (e1 + e2) ─────

fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('DyCause Discovered Granger Causal Edges (e1 + e2)', fontsize=13, pad=10)

nodes = {
    'FE': (6, 8, 'front-end\n(idx=0)', '#3498db'),
    'CA': (3, 5, 'catalogue\n(idx=1)', '#2ecc71'),
    'PA': (9, 5, 'payment\n(idx=2)', '#e74c3c'),
    'US': (6, 2, 'user\n(idx=3)', '#f39c12'),
}

# e1 edges (Pod-Kill payment): user→catalogue + user→payment→catalogue→front-end
# e2 edges (Pod-Kill user):    user→payment→catalogue→front-end
edges = [
    ('US','CA', 'user→catalogue\n(e1 only)',      '#f39c12'),
    ('US','PA', 'user→payment\n(e1+e2 shared)',   '#e67e22'),
    ('PA','CA', 'payment→catalogue\n(e1+e2)',     '#e67e22'),
    ('CA','FE', 'catalogue→front-end\n(e1+e2)',   '#2ecc71'),
]

for (u, v, label, color) in edges:
    xu, yu, _, _ = nodes[u]; xv, yv, _, _ = nodes[v]
    dx, dy = xv - xu, yv - yu
    rad = 0.15 if abs(dy) > 2 else 0
    ax.annotate('', xy=(xv, yv+0.35), xytext=(xu, yu-0.05),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8,
                               connectionstyle=f'arc3,rad={rad}'))
    mx, my = (xu+xv)/2, (yu+yv)/2
    ax.text(mx+0.3, my, label, fontsize=6.5, ha='center', color=color, fontweight='bold')

for key, (x, y, name, color) in nodes.items():
    circle = plt.Circle((x, y), 0.5, color=color, ec='white', lw=2)
    ax.add_patch(circle)
    ax.text(x, y, key, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(x, y-1.0, name, ha='center', fontsize=7, color='#333')

ax.text(6, 9.5, 'Entry Point', ha='center', fontsize=8, color='#3498db')
ax.text(9, 6.2, 'e1 root\n(Pod-Kill)', ha='center', fontsize=6.5, fontweight='bold', color='#e74c3c')
ax.text(6, 1.4, 'e2 root\n(Pod-Kill)', ha='center', fontsize=6.5, fontweight='bold', color='#f39c12')

import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
leg = [Line2D([0],[0],color='#f39c12',lw=2,label='e1 only (user→catalogue)'),
       Line2D([0],[0],color='#e67e22',lw=2,label='e1+e2 shared chain'),
       Line2D([0],[0],color='#2ecc71',lw=2,label='e1+e2 shared (catalogue→front-end)')]
ax.legend(handles=leg, loc='lower right', fontsize=7)

fig.text(0.5, 0.02,
         '4 nodes × 3 targets = 12 theoretical. DyCause finds 4 significant (e1) / 3 significant (e2). Both trace to front-end.',
         ha='center', fontsize=7, color='#999')

fig.savefig(os.path.join(OUT, 'fig4_topology.png'), bbox_inches='tight', dpi=150)
plt.close()
print("Saved fig4_topology.png")


# ─── Figure 5: Summary table ─────────────────────────────

fig, ax = plt.subplots(figsize=(9, 3.5))
ax.axis('off')
ax.set_title('Experiment Results Summary', fontsize=13, pad=10)

data = [
    ['e1', 'Pod-Kill', 'payment (idx=2)', '100%', '—', '75.00%'],
    ['e2', 'Pod-Kill', 'user (idx=3)', '100%', '—', '75.00%'],
    ['Pymicro', 'Latency injection', 'service 1', '100%', '100%', '93.75%'],
    ['proof', 'Pod-Kill [CPU]', 'payment (idx=2)', '0%', '0%', '0%'],
]
cols = ['Exp', 'Fault', 'Root Cause', 'PR@2', 'PR@5', 'Acc']

table = ax.table(cellText=data, colLabels=cols, cellLoc='center', loc='center',
                 colColours=['#34495e']*6)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)

for i in range(len(data)):
    for j in range(len(cols)):
        cell = table[i+1, j]
        if i < 2:
            cell.set_facecolor('#e8f8f5')
        elif i == 2:
            cell.set_facecolor('#ebf5fb')
        else:
            cell.set_facecolor('#fdedec')
        if j == 3 or j == 4 or j == 5:
            pass

fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig5_summary.png'), bbox_inches='tight')
plt.close()
print("Saved fig5_summary.png")

print(f"\nAll figures saved to {OUT}/")
