import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

C = 1e-7              # Ф
alpha = 100           # 1/c
omega2 = 1e4          # рад/с
Qm = 4e-3             # Кл

# Время
t2 = np.linspace(0, 0.006, 3000)  # до 6 мс

# Заряд и огибающие
q2 = Qm * np.exp(-alpha * t2) * np.cos(omega2 * t2)
env = Qm * np.exp(-alpha * t2)

# Точки (каждые T/4)
T = 2 * np.pi / omega2
t_points = np.arange(0, int(0.006/(T/4)) + 1) * T/4
q_points = Qm * np.exp(-alpha * t_points) * np.cos(omega2 * t_points)

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(t2 * 1000, q2 * 1e3, linewidth=2, label="q(t)", color="green")
ax2.plot(t2 * 1000, env * 1e3, "--", linewidth=1.5, color='red', label="огибающие")
ax2.plot(t2 * 1000, -env * 1e3, "--", linewidth=1.5, color='red')

# Точки
ax2.scatter(t_points * 1000, q_points * 1e3, color='blue', s=30, zorder=5, label="точки T/4")

# Маленькие подписи к точкам
for t_pt, q_pt in zip(t_points, q_points):
    # Форматируем число (убираем -0.00)
    value = q_pt * 1e3
    if abs(value) < 0.005:
        label = "0"
    else:
        label = f"{value:.1f}"
    
    # Определяем смещение (вверх или вниз)
    offset = 5 if q_pt >= 0 else -7
    
    ax2.annotate(label, (t_pt * 1000, q_pt * 1e3),
                 xytext=(0, offset), 
                 textcoords="offset points",
                 ha='center', 
                 fontsize=6,
                 color='blue')

ax2.set_xlabel("t, мс")
ax2.set_ylabel("q(t), мКл")
ax2.set_title("Задача 13: Затухающие колебания")

# Сетка
ax2.xaxis.set_major_locator(MultipleLocator(0.5))
ax2.xaxis.set_minor_locator(MultipleLocator(0.1))
ax2.yaxis.set_major_locator(MultipleLocator(1))
ax2.yaxis.set_minor_locator(MultipleLocator(0.2))

ax2.grid(which='major', linewidth=1.2, alpha=0.7)
ax2.grid(which='minor', linestyle='--', linewidth=0.5, alpha=0.3)

ax2.legend(fontsize=9)
plt.tight_layout()
plt.show()