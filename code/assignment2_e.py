import mathlib.rng
import matplotlib.pyplot as plt
import numpy as np

# The values of abc found in assigment 2.1.
a = 1.316496837562065814
b = 1.305096297363074420
c = 1.790962180074062715
A = 0.051464524931584120

# The amount of halo's to generate.
haloes = 1000

# Initialize with the seed at the end of assigment 2.4
# to keep the usage of the random number generator contineus 
# through out the full assigment (see report question 1.b).
rng = mathlib.rng.RNG(1016249662)



# The functions from assigment 2.4 and the new function to plot (last one).
sample_dist = lambda x : (b**2  * (x/b)**(a-1)* np.exp(-(x/b)**c) )*A*4*np.pi
enclosing_func = lambda x : 2
enclosed_transform = lambda x : 5*x
N = lambda x : sample_dist(x)*100   #N(x) = p(x)*<N_{sat}> (plot function)

# Create an array with the bins.
bins = np.logspace(-4, np.log10(5), 21)

# Create a matrix that stores all radii for each iteration.
# This matrix is not used in this assigment, but is needed
# for assigment 2.g. 
radi_all = np.zeros((haloes, 100)) 

#
# Generate the samples
#

# The first halo is generated outside a loop to obtain the bin-widths,
# bin-centers and the initial histogram. This histogram is used to
# create a combined histogram by adding the histograms for each halo
# to it. The final histogram is then obtained by dividing this combined
# histogram by the bin width and the number of haloes.

# Radii of first halo.
radi = rng.rejection_sampling(sample_dist, \
                              enclosing_func, enclosed_transform, 100)
histogram, bin_edges = np.histogram(radi, bins=bins) 
bin_widths = bins[1:] - bins[:-1]
bin_centers = (bins[0:-1] + bins[1:])/2

# Remaining haloes are created in a loop
for i in range(1, haloes):
    radi = rng.rejection_sampling(sample_dist, \
                                  enclosing_func, enclosed_transform, 100)
    histogram += np.histogram(radi, bins=bins)[0] # add histograms together
    radi_all[i] = radi

# Divide by the number of haloes to obtain the average and
# divide by bin width to correct for different sized bins.
histogram = np.array(histogram) 
histogram_normed = histogram/ (haloes*bin_widths)

# Plot the histogram and the function.
x_plot = np.linspace(0.002, 5, haloes) #x values to plot N(x) for
plt.bar(bin_centers, histogram_normed, width=bin_widths, color='orange', edgecolor='black')
plt.plot(x_plot, N(x_plot), c='red')
plt.loglog()
plt.xlim(1e-3, 10)
plt.savefig('./plots/assignment2e.pdf')
    
# Save the generated radii for assigment 2.g.
np.save('radii_2e', radi_all)

# No need to print the final seed as the random number generator is
# not needed for any other assigment.
