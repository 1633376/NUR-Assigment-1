import mathlib.rng
import mathlib.integrate 
import numpy as np

# Recreate the random number generator with the last seed of the previous exercise.
# This is done to make the execution of the random number generator 
# continues through out the all assigments. See assigment 1.b in
# the report for more information.  
rng = mathlib.rng.RNG(3197832550)

# Generate the random numbers.
a = rng.gen_next_float_range(1.1, 2.5)
b = rng.gen_next_float_range(0.5, 2)
c = rng.gen_next_float_range(1.5, 4)

# The density function in spherical coordinates integrated
# over the angles theta and phi.
density = lambda x: b**2  * (x/b)**(a-1)* np.exp(-(x/b)**c) * 4 *np.pi

# Find the normalization constant.
A = 1/mathlib.integrate.romberg(density, 0, 5, 15)

for label,value in zip(['a','b','c','A'], [a,b,c,A]):
    print(label + ' = {0:.18f}'.format(value))

# Print the seed, which is needed in assigment 2.d.
print('Final seed: ', rng.get_seed())