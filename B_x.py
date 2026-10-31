from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

x_mm = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 11.4, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 29.0, 30.0, 30.5, 31.0, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5, 36.0, 37.0, 38.0, 39.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0])
B_mT = np.array([173.23, 173.30, 173.43, 173.49, 173.49, 173.49, 173.49, 173.49, 173.49, 173.43, 173.36, 173.23, 172.98, 172.66, 171.63, 166.70, 159.47, 143.15, 136.62, 126.69, 115.04, 105.57, 95.644, 84.825, 74.454, 69.652, 63.06, 57.68, 52.24, 49.23, 42.89, 37.90, 33.48, 30.41, 25.74, 22.15, 19.53, 17.41, 15.68])

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 12,
    'mathtext.fontset': 'stix',
    'axes.linewidth': 0.9,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'savefig.facecolor': 'white',
})
fig, ax = plt.subplots(figsize=(9.0, 4.8))
ax.plot(x_mm, B_mT, color='#0072B2', linewidth=1.1,
        marker='o', markersize=4.5, markerfacecolor='white',
        markeredgewidth=1.3, zorder=3)
ax.set(xlabel=r'$x$ (mm)', ylabel=r'$B$ (mT)',
       xlim=(-1, 51), ylim=(0, 185),
       xticks=np.arange(0, 51, 5), yticks=np.arange(0, 181, 20))
ax.set_title(r'$B$-$x$', fontsize=15, pad=12)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='both', top=True, right=True)
fig.tight_layout(pad=1.2)
fig.savefig(Path(__file__).with_suffix('.png'), dpi=300, bbox_inches='tight')
