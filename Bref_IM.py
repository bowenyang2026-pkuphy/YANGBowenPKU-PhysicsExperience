from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

IM_A = np.array([0.000, 0.100, 0.200, 0.300, 0.400, 0.500,
                 0.600, 0.700, 0.800, 0.900, 1.000])
B_RAW_MT = np.array([
    [0.4, 0.7, 0.6, 0.6],
    [27.7, 28.5, 28.2, 28.0],
    [57.1, 58.4, 56.7, 55.7],
    [86.2, 87.6, 85.2, 85.2],
    [114.8, 116.3, 114.0, 114.0],
    [145.1, 145.2, 142.9, 142.9],
    [172.0, 174.0, 171.3, 171.3],
    [200.6, 202.2, 199.1, 199.0],
    [228.5, 230.5, 227.0, 227.0],
    [256.2, 257.6, 255.2, 255.1],
    [282.9, 283.8, 281.6, 281.8],
])
B_MT = B_RAW_MT.mean(axis=1)
k, b = np.polyfit(IM_A, B_MT, 1)
fit_current = np.linspace(0, 1.0, 300)

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 12,
    'mathtext.fontset': 'stix',
    'axes.linewidth': 0.9,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'savefig.facecolor': 'white',
})
fig, ax = plt.subplots(figsize=(6.4, 4.8))
ax.scatter(np.repeat(IM_A, 4), B_RAW_MT.ravel(),
           color='#888888', s=18, alpha=0.7, zorder=1)
ax.plot(fit_current, k * fit_current + b, color='#D55E00',
        linestyle='--', linewidth=1.3, zorder=2)
ax.plot(IM_A, B_MT, color='#0072B2', linewidth=1.1,
        marker='o', markersize=6, markerfacecolor='white',
        markeredgewidth=1.3, zorder=3)
ax.set(xlabel=r'$I_{\mathrm{M}}$ (A)', ylabel=r'$B_{\mathrm{ref}}$ (mT)',
       xlim=(-0.02, 1.04), ylim=(-5, 300),
       xticks=np.arange(0, 1.01, 0.2))
ax.set_title(r'$B_{\mathrm{ref}}$-$I_{\mathrm{M}}$', fontsize=15, pad=12)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='both', top=True, right=True)
fig.tight_layout(pad=1.2)
fig.savefig(Path(__file__).with_suffix('.png'), dpi=300, bbox_inches='tight')
