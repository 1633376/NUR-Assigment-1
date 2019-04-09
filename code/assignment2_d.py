import mathlib.rng
import mathlib.derivative
import numpy as np

# The values of abc found in assigment 2.1.
a = 1.316496837562065814
b = 1.305096297363074420
c = 1.790962180074062715
A = 0.051464524931584120

# Initialize with the seed at the end of assigment 2.1.
rng = mathlib.rng.RNG(499869219)

# The distribution from which we want to sample.
sample_dist = lambda x : (b**2  * (x/b)**(a-1)* np.exp(-(x/b)**c) )*A*4*np.pi
# The enclosing distribution.
enclosing_dist = lambda x : 2
# The transformation for a uniform variable to the enclosing distribution.
enclosed_transform = lambda x : 5*x

# Generate 100 uniform distributed angles.
theta, phi = rng.gen_uniform_spherical_surface_coords(100)
radii = rng.rejection_sampling(sample_dist, \
                               enclosing_dist, enclosed_transform, 100)

# Display the final seed used for the next assigment,
print('Final seed: ', rng.get_seed())
# Empty line to seperate seed from the remaining output
print('') 

# Print the results
print('x, phi, theta')
for pair in zip(radii,phi, theta):
    print(pair)
