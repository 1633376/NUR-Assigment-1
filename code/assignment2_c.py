import mathlib.derivative
import numpy as np

# The values of abc found in assigment 2.1.
a = 1.316496837562065814
b = 1.305096297363074420
c = 1.790962180074062715
A = 0.051464524931584120

# The analytical derivative and the density.
analytical = (A*100*((a-3) -c))/(b*np.exp(1)) 
n = lambda x: (x/b)**(a-3)* np.exp(-(x/b)**c)*A*100

# Print the results.
print('Analytical: {0:.12f}'.format(analytical))
print('Numeric: {0:.12f}'.format(mathlib.derivative.ridder(n,b,1e-13)))
