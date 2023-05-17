import matplotlib.pyplot as plt
import random
import numpy as np
import collections
from scipy.optimize import curve_fit
from ScatteringFunctions import p_c, p_pe, p_kn


class Source:

    def __init__(self, name, energy, position, density):
        self.name = name
        self.energy = energy
        self.x = position[0]
        self.y = position[1]
        self.Lambda = 2.24 * density
        self.length = 0
        self.angle = 0
        self.energy_scattered = None
        self.x_scattered = None
        self.y_scattered = None
        self.scatters = 0
        self.phi = None
        ax.plot(self.x, self.y, "r.", markersize=10)

    def gamma_emission(self):
        self.angle = 2 * np.pi * random.uniform(0, 1)

    def absorption_length(self):
        self.length = -1 / self.Lambda * np.log(1 - random.uniform(0, 1))

    def stop_point(self):
        self.absorption_length()
        self.gamma_emission()
        depth = DISTANCE + self.length
        self.x = depth * np.cos(self.angle)
        self.y = depth * np.sin(self.angle)

    def compton_scatter(self, plot):
        self.absorption_length()
        self.compton_angle()
        theta = self.angle + self.phi
        self.energy_scattered = self.energy / (1 + self.energy / .511 * (1 - np.cos(theta)))
        self.x_scattered = self.x + self.length * np.cos(theta)
        self.y_scattered = self.y + self.length * np.sin(theta)
        if DISTANCE < self.x_scattered < DISTANCE + LENGTH and abs(self.y_scattered) < DIAMETER / 2 and plot == "Yes":
            ax.plot(self.x, self.y, "r.", markersize=5)
            ax.plot([self.x, self.x_scattered], [self.y, self.y_scattered], "k--")
        elif plot == "Yes":
            ax.plot(self.x, self.y, "rx")
        self.x, self.y, self.angle = self.x_scattered, self.y_scattered, theta
        self.scatters += 1

    def compton_angle(self):
        p = True
        while p:
            q = random.uniform(0, 1)
            theta = random.uniform(0, 2*np.pi)
            if q < p_kn(self.energy, theta):
                self.phi = theta
                p = False


def draw_detector(diameter, length, distance):
    plt.plot([distance, distance], [-diameter / 2, diameter / 2], "k-")
    plt.plot([distance + length, distance + length], [-diameter / 2, diameter / 2], "k-")
    plt.plot([distance, distance + length], [diameter / 2, diameter / 2], "k-")
    plt.plot([distance, distance + length], [-diameter / 2, -diameter / 2], "k-")
    plt.plot([0, distance + length], [0, 0], "k--")
    plt.plot([0, distance], [0, diameter / 2], "k--")
    plt.plot([0, distance], [0, -diameter / 2], "k--")
    return np.arctan2(-diameter / 2, distance), np.arctan2(diameter / 2, distance)


DIAMETER, LENGTH, DISTANCE = 3, 10, 5
ENERGY, START, DENSITY = .663, [0, 0], 3.67
HYPOTENUSE = ((DIAMETER / 2) ** 2 + DISTANCE ** 2) ** (1 / 2)

# Figure Generator
fig, ax = plt.subplots()
plt.xlabel("x [cm]")
plt.ylabel("y [cm]")
plt.title("Gamma Ray Absorption")

# Detector drawing
min_angle, max_angle = draw_detector(DIAMETER, LENGTH, DISTANCE)

# Histogram of Energies
# lengths = []
# for i in range(10000):
#     source = Source("cs137", ENERGY, START, DENSITY)
#     source.stop_point()
#     lengths.append(source.length)
# plt.figure(2)
# plt.hist(lengths)
# plt.xlabel("Gamma Ray Penetration Depth [cm]")
# plt.ylabel("Counts")
# plt.title("Penetration Depth Histogram")

# Adding Compton Scattering + Photoelectric Absorption
energies, scatters = [], []
for i in range(1000000):
    source = Source("cs137", ENERGY, START, DENSITY)
    source.stop_point()
    e_sum = 0
    if abs(source.y) < DIAMETER / 2 and DISTANCE < source.x < DISTANCE + LENGTH:
        # ax.plot([0, source.x], [0, source.y], "r--")
        r = random.uniform(0, 1)
        while DISTANCE < source.x < DISTANCE + LENGTH and abs(source.y) < DIAMETER / 2:
            if r < p_pe(source.energy) / (p_c(source.energy) + p_pe(source.energy)):  # Photoelectric Absorption
                e_sum += source.energy
                # ax.plot(source.x, source.y, "k*")
                energies.append(round(1000 * e_sum, 1))
                break
            else:  # Compton Scatter
                source.compton_scatter("No")
                if source.energy - source.energy_scattered > .001:
                    energies.append(round(1000 * (source.energy - source.energy_scattered), 1))
                e_sum += source.energy - source.energy_scattered
                source.energy = source.energy_scattered
                scatters.append(source.scatters)


# print(energies)
# plt.show()


counter = collections.Counter(energies)
print(counter)
# print(scatters)
sort_list = sorted(counter.keys())
sort = {}
for i in sort_list:
    sort[i] = counter.get(i)

plt.figure(3)
plt.plot(counter.keys(), counter.values(), "b.", markersize=1)
# plt.plot(sort.keys(), sort.values(), "k-", markersize=1)
plt.xlabel("Energy [KeV]")
print(np.mean(energies))
# print(scatters)
print(np.mean(scatters))
# plt.figure(4)
# plt.hist(scatters, bins=max(scatters))
plt.show()

