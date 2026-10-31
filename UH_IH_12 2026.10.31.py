from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
CURRENT_MA = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
VOLTAGE_MV = np.array([5.408, 10.848, 16.225, 21.688, 27.038])
COLOR = '#0072B2'

def four_sig(value):
    value = Decimal(str(value))
    if not value:
        return '0.000'
    quantum = Decimal(1).scaleb(value.adjusted() - 3)
    return format(value.quantize(quantum, rounding=ROUND_HALF_UP), 'f')
b, k = np.polynomial.polynomial.polyfit(CURRENT_MA, VOLTAGE_MV, 1)
xx = np.linspace(0, 10.5, 400)
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12, 'mathtext.fontset': 'stix', 'axes.linewidth': 0.9, 'xtick.direction': 'in', 'ytick.direction': 'in', 'pdf.fonttype': 42, 'savefig.facecolor': 'white'})
fig, ax = plt.subplots(figsize=(6.4, 4.8))
ax.plot(xx, k * xx + b, color=COLOR, linewidth=1.3, zorder=2)
ax.scatter(CURRENT_MA, VOLTAGE_MV, s=38, marker='o', facecolors='white', edgecolors=COLOR, linewidths=1.3, zorder=3)
ax.set(xlabel='$I_{\\mathrm{H}}$ (mA)', ylabel='$U_{\\mathrm{H}}$ (mV)', xlim=(0, 10.8), ylim=(0, 30), xticks=np.arange(0, 11, 2))
ax.set_title('UH-IH 12', fontsize=15, pad=12)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='both', top=True, right=True)
sign = '+' if b >= 0 else '-'
equation = f'$U_{{\\mathrm{{H}}}} = {four_sig(k)} I_{{\\mathrm{{H}}}} {sign} {four_sig(abs(b))}$'
ax.text(0.06, 0.88, equation, transform=ax.transAxes, fontsize=13, ha='left', va='top')
fig.tight_layout(pad=1.2)
folder = Path(__file__).resolve().parent
stem = Path(__file__).stem
for ext in ('png', 'pdf'):
    path = folder / f'{stem}.{ext}'
    fig.savefig(path, dpi=300, bbox_inches='tight')
