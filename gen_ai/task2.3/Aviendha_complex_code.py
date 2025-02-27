import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# generate data
def secret_func(x):
    return np.cos(x**2) - 3 * np.sin(x) + 1

xvals = np.linspace(-3, 3, num=20)
yvals = secret_func(xvals)

fig, ax = plt.subplots()
ax.plot(xvals, yvals, marker="o")
ax.axhline(y=0, linestyle="--", color="k")

# save it out
data = np.empty((xvals.shape[0], 2), dtype=np.float64)
data[:, 0] = xvals
data[:, 1] = yvals
np.savetxt("data.txt", data)

# linear interpolation
def compute_interp_parameters(xvals, yvals):
    n_intervals = len(xvals) - 1
    slopes = np.empty((n_intervals,), dtype=np.float64)
    intercepts = np.empty((n_intervals,), dtype=np.float64)

    for i in range(n_intervals):
        # get points
        x1 = xvals[i]
        x2 = xvals[i + 1]
        y1 = yvals[i]
        y2 = yvals[i + 1]

        delta_x = x2 - x1
        delta_y = y2 - y1

        slopes[i] = delta_y / delta_x

        intercepts[i] = y1 - slopes[i] * x1

    return slopes, intercepts

def do_interpolation(x, xvals, yvals, slopes, intercepts):
    # figure out the appropriate range for x
    if x < xvals[0] or x > xvals[-1]:
        raise ValueError(f"invalid value {x}")

    for i in range(len(xvals) - 1):
        if x >= xvals[i] and x <= xvals[i + 1]:
            idx = i
            break

    y = slopes[idx] * x + intercepts[idx]

    return y

# test it out
slopes, intercepts = compute_interp_parameters(xvals, yvals)

xinterp = np.linspace(-3, 3, num=1000)

yinterp = [do_interpolation(x, xvals, yvals, slopes, intercepts) for x in xinterp]

# plot it
fig, ax = plt.subplots()
ax.plot(xvals, yvals, linestyle="", marker="o", label="Data")
ax.plot(xinterp, yinterp, linestyle="-", label="Linear interpolation")
ax.legend();

# now do a cubic spline
spline = CubicSpline(xvals, yvals)

yinterp2 = spline(xinterp)

# plot it again
ytrue = secret_func(xinterp)

fig, ax = plt.subplots()
ax.plot(xvals, yvals, linestyle="", marker="o", label="Data")
ax.plot(xinterp, yinterp, linestyle="--", label="Linear interpolation")
ax.plot(xinterp, yinterp2, linestyle="-", label="Cubic spline")
ax.plot(xinterp, ytrue, linestyle=":", label="True function")
ax.legend();

# root finding
def bisection(func, a, b, tol=2e-12):
    aval = func(a)
    bval = func(b)

    # check the signs
    if (np.sign(aval) == 0.0):
        raise ValueError("a is already a root of this function!")
    if (np.sign(bval) == 0.0):
        raise ValueError("b is already a root of this function!")

    if np.sign(aval) == np.sign(bval):
        raise ValueError("the function does not change sign on the interval")

    while abs(aval) > tol:
        newx = (a + b) / 2
        newy = func(newx)

        if np.sign(newy) == np.sign(aval):
            # replace a with new value
            a = newx
            aval = newy
        else:
            # replace b with new value
            b = newx
            bval = newy

    return a

root1 = bisection(spline, -1, 1)
print("root: ", root1)

spline(root1)

root2 = bisection(spline, 2, 2.5)
print("root: ", root2)

root3 = bisection(spline, 2.5, 3)
print("root: ", root3)

# add to the plot
fig, ax = plt.subplots()
ax.plot(xvals, yvals, linestyle="", marker="o", label="Data")
ax.plot(xinterp, yinterp, linestyle="--", label="Linear interpolation")
ax.plot(xinterp, yinterp2, linestyle="-", label="Cubic spline")
ax.scatter([root1, root2, root3], [0, 0, 0], marker="s", color="C3", label="Roots")
ax.axhline(0.0, color="k", linestyle="--")
ax.legend();

# "true" roots
root1_t = bisection(secret_func, -1, 1)
root2_t = bisection(secret_func, 2, 2.5)
root3_t = bisection(secret_func, 2.5, 3)

print(f"difference in root1: {np.abs(root1 - root1_t)}")
print(f"difference in root2: {np.abs(root2 - root2_t)}")
print(f"difference in root3: {np.abs(root3 - root3_t)}")
