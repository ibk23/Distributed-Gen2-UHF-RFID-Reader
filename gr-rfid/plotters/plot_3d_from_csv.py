# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import csv

x_col=8
y_col=13
z_col=11

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

with open('../misc/data/MonzaX-CW.csv') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader, None)
    for row in reader:
        print(row)
        try:
            ax.scatter(float(row[x_col]), float(row[y_col]), float(row[z_col]), c='r', marker='o')
        except Exception as e:
            print("Could not print row due to",e)

ax.set_xlabel(headers[x_col])
ax.set_ylabel(headers[y_col])
ax.set_zlabel(headers[z_col])

print(headers)
plt.show()
