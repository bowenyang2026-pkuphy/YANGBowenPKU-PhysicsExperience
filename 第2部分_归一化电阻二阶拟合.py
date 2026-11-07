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
U_mV = np.array([.08, 6.20, 6.54, 8.68, 11.29, 14.09, 19.14,
                 22.25, 25.13, 29.74, 32.35, 34.74, 36.14])
E, R1, R2, Rp = 10.0, 10138.0, 9995.0, 99.4
R0 = R1 * Rp / R2
q = (U_mV - U_mV[0]) * 1e-3 / E + Rp / (R2 + Rp)
normalized_R = R2 / Rp * q / (1 - q)
RT = R0 * normalized_R

t = T[1:]
y = normalized_R[1:] - 1
X = np.column_stack((t, t**2))
A, B = np.linalg.lstsq(X, y, rcond=None)[0]
residuals = y - X @ np.array([A, B])
dof = len(t) - 2
s2 = residuals @ residuals / dof
cov = s2 * np.linalg.inv(X.T @ X)
sigma_A, sigma_B = np.sqrt(np.diag(cov))
pred = 1 + A*T + B*T**2
R_squared = 1 - np.sum((normalized_R-pred)**2) / np.sum((normalized_R-normalized_R.mean())**2)
A_linear = t @ y / (t @ t)
SSE_linear = np.sum((y-A_linear*t)**2)
results = dict(A_per_C=float(A), B_per_C2=float(B),
               sigma_A_per_C=float(sigma_A), sigma_B_per_C2=float(sigma_B),
               cov_A_B=float(cov[0, 1]), R_squared=float(R_squared),
               R0_ohm=float(R0), U0_mV=float(U_mV[0]), n_raw=len(T),
               n_fitted=len(t), dof=dof, T_C=T.tolist(), U_mV=U_mV.tolist(),
               normalized_R=normalized_R.tolist(), RT_ohm=RT.tolist(),
               SSE_quadratic=float(residuals@residuals),
               constrained_linear_A=float(A_linear), SSE_linear=float(SSE_linear))

font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'
font_manager.fontManager.addfont(font_path)
cn = font_manager.FontProperties(fname=font_path)
plt.rcParams.update({'font.family': cn.get_name(), 'font.size': 12,
                     'mathtext.fontset': 'stix', 'axes.linewidth': .9,
                     'xtick.direction': 'in', 'ytick.direction': 'in',
                     'axes.unicode_minus': False, 'pdf.fonttype': 42})
fig, ax = plt.subplots(figsize=(7.6, 4.9), layout='constrained')
ax.scatter(T, normalized_R, s=28, facecolors='white', edgecolors='black',
           linewidths=.9, label='换算数据', zorder=3)
grid = np.linspace(0, 103, 400)
ax.plot(grid, 1+A*grid+B*grid**2, color='#235789', lw=1.5, label='二阶拟合')
ax.set(xlim=(-3, 105), ylim=(.985, 1.395), xlabel=r'$T/{}^{\circ}\mathrm{C}$',
       ylabel=r'$R/R_0$')
ax.set_xticks(np.arange(0, 101, 20))
ax.set_yticks(np.arange(1.0, 1.401, .1))
ax.tick_params(top=True, right=True)
ax.legend(frameon=False, loc='upper left', prop=cn)
fig.savefig(OUT/'第2部分_归一化电阻二阶拟合.pdf')
fig.savefig(OUT/'第2部分_归一化电阻二阶拟合.png', dpi=240)
plt.close(fig)
results.update(relative_standard_uncertainty_A=float(sigma_A / abs(A)),
               relative_standard_uncertainty_B=float(sigma_B / abs(B)))
(OUT/'第2部分_归一化电阻二阶拟合结果.json').write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
