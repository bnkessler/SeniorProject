import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

Z = 11
r_e = 0.07941  # barn
e_electron = .51099895000  # MeV
alpha = 0.00729735


def p_c(e_gamma):
    for energy in e_gamma:
        k = energy / e_electron
        t1 = (Z * 2 * np.pi * r_e ** 2)
        t2 = (1 + k) / k ** 2
        t3 = (2 * (1 + k) / (1 + 2 * k)) - (np.log(1 + 2 * k) / k)
        t4 = np.log(1 + 2 * k) / (2 * k)
        t5 = (1 + 3 * k) / ((1 + 2 * k) ** 2)
        s = t1 * (t2 * t3 + t4 - t5)
        s_c.append(s)


def p_pe(e_gamma):  # Units of barn/g
    for energy in e_gamma:
        s = 0
        k = energy / e_electron
        s += (8 * (2 ** .5) * np.pi) * (r_e ** 2 * alpha ** 4) * ((Z ** 5) / (k ** 3.5))
        # print(s)
        s_pe.append(s)


energies = np.linspace(0.01, 1, 1000)
s_pe, s_c, s_t = [], [], []
p_pe(energies)
p_c(energies)
for i in range(len(energies)):
    s_t.append(s_pe[i] + s_c[i])

fig1, [ax1, ax2] = plt.subplots(2)
# Log Plot
ax1.loglog(energies, s_pe, "r-", label="$\u03C3_{pe}$")
ax1.loglog(energies, s_c, "b-", label="$\u03C3_{c}$")
ax1.loglog(energies, s_t, "k--", label="$\u03C3_{c+pe}$")

ax1.set_title("Gamma Ray Attenuation [barn/atom] vs Energy [MeV]")
ax1.set_xlabel("Energy [MeV]")
ax1.set_ylabel("Gamma Ray Attenuation [barn/atom]")
ax1.legend()

# Non-Log Plot
ax2.plot(energies, s_pe, "r-", label="$\u03C3_{pe}$")
ax2.plot(energies, s_c, "b-", label="$\u03C3_{c}$")
ax2.plot(energies, s_t, "k--", label="$\u03C3_{c+pe}$")

ax2.set_xlabel("Energy [MeV]")
ax2.set_ylabel("Gamma Ray Attenuation [barn/atom]")
ax2.legend()

# plt.show()

x_pe = sorted([0.2916640776023704, 0.17012542798525893, 0.09923286228832551, 0.06251534353689711, 0.039995090972036657,
               0.02126959386668691, 0.014251026703029978, 0.01, 0.029848079169243275, 0.051171730071146046,
               0.07998527336796708, 0.1289341296525715, 0.21434022335148567, 0.40304280305680523, 0.5400593278542372,
               1, 0.7125950633568408])
y_pe = sorted([0.0441321661704945, 0.1867792689836968, 0.7905004070570255, 2.731263722800847, 9.020793790531423,
               45.72354139422552, 117.84975156190525, 290.36018399677124, 19.85647246589344, 4.691683114474265,
               1.4529068195715225, 0.3930118039281055, 0.09714324069179653, 0.019602329826462782, 0.010195102779946461,
               0.00282065292413126, 0.0055469716219741045], reverse=True)
x_c = [0.01, 0.01469684386112446, 0.020309176209047358, 0.029848079169243275, 0.0406158598837698,
       0.050389626250651506, 0.06963207939763882, 0.09923286228832551, 0.15040335536380245, 0.21434022335148567,
       0.3007882518043099, 0.4774520538566129, 0.7348872892180384, 1, 0.5923457145875803, 0.367466194073669,
       0.2578524352884274, 0.11937766417144363]
y_c = [0.36731187157481726, 0.4399027159972232, 0.48141263286799674, 0.5268394912259641, 0.5511359509536734,
       0.5511359509536734, 0.5511359509536734, 0.5268394912259641, 0.49238826317067413, 0.44993197000986745,
       0.4111364806573184, 0.3591242692095019, 0.2998631348575567, 0.2678995770570536, 0.3281586950982565,
       0.3930118039281055, 0.43009702008392386, 0.515095922345358]

y_pe_log = [np.log10(i) for i in y_pe]
y_c_log = [np.log10(i) for i in y_c]


def best_fit_pe(xdata, a, b, c):
    y_pe_new = []
    for x in xdata:
        y_pe_new.append(a / x + b / x ** 2 + c)
    return y_pe_new


def best_fit_c(xdata, a, b):
    y_c_new = []
    for x in xdata:
        y_c_new.append(a * x + b)
    return y_c_new


# def best_fit_log_pe(xdata, a, b):
#     y_pe_log_new = []
#     for x in xdata:
#         y_pe_log_new.append(np.log10(a * x ** .15 + b))
#     return y_pe_log_new
#
#
# def best_fit_log_c(xdata, a, b):
#     y_c_log_new = []
#     for x in xdata:
#         y_c_log_new.append(a * x ** 2 + b)
#     return y_c_log_new


params_pe = scipy.optimize.curve_fit(best_fit_pe, x_pe, y_pe)
# params_log_pe = scipy.optimize.curve_fit(best_fit_log_pe, x_pe, y_pe_log)
params_c = scipy.optimize.curve_fit(best_fit_c, x_c, y_c)
# params_log_c = scipy.optimize.curve_fit(best_fit_log_c, x_c, y_c_log)

y_pe_fit = best_fit_pe(x_pe, *params_pe[0])
y_c_fit = best_fit_c(x_c, *params_c[0])
# y_pe_fit_log = best_fit_log_pe(x_pe, *params_log_pe[0])
# y_c_fit_log = best_fit_log_c(x_c, *params_log_c[0])

# fig2, [ax1, ax2] = plt.subplots(2)
# ax1.loglog(x_pe, y_pe, "r.")
# ax1.loglog(x_c, y_c, "b.")
# ax1.plot(x_pe, y_pe_fit_log, "y-", label="balls")

# ax1.set_title("Gamma Ray Attenuation [barn/atom] vs Energy [MeV]")
# ax1.set_xlabel("Energy [MeV]")
# ax1.set_ylabel("Gamma Ray Attenuation [barn/atom]")
# ax1.legend()

fig2, ax1 = plt.subplots(1)
ax1.scatter(x_pe, y_pe)
ax1.scatter(x_c, y_c)
ax1.plot(x_pe, y_pe_fit,
         label=f"$\u03C3_{{pe}}$={round(params_pe[0][0], 5)}/x"
               f" + {round(params_pe[0][1], 5)}/$x^2$ + {round(params_pe[0][2], 5)}")
ax1.plot(x_c, y_c_fit,
         label=f"$\u03C3_c$={round(params_c[0][0], 5)}*x + {round(params_c[0][1])} ")

ax1.set_title("Gamma Ray Attenuation [${cm^2}$/g] vs Energy [MeV]")
ax1.set_xlabel("Energy [MeV]")
ax1.set_ylabel("Gamma Ray Attenuation [${cm^2}$/g]")
ax1.legend()

plt.show()
