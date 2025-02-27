import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.optimize import bisect

# Define the function
def secret_func(x):
    return np.cos(x**2) - 3 * np.sin(x) + 1

# Generate data
xvals = np.linspace(-3, 3, num=20)
yvals = secret_func(xvals)

# Save the data
np.savetxt("data.txt", np.column_stack((xvals, yvals)))

# Linear interpolation (optimized)
xinterp = np.linspace(-3, 3, num=1000)
yinterp = np.interp(xinterp, xvals, yvals)

# Plot
fig, ax = plt.subplots()
ax.plot(xvals, yvals, "o", label="Data")
ax.plot(xinterp, yinterp, "--", label="Linear interpolation")
ax.legend()

# Cubic spline interpolation
spline = CubicSpline(xvals, yvals)
yinterp2 = spline(xinterp)

# Plot comparison
ytrue = secret_func(xinterp)
fig, ax = plt.subplots()
ax.plot(xvals, yvals, "o", label="Data")
ax.plot(xinterp, yinterp, "--", label="Linear interpolation")
ax.plot(xinterp, yinterp2, "-", label="Cubic spline")
ax.plot(xinterp, ytrue, ":", label="True function")
ax.legend()

# Find roots using SciPy's optimized bisection
root1 = bisect(spline, -1, 1)
root2 = bisect(spline, 2, 2.5)
root3 = bisect(spline, 2.5, 3)

print(f"Roots: {root1}, {root2}, {root3}")

# Plot roots
fig, ax = plt.subplots()
ax.plot(xvals, yvals, "o", label="Data")
ax.plot(xinterp, yinterp, "--", label="Linear interpolation")
ax.plot(xinterp, yinterp2, "-", label="Cubic spline")
ax.scatter([root1, root2, root3], [0, 0, 0], marker="s", color="red", label="Roots")
ax.axhline(0.0, color="k", linestyle="--")
ax.legend()

# Compare with "true" roots
root1_t = bisect(secret_func, -1, 1)
root2_t = bisect(secret_func, 2, 2.5)
root3_t = bisect(secret_func, 2.5, 3)

print(f"Differences in roots: {np.abs(root1 - root1_t)}, {np.abs(root2 - root2_t)}, {np.abs(root3 - root3_t)}")
