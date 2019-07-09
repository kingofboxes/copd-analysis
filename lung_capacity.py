# Import the required libraries.
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.gridspec as gridspec

# ===== FUNCTIONS ===== #

# Fit the curve to this.
def func(x, a, b, c):
    return a - b * np.exp(-c * x)

# Output summary report.
def output(yc1, yc2, yc3, tpi, ci):
    print('')
    print('=== SUMMARY REPORT ===')
    print('')
    print('FEV1 Trial #1:', '%.4f' % yc1[FEV1_INDEX], 'L')
    print('FVC Trial #1: ', '%.4f' % yc1[FVC_INDEX], 'L')
    print('')
    print('FEV1 Trial #2:', '%.4f' % yc2[FEV1_INDEX], 'L')
    print('FVC Trial #2: ', '%.4f' % yc2[FVC_INDEX], 'L')
    print('')
    print('FEV1 Trial #3:', '%.4f' % yc3[FEV1_INDEX], 'L')
    print('FVC Trial #3 :', '%.4f' % yc3[FVC_INDEX], 'L')
    print('')
    print('Average Tiffeneau-Pinelli Index: ', '%.4f' % tpi)
    print('')
    print('95% Confidence Interval: ' + '[%.4f' % ci[0] + ', ' +  '%.4f]' % ci[1])
    print('')
    print('=== SUMMARY REPORT ===')
    print('')

# ===== END FUNCTIONS ===== #

# Define amount of data points and initial curve.
x = np.linspace(0, 5, 100)
y = func(x, 5, 5, 2)

# Generate noise.
yn1 = y + np.random.normal(0,0.1,len(x))
yn1[0] = 0
yn2 = y + np.random.normal(0,0.2,len(x))
yn2[0] = 0
yn3 = y + np.random.normal(0,0.4,len(x))
yn3[0] = 0

# Hash defines go here.
FEV1_INDEX = int(len(x)/5 - 1)
FVC_INDEX = int(len(x) - 1)

# Create the figure and divide it into 2 by 3 grid.
fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(2, 3)

# Create the 3 subplots at the top.
for i in range(3):

    # Add the subplot.
    ax = fig.add_subplot(gs[0, i])

    # Red, Green & Blue for the three different plots.
    if i == 0: ax.scatter(x, yn1, c='r', marker='.', label='Trial #%d' % (i+1))
    elif i == 1: ax.scatter(x, yn2, c='b', marker='.', label='Trial #%d' % (i+1))
    else: ax.scatter(x, yn3, c='g', marker='.', label='Trial #%d' % (i+1))

    # Customisation regarding axis.
    # ax.set_label('Test Data')
    ax.set_title('Spirometry Test %d' % (i+1))
    ax.set_ylabel('Volume of Air (L)')
    ax.set_xlabel('Time (s)')
    ax.set_yticks(np.arange(0, 6, step=1))
    ax.set_xticks(np.arange(0, 6, step=1))
    ax.grid(True)
    ax.legend()

# Align the labels.   
fig.align_labels()

# Find the variables for the curve fit.
popt1, pcov1 = curve_fit(func, x, yn1)
popt2, pcov2 = curve_fit(func, x, yn2)
popt3, pcov3 = curve_fit(func, x, yn3)
yc1 = func(x, *popt1)
yc2 = func(x, *popt2)
yc3 = func(x, *popt3)
tpi = round(float((yc1[FEV1_INDEX]/yc1[FVC_INDEX] + yc2[FEV1_INDEX]/yc2[FVC_INDEX] + yc3[FEV1_INDEX]/yc3[FVC_INDEX])/3), 4)

# Statistical Analysis
TPI = []
TPI.append(yc1[FEV1_INDEX]/yc1[FVC_INDEX])
TPI.append(yc2[FEV1_INDEX]/yc2[FVC_INDEX])
TPI.append(yc3[FEV1_INDEX]/yc3[FVC_INDEX])

std = np.std(TPI, ddof=1)
mean = np.mean(TPI)
ci = [mean - 2.776 * std/(math.sqrt(3)), mean + 2.776 * std/(math.sqrt(3))]

# Output summary report.
output(yc1, yc2, yc3, tpi, ci)

# Create the averaged subplot at the bottom.
ax = fig.add_subplot(gs[1, :])
ax.plot(x, yc1, 'r-', label="Fitted Curve: Trial #1")
ax.plot(x, yc2, 'b-', label="Fitted Curve: Trial #2")
ax.plot(x, yc3, 'g-', label="Fitted Curve: Trial #3")
ax.set_ylabel('Volume of Air (L)')
ax.set_xlabel('Time (s)')
ax.set_yticks(np.arange(0, 6, step=1))
ax.set_xticks(np.arange(0, 6, step=1))
ax.set_title('Spirometry Results')
ax.text(1,1, "Tiffeneau-Pinelli Index: " + str(tpi))
ax.grid(True)
ax.legend()

# Show figure.
# plt.show()

# # Save figure.
# plt.savefig('output/lung_capacity.png')
plt.close(fig)