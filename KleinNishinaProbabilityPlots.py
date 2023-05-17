import random

import numpy as np
from ScatteringFunctions import p_kn
import matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 1000)
energies = [2.75e-6, 6e-2, .511, .663, 1.46, 10]
prob_dict = {}

for energy in energies:
    probabilities = []
    for i in theta:
        probabilities.append(p_kn(energy, i))
    prob_dict[energy] = probabilities

for energy in energies:
    plt.polar(theta, prob_dict[energy], label=f"{energy} MeV")
plt.figure(1)
plt.legend()
# plt.show()

accepted_angles = []
plt.figure(2)
for i in range(10000):
    p = True
    energy = .663
    while p:
        q = random.uniform(0, 1)
        theta = random.uniform(0, 2*np.pi)
        print(q, theta)
        if q < p_kn(energy, theta):
            accepted_angles.append(theta)
            p = False

plt.hist(accepted_angles, bins=16)
# plt.axis([0, 2*np.pi, 0, 750])
plt.xticks(np.linspace(0, 2*np.pi, 16), labels=[
    "0", "\u03C0/6", "\u03C0/4", "\u03C0/3", "\u03C0/2", "2\u03C0/3", "3\u03C0/4", "5\u03C0/6", "\u03C0"
    "7\u03C0/6", "5\u03C0/4", "4\u03C0/3", "3\u03C0/2", "5\u03C0/3", "7\u03C0/4", "11\u03C0/6", "2\u03C0"
])

plt.show()


