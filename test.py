import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(24)

# Generate time series
n_points = 1000
time = np.arange(n_points)
mean = 0
std_dev = 1

# Generate a random walk
random_walk = np.cumsum(np.random.normal(0, 0.1, n_points))

# Center the random walk around the mean and increase variance
centered_series = (random_walk - np.mean(random_walk)) * 3 + mean

# Calculate mean and standard deviation
series_mean = np.mean(centered_series)
series_std = np.std(centered_series)

plt.rcParams.update({'font.size': 18})

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(time, centered_series, label='Spread')
plt.axhline(y=series_mean, color='r', linestyle='--', label='Spread Mean')
plt.axhline(y=series_mean + 0.75*series_std, color='g', linestyle=':', label='Spread Mean + 1 Std Dev')
plt.axhline(y=series_mean - 0.75*series_std, color='g', linestyle=':', label='Spread Mean - 1 Std Dev')

plt.title('Spread (P1, P2)', fontsize=24)
plt.xlabel('Time', fontsize=18)
plt.ylabel('Value', fontsize=18)
plt.legend(fontsize=16)

plt.xticks([])
plt.yticks([])

plt.tight_layout()
plt.savefig('pairs_trading_spread_graph.png')