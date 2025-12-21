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

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(t2 * 1000, q2 * 1e3, linewidth=2, label="q(t)", color="green")
ax2.plot(t2 * 1000, env * 1e3, "--", linewidth=1.5, color='red', label="+огибающая")
ax2.plot(t2 * 1000, -env * 1e3, "--", linewidth=1.5, color='red', label="-огибающая")

ax2.set_xlabel("t, мс")
ax2.set_ylabel("q(t), мКл")
ax2.set_title("Задача 13: Затухающие колебания")

# Сетка
ax2.xaxis.set_major_locator(MultipleLocator(0.5))  # 0.5 мс
ax2.xaxis.set_minor_locator(MultipleLocator(0.1))
ax2.yaxis.set_major_locator(MultipleLocator(1))    # 1 мКл
ax2.yaxis.set_minor_locator(MultipleLocator(0.2))

ax2.grid(which='major', linewidth=1.2)
ax2.grid(which='minor', linestyle='--', linewidth=0.5)

ax2.legend()
plt.tight_layout()
plt.show()