from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

BREF_MT = [0.58, 28.10, 56.98, 86.05, 114.78, 144.03, 172.15, 200.23, 228.25, 256.03, 282.53]
UHB_MV = [0.180, 4.463, 8.935, 13.493, 17.833, 22.483, 26.905, 31.290, 35.723, 40.095, 44.173]
COLOR = '#0072B2'

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
ax.plot(BREF_MT, UHB_MV, color=COLOR, linewidth=1.3,
        marker='o', markersize=6, markerfacecolor='white',
        markeredgewidth=1.3)
ax.set(xlabel=r'$B_{\mathrm{ref}}$ (mT)',
       ylabel=r'$U_{\mathrm{HB}}$ (mV)',
       xlim=(-5, 300), ylim=(-1, 48), xticks=range(0, 301, 50))
ax.set_title(r'$U_{\mathrm{HB}}$-$B_{\mathrm{ref}}$', fontsize=15, pad=12)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='both', top=True, right=True)
fig.tight_layout(pad=1.2)
fig.savefig(Path(__file__).with_suffix('.png'), dpi=300, bbox_inches='tight')
