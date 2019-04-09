import mathlib.roots as roots
import numpy as np


# The values of abc found in assigment 2.1.
a = 1.316496837562065814
b = 1.305096297363074420
c = 1.790962180074062715
A = 0.051464524931584120


# The maximum x and y coordinate,
x_max = b*((a-1)/c)**(1/c)
y_max = (b**2  * (x_max/b)**(a-1)* np.exp(-(x_max/b)**c) )*A*4*np.pi*100


# The function to put equal to zero and solve. 
root_func = lambda x: (b**2 *(x/b)**(a-1)* np.exp(-(x/b)**c))*A*4*np.pi*100 - y_max/2 
# The derivative of this function, needed for newton_raphson.
root_der = lambda x: 4*np.pi*100*b*np.exp(-(x/b)**c)*((a-1)*(x/b)**(a-2)-c*(x/b)**(a-1)*(x/b)**(c-1)) 

# Print the roots
print('Left root: {0:.7f}'
      .format(roots.newton_raphson(root_func, root_der, 0, 0.3, 1e-10)))
print('Right root: {0:.7f}'
      .format(roots.newton_raphson(root_func, root_der, 1, 2, 1e-10)))
