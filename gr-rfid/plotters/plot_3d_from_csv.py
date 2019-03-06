# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import csv


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

with open('../misc/data/RN16ForMatlab.csv') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader, None)
    for row in reader:
        print(row)
        try:
            ax.scatter(float(row[2]), float(row[3]), float(row[1]), c='r', marker='o')
        except Exception as e:
            print("Could not print row due to",e)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
