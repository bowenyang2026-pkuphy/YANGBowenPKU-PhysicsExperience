from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = Path(__file__).resolve().parent
T = np.array([0, 19.07, 25.69, 36.85, 51.83, 66.89, 74.75, 82.40, 100.40])
Rp = np.array([100.02, 106.0, 108.9, 113.0, 119.0, 124.4, 127.2, 130.0, 136.4])
R1, R2 = 10138.0, 9995.0
RT = R1 / R2 * Rp
N = len(T)
X = np.column_stack((T, np.ones(N)))
k, b = np.linalg.lstsq(X, RT, rcond=None)[0]
residuals = RT - X @ np.array([k, b])
s2 = residuals @ residuals / (N - 2)
cov = s2 * np.linalg.inv(X.T @ X)
sigma_k, sigma_b = np.sqrt(np.diag(cov))
A1 = k / b
grad_A1 = np.array([1 / b, -k / b**2])
sigma_A1 = np.sqrt(grad_A1 @ cov @ grad_A1)
r = np.corrcoef(T, RT)[0, 1]
results = dict(n=N, T_C=T.tolist(), Rp_ohm=Rp.tolist(), RT_ohm=RT.tolist(),
               k_ohm_per_C=float(k), R0_ohm=float(b), A1_per_C=float(A1),
               sigma_k_ohm_per_C=float(sigma_k), sigma_R0_ohm=float(sigma_b),
               cov_k_b=float(cov[0, 1]), sigma_A1_per_C=float(sigma_A1),
               r=float(r), R_squared=float(r*r), residual_variance=float(s2),
               Sxx=float(np.sum((T-T.mean())**2)), T_mean=float(T.mean()))

font_path = '/System/Library/Fonts/Supplemental/Songti.ttc'
font_manager.fontManager.addfont(font_path)
cn = font_manager.FontProperties(fname=font_path)
plt.rcParams.update({'font.family': cn.get_name(), 'font.size': 12,
                     'mathtext.fontset': 'stix', 'axes.linewidth': .9,
                     'xtick.direction': 'in', 'ytick.direction': 'in',
                     'axes.unicode_minus': False, 'pdf.fonttype': 42})
fig, ax = plt.subplots(figsize=(7.6, 4.9), layout='constrained')
ax.scatter(T, RT, s=28, facecolors='white', edgecolors='black',
           linewidths=.9, label='测量数据', zorder=3)
t = np.linspace(0, 103, 400)
ax.plot(t, k*t+b, lw=1.5, color='#235789', label='线性拟合')
ax.set(xlim=(-3, 105), ylim=(98, 141), xlabel=r'$T/{}^{\circ}\mathrm{C}$',
       ylabel=r'$R_T/\Omega$')
ax.set_xticks(np.arange(0, 101, 20))
ax.set_yticks(np.arange(100, 141, 10))
ax.tick_params(top=True, right=True)
ax.legend(frameon=False, loc='upper left', prop=cn)
fig.savefig(OUT / '选做实验2_RT线性拟合.pdf')
fig.savefig(OUT / '选做实验2_RT线性拟合.png', dpi=240)
plt.close(fig)
(OUT / '选做实验2_RT线性拟合结果.json').write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
