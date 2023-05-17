import numpy as np

Z = 11
N = 6.022e23
r_e = 0.07941  # barn
# r_e = 2.817940e-13  # cm
e_electron = .51099895000  # MeV
alpha = 0.00729735
m_e = 9.109387e-31  # kg
c = 299792458  # m/s
s_pe, s_c = [], []


def p_c(e_gamma):
    if e_gamma is type(list) or isinstance(e_gamma, np.ndarray):
        for energy in e_gamma:
            k = energy / e_electron
            if energy > .1:
                t1 = (Z * 2 * np.pi * (r_e ** 2))
                t2 = (1 + k) / (k ** 2)
                t3 = (2 * (1 + k) / (1 + 2 * k)) - (np.log(1 + 2 * k) / k)
                t4 = np.log(1 + 2 * k) / (2 * k)
                t5 = (1 + 3 * k) / ((1 + 2 * k) ** 2)
                s = t1 * (t2 * t3 + t4 - t5)
                s_c.append(s)
            else:
                t1 = (Z * 8/3 * np.pi * (r_e ** 2))
                t2 = 1 / ((1 + 2*k) ** 2)
                t3 = 1 + 2*k + 6/5*(k**2) - 1/2*(k**3) + 2/7*(k**4) - 6/35*(k**5) + 8/105*(k**6) + 4/105*(k**7)
                s = t1 * t2 * t3
                s_c.append(s)
        return s_c
    else:
        k = e_gamma / e_electron
        if e_gamma > .1:
            t1 = (Z * 2 * np.pi * r_e ** 2)
            t2 = (1 + k) / k ** 2
            t3 = (2 * (1 + k) / (1 + 2 * k)) - (np.log(1 + 2 * k) / k)
            t4 = np.log(1 + 2 * k) / (2 * k)
            t5 = (1 + 3 * k) / ((1 + 2 * k) ** 2)
            s = t1 * (t2 * t3 + t4 - t5)
        else:
            t1 = (Z * 8 / 3 * np.pi * (r_e ** 2))
            t2 = 1 / ((1 + 2 * k) ** 2)
            t3 = 1 + 2 * k + 6 / 5 * (k ** 2) - 1 / 2 * (k ** 3) + 2 / 7 * (k ** 4) - 6 / 35 * (k ** 5) + 8 / 105 * (
                        k ** 6) + 4 / 105 * (k ** 7)
            s = t1 * t2 * t3
        return s


def p_pe(e_gamma):  # Units of barn/atom
    if e_gamma is type(list) or isinstance(e_gamma, np.ndarray):
        for energy in e_gamma:
            s = 0
            k = energy / e_electron
            s += (8 * (2 ** .5) * np.pi) * (r_e ** 2 * alpha ** 4) * ((Z ** 5) / (k ** 3.5))
            s_pe.append(s)
        return s_pe
    else:
        s = 0
        k = e_gamma / e_electron
        s += (8 * (2 ** .5) * np.pi) * (r_e ** 2) * (alpha ** 4) * ((Z ** 5) / (k ** 3.5))
        return s


def p_kn(e_gamma, theta):
    a = e_gamma / .511
    t1 = (1 / (1 + a*(1 - np.cos(theta))))**2
    t2 = (1 + np.cos(theta)**2) / 2
    t3 = 1 + ((a**2 * (1 - np.cos(theta))**2) / ((1 + np.cos(theta)**2) * (1 + a*(1 - np.cos(theta)))))
    return t1*t2*t3


