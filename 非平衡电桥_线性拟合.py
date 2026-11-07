from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = Path(__file__).resolve().parent
T = np.array([0, 18.64, 20.03, 25.82, 33.02, 40.17, 53.85,
              62.70, 70.20, 82.85, 90.13, 96.27, 100.40])
U = np.array([0.08, 6.20, 6.54, 8.68, 11.29, 14.09, 19.14,
              22.25, 25.13, 29.74, 32.35, 34.74, 36.14])
k, b = np.polyfit(T, U, 1)
pred = k * T + b
r = np.corrcoef(T, U)[0, 1]
sigma_k = np.sqrt(np.sum((U - pred)**2) /
                  ((len(T) - 2) * np.sum((T - T.mean())**2)))
E, R1, R2, Rp = 10.0, 10138.0, 9995.0, 99.4
R0 = R1 * Rp / R2
k0 = k * 1e-3
A1 = k0 * (R2 + Rp)**2 / (E * R2 * Rp)
sigma_k0 = sigma_k * 1e-3
sigma_A1_fit = (R2 + Rp)**2 / (E * R2 * Rp) * sigma_k0

font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'
font_manager.fontManager.addfont(font_path)
cn = font_manager.FontProperties(fname=font_path)
plt.rcParams.update({
    'font.family': cn.get_name(), 'font.size': 12,
    'mathtext.fontset': 'stix', 'axes.linewidth': 0.9,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'axes.unicode_minus': False, 'pdf.fonttype': 42,
})
fig, ax = plt.subplots(figsize=(7.6, 4.9), layout='constrained')
ax.scatter(T, U, s=28, facecolors='white', edgecolors='black',
           linewidths=0.9, label='测量数据', zorder=3)
grid = np.linspace(0, 103, 400)
ax.plot(grid, k * grid + b, color='#235789', lw=1.5, label='线性拟合')
ax.set(xlim=(-3, 105), ylim=(-1.5, 39),
       xlabel=r'$T/{}^{\circ}\mathrm{C}$',
       ylabel=r'$U_{\mathrm{out}}/\mathrm{mV}$')
ax.set_xticks(np.arange(0, 101, 20))
ax.set_yticks(np.arange(0, 40, 5))
ax.tick_params(top=True, right=True)
ax.legend(frameon=False, loc='upper left', prop=cn)
fig.savefig(OUT / '非平衡电桥_线性拟合.png', dpi=240)
fig.savefig(OUT / '非平衡电桥_线性拟合.pdf')
plt.close(fig)
results = dict(n=len(T), k_mV_per_C=float(k), b_mV=float(b),
               r=float(r), R_squared=float(r*r), sigma_k_mV=float(sigma_k),
               R0_ohm=float(R0), k0_V_per_C=float(k0), A1_per_C=float(A1),
               sigma_k0_V_per_C=float(sigma_k0),
               sigma_A1_fit_per_C=float(sigma_A1_fit))
(OUT / '非平衡电桥_线性拟合结果.json').write_text(
    json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
