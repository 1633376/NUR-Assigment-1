import mathlib.utils as utils
import matplotlib.pyplot as plt
import numpy as np


# Read in the radii from assigment 2.e.
radii_matrix = np.load('radii_2e.npy')

#
# Create the histograms for each of the 100 generated radii (see assigment 2.e)
# and find the bin with the maximal number of counts over the full dataset 
# (i.e the maximum within all the histograms).
#

# The array in which the histograms are stored.
histograms = list()
# The bins for each histogram.
bins = np.logspace(-4, np.log10(5), 21)
# The histogram with the maximum bin.
max_hist_idx = 0                        
# The bin with the maximum number of counts. 
max_bin_idx = 0                         


for idx in range(radii_matrix.shape[0]):
    
    # Create the histogram and save it.
    histogram = np.histogram(radii_matrix[idx], bins = bins)[0]
    histograms.append(histogram)  

    # Loop over all bins in this new histogram.
    for bin_idx, bin_counts in enumerate(histogram):

        # Check if a bin in the new histogram contains
        # more counts than the known maximum and save the bin index and the 
        # histogram index if this is true.
        if histograms[max_hist_idx][max_bin_idx] < bin_counts: 
            max_hist_idx = idx
            max_bin_idx = bin_idx

# For each histogram take the bin with the index of max_bin_idx
# and save the counts in an array. 
bin_counts = np.array([hist[max_bin_idx] for hist in histograms])
bin_counts =  bin_counts

# Print the median, 16th percentile and 84th percentile for the counts.
print('Median: {0:.1f}'.format(utils.median(bin_counts)))
print('Percentile 16th: {0:.1f}'.format(utils.percentile(bin_counts, 16)))
print('Percentile 84th: {0:.1f}'.format(utils.percentile(bin_counts, 84)))

# Plot the histogram for the counts with bin width of 1.
plt.hist(bin_counts, density=True,
         bins=np.arange(min(bin_counts), max(bin_counts) + 1, 1),
         edgecolor='black')

#
# Overplot the Poisson distribution.
#

# Mean events
mean = int(sum(bin_counts)/len(bin_counts)) 
x = np.arange(1, 60, 1)

# Poisson function can't take arrays :(
y = [utils.poisson(mean, float(x_val)) for x_val in x] 
plt.plot(x, y, label='Poisson(mean:{0:.1f})'.format(mean))
plt.legend()

# Save the plot
plt.savefig('./plots/poisson.pdf')

