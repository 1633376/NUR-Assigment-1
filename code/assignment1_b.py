import mathlib.utils
import mathlib.rng
import matplotlib.pyplot as plt
import numpy as np

# Initialize the random number generator.
rng = mathlib.rng.RNG(5332341) 
print('Initializing seed: ', 5332341)

# Plot sequential random numbers against each other in a scatter plot. 
x_values = rng.gen_next_floats(1001)
plt.scatter(x_values[0:1000], x_values[1:1001], s=2)
plt.savefig('./plots/random_next_current.pdf')
plt.figure()

# Plot 1e6 random points.  
values = rng.gen_next_floats(int(1e6)) 

plt.hist(values, bins=20, range=(0,1),alpha=0.8,edgecolor='black')
plt.savefig('./plots/random_uniformness.pdf')
print('Seed after creating plots: ', rng.get_seed())


