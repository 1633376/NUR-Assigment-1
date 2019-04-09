import mathlib.interpolate as interp
import matplotlib.pyplot as plt
import numpy as np 

# The values of abc found in assigment 2.1.
a = 1.316496837562065814
b = 1.305096297363074420
c = 1.790962180074062715
A = 0.051464524931584120

# The volume number density function that is
# used to create the y-values of the points.
density = lambda x: A*(x/b)**(a-3)* np.exp(-(x/b)**c)

# The points.
points_x = np.array([1e-4, 1e-2, 1e-1, 1, 5.0])
points_y = density(points_x)

# Take the logarithm.  
points_x_log = np.log10(points_x)
points_y_log = np.log10(points_y)

# Points to interpolate.
interpolate_x = np.linspace(1e-4, 5, 2000) 
interpolate_x_log = np.log10(interpolate_x)

# Create the interpolated points.
lin_interp = list()
poly_interp = list()

for x in interpolate_x_log:
    lin_interp.append(10**interp.interpolate_linear(points_x_log,\
                                                    points_y_log, x))
    poly_interp.append(10**interp.interpolate_neville(points_x_log, \
                                                    points_y_log, x))

# First only plot the points and then plot the points 
# with the interpolated values.
plt.loglog()
plt.scatter(points_x, points_y, s=15, color = 'black',zorder=1)
plt.savefig('./plots/points.pdf')
plt.plot(interpolate_x, lin_interp, label = 'lineair',
         linestyle = '--', zorder = 0)
plt.plot(interpolate_x, poly_interp, label= 'polynomial',
         linestyle = '-.', zorder = 0)
plt.legend()
plt.savefig('./plots/interpolate.pdf')



  