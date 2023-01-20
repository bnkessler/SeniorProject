import matplotlib.pyplot as plt
import numpy as np
import random

length = 2
radius = int(length/2)
theta = np.linspace(0, 2 * np.pi, 500)
trials = 1000000
runs = 100


def draw_box():
    fig, ax = plt.subplots()
    ax.plot([-length/2, -length/2], [-length/2, length/2], "k-")
    ax.plot([length/2, length/2], [-length/2, length/2], "k-")
    ax.plot([-length/2, length/2], [-length/2, -length/2], "k-")
    ax.plot([-length/2, length/2], [length/2, length/2], "k-")
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), "k-")


def pi_avg(runs):
    sum = 0
    for i in range(runs):
        print(f"Run: {i+1}")
        # draw_box()
        coords = []
        for i in range(trials):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            # plt.plot(x, y, "b.")
            coords.append([x, y])
        # plt.show()

        counts = 0
        for val in coords:
            if val[0]**2 + val[1]**2 <= radius**2:
                counts += 1

        pi_compute = 4 * counts/trials
        print(f"Computed value of pi: {pi_compute}")
        sum += pi_compute

    pi = sum/runs
    print(f"Average value of pi computed: {pi} over {runs} simulations")


pi_avg(runs)
