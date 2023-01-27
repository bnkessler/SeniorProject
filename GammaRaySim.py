import matplotlib.pyplot as plt
import random
import numpy as np


class Source:

    def __init__(self, name, energy, position, density):
        self.name = name
        self.energy = energy
        self.x = position[0]
        self.y = position[1]
        ax.plot(self.x, self.y, "r.", markersize=10)
        self.Lambda = 2.24 * density

    def absorption_length(self, r):
        length = -1 / self.Lambda * np.log(1 - r)
        return length


def draw_detector(diameter, length, distance):
    plt.plot([distance, distance], [-diameter/2, diameter/2], "k-")
    plt.plot([distance + length, distance + length], [-diameter/2, diameter/2], "k-")
    plt.plot([distance, distance + length], [diameter/2, diameter/2], "k-")
    plt.plot([distance, distance + length], [-diameter/2, -diameter/2], "k-")
    plt.plot([0, distance + length], [0, 0], "k--")
    plt.plot([0, distance], [0, diameter / 2], "k--")
    plt.plot([0, distance], [0, -diameter / 2], "k--")
    return np.arctan2(-diameter / 2, distance), np.arctan2(diameter / 2, distance)


def gamma_emission():
    emission_angle = np.pi*random.uniform(-1, 1)
    return emission_angle


DIAMETER, LENGTH, DISTANCE = 3, 10, 5
ENERGY, START, DENSITY = .663, [0, 0], 3.67
HYPOTENUSE = ((DIAMETER/2)**2 + DISTANCE**2)**(1/2)

fig, ax = plt.subplots()
min_angle, max_angle = draw_detector(DIAMETER, LENGTH, DISTANCE)
source = Source("cs137", ENERGY, START, DENSITY)
plt.xlabel("x [cm]")
plt.ylabel("y [cm]")
plt.title("Gamma Ray Absorption")

lengths = []
for i in range(10000):
    r = random.uniform(0, 1)
    lengths.append(source.absorption_length(r))
plt.figure(2)
plt.hist(lengths)
plt.xlabel("Gamma Ray Penetration Depth [cm]")
plt.ylabel("Counts")
plt.title("Penetration Depth Histogram")

for i in range(500):
    angle = gamma_emission()
    absorption_length = random.choice(lengths)
    if min_angle < angle < max_angle and (LENGTH * absorption_length + DISTANCE) < 15:
        ax.plot([0, (LENGTH * absorption_length + DISTANCE)], [0, HYPOTENUSE * np.sin(angle)], "r--")

plt.show()

