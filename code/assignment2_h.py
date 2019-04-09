import numpy as np
import mathlib.interpolate3D as intp3d
import mathlib.integrate as intgrt

# Values of the a, b and c parameters.
a_values = np.arange(1.1, 2.6, 0.1) #15
b_values = np.arange(0.5, 2.1, 0.1) #16
c_values = np.arange(1.5, 4.1, 0.1) #26 

# Row is a , column is b , depth is c.
table = np.zeros((len(a_values), len(b_values), len(c_values)))

for row, a_val in enumerate(a_values):
    for column, b_val in enumerate(b_values):
        for depth, c_val in enumerate(c_values):
            
            # The function to normalize (simmilar as in assigment 2.a)
            # This function unfortunatly couldn't be split over multiple
            # lines so it might look slightly ugly in the report.
            density = lambda x: b_val**2 *(x/b_val)**(a_val-1)*np.exp(-(x/b_val)**c_val)*4*np.pi
            
            # Insert the value in the table.
            table[row][column][depth] = 1/intgrt.romberg(density, 0, 5, 15)

# Save the table to the disk to use it later in the next assigment.
np.save('table_2h', table)


