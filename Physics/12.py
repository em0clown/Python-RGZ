import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Дано
L = 0.35              # Гн
T0 = 0.006            # с
C2 = 3e-6             # Ф
U0 = 45               # В

# Расчёты
C1 = (T0 / (2 * np.pi))**2 / L
Ceq = (C1 * C2) / (C1 + C2)
Q0 = Ceq * U0
omega = 1 / np.sqrt(L * Ceq)

# Время и заряд
t1 = np.linspace(0, 0.01, 2000)  # до 10 мс
q1 = Q0 * np.cos(omega * t1)

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(t1 * 1000, q1 * 1e6, linewidth=2, color='blue', label="q(t)")

ax1.set_xlabel("t, мс")
ax1.set_ylabel("q(t), мкКл")
ax1.set_title("Задача 12: q(t) = Q₀ cos(ωt)")

# Сетка
ax1.xaxis.set_major_locator(MultipleLocator(0.5))  # 0.5 мс
ax1.xaxis.set_minor_locator(MultipleLocator(0.1))
ax1.yaxis.set_major_locator(MultipleLocator(10))   # 10 мкКл
ax1.yaxis.set_minor_locator(MultipleLocator(2))

ax1.grid(which='major', linewidth=1.2)
ax1.grid(which='minor', linestyle='--', linewidth=0.5)

ax1.legend()
plt.tight_layout()
plt.show()

