# Import the required libraries.
import math
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Define 'x' and 'f'.
x = sp.symbols('x')
f = 5 - 5 * math.e**(-3.5*x)

# Define an array of numbers.
b = []
a = np.linspace(0, 5, 100)
for i in a: b.append(f.subs(x, i))

# Generate noise.
nse = []
for i in range(3): nse.append(np.random.normal(0,0.05,len(a)))
nse.append(np.array((nse[0] + nse[1] + nse[2])/3))

# Create the figure and divide it into 2 by 3 grid.
fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(2, 3)

# Create the 3 subplots at the top.
for i in range(3):
    ax = fig.add_subplot(gs[0, i])

    # Red, Green & Blue for the three different plots.
    if i == 0:
        ax.plot(a, b+nse[i], c='r', label='Patient Data')
    elif i == 1: 
        ax.plot(a, b+nse[i], c='b', label='Patient Data')
    elif i == 2: 
        ax.plot(a, b+nse[i], c='g', label='Patient Data')

    # Customisation regarding axis.
    ax.set_label('Test Data')
    ax.set_title('Spirometry Test %d' % (i+1))
    ax.set_ylabel('Capacity (L)')
    ax.set_xlabel('Time (s)')
    ax.set_yticks(np.arange(0, 6, step=1))
    ax.set_xticks(np.arange(0, 6, step=1))
    ax.grid(True)
    ax.legend()

# Align the labels.   
fig.align_labels()

# Create the averaged subplot at the bottom.
ax = fig.add_subplot(gs[1, :])
ax.plot(a, b+nse[3], c='black', label='Averaged Data')
ax.set_ylabel('Capacity (L)')
ax.set_xlabel('Time (s)')
ax.set_yticks(np.arange(0, 6, step=1))
ax.set_xticks(np.arange(0, 6, step=1))
ax.set_title('Spirometry Results')
ax.grid(True)
ax.legend()

# Show figure.
plt.show()