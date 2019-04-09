import numpy as np
import matplotlib.pyplot as plt

# The a,b,cfound in the previous assigment for
# m11, m12, m13, m14, m15.
abc_values = np.array([[1.28368, 1.14960, 3.33632],
              [1.54045, 0.94998, 3.74252],
              [1.40908, 0.85051, 3.20000],
              [1.61791, 0.74704, 3.48682],
              [1.60000, 0.94610, 2.90000]])

# Massa's of the halo's in suns masses.
masses = [10e11, 10e12, 10e13, 10e14, 10e15]

#plot the points
labels = ['a', 'b', 'c']
colors = ['red', 'green', 'blue']
for i in range(0,3):
    plt.scatter(masses, abc_values[:,i],c=colors[i], label = labels[i])

plt.legend()
plt.loglog()
plt.show()


