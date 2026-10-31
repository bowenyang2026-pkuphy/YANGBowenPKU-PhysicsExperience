from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

IM_A = np.array([0.000, 0.100, 0.200, 0.300, 0.400, 0.500,
                 0.600, 0.700, 0.800, 0.900, 1.000])
B_MT = np.array([1.15, 28.57, 57.20, 86.38, 114.2, 143.9,
                 172.2, 200.3, 228.7, 256.7, 282.8])

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
ax.plot(IM_A, B_MT, color='#0072B2', linewidth=1.1,
        marker='o', markersize=6, markerfacecolor='white',
        markeredgewidth=1.3, zorder=3)
ax.set(xlabel=r'$I_{\mathrm{M}}$ (A)', ylabel=r'$B$ (mT)',
       xlim=(-0.02, 1.04), ylim=(-5, 300),
       xticks=np.arange(0, 1.01, 0.2))
ax.set_title(r'$B$-$I_{\mathrm{M}}$', fontsize=15, pad=12)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='both', top=True, right=True)
fig.tight_layout(pad=1.2)
fig.savefig(Path(__file__).with_suffix('.png'), dpi=300, bbox_inches='tight')
