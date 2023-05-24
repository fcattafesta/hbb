import numpy as np
import matplotlib.pyplot as plt

# Generate some random data
np.random.seed(0)
data = np.random.normal(0, 1, 1000)

# Compute the histogram using pyplot.hist()
hist, bin_edges, _ = plt.hist(data, bins=10)

# Compute the bin centers
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# Compute the error bars (sqrt(N) for Poisson statistics)
errors = np.sqrt(hist)

# Plot the histogram as points with error bars
plt.errorbar(bin_centers, hist, yerr=errors, fmt='o', ecolor='red', capsize=3)

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram with Error Bars')

# Show the plot
plt.show()
