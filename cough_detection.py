# Import the required libraries.
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# Read all the numbers in a list.
f = open(sys.argv[1], "r")
y = [int(i) for i in f.read().splitlines()]
x = np.linspace(0, 10, len(y))
f.close()

# List of peak indices.
peak = []

# Define a partition.
par = 80                        # 10 second samples, divide again to change partition size (currently 8 partitions per second block).
seg = int(len(y) / par)         # Each segment is 125 ms, or 0.125s.
thres = 200                     # Threshold for coughing, manually defined.

# Go through each partition and mark the largest point in each parititon above the threshold.
start = 0
finish = seg-1

for i in range(0, par):

    # Temporary variables for storing the index and max value of each partition.
    temp_max = 0
    temp_index = 0

    for a in range(start, finish):
        if y[a] > temp_max:
            temp_max = y[a]
            temp_index = a

    if temp_max > thres:
        peak.append(temp_index)

    start += seg
    finish += seg

# Remove excess peaks that exist within the partitions.
# First checks whether there exists another peak within the next partition.
# If it exists, check for which value is bigger.
# Save the bigger one, remove the smaller one.
for i in peak:
    curr = peak.index(i)
    if curr != len(peak)-1:
        if i+seg - peak[curr+1] > 0:
            if y[peak[curr]] < y[peak[curr+1]]:
                peak.pop(curr)
            else:
                peak.pop(curr+1)

# Plot the graph and alter the figure.
plt.plot(x, y, 'b-', label="Data Stream")
plt.ylabel('Voltage (V)')
plt.xlabel('Time (s)')
plt.title('Patient Coughing Data')
plt.grid(True)

############### OUTPUT / DISPLAY OPTIONS ###############

# Specify which mode to use to display graph; solid lines or peak points.
if sys.argv[2] is '1':

    # Extract the boundaries and plot on the graph as solid red lines.
    for p in peak:

        # Checks for any potential boundary errors.
        if p-seg > 0 and p+seg < len(y):
            temp_x = [x[i] for i in range(p-seg, p+seg)]
            temp_y = [y[i] for i in range(p-seg, p+seg)]
        elif p-seg > 0 and p+seg > len(y):
            temp_x = [x[i] for i in range(p-seg, len(y))]
            temp_y = [y[i] for i in range(p-seg, len(y))]
        elif p-seg < 0 and p+seg < len(y):
            temp_x = [x[i] for i in range(0, p+seg)]
            temp_y = [y[i] for i in range(0, p+seg)]
        else:
            temp_x = [x[i] for i in range(0, len(y))]
            temp_y = [y[i] for i in range(0, len(y))]

        # Plot the solid lines onto the figure.

        if peak.index(p) != len(peak) - 1:   
            plt.plot(temp_x, temp_y, 'r-')
        else:
            plt.plot(temp_x, temp_y, 'r-', label="Coughing Region(s)")

elif sys.argv[2] is '0':
    
    # Plot the peaks onto the graph.
    for i in range(0, len(peak)):
        if i != len(peak)-1:
            plt.plot(x[peak[i]], y[peak[i]], 'r*')
        else:
            plt.plot(x[peak[i]], y[peak[i]], 'r*', label="Coughing Peak(s)")

# Output report.
print('')
print('=== SUMMARY REPORT ===')
print('')
print('The patient has coughed %d time(s) in the last 10 seconds.' % len(peak))
print('')
print('=== SUMMARY REPORT ===')
print('')

# Show the graph.
plt.legend()
# plt.show()

# Save figure.
plt.savefig('out/cough_detection.png')
plt.close()