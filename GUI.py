import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(45)

# Generate random energy consumption data
num_intervals = 24 * 60 * 12  # 24 hours * 60 minutes * 12 intervals per minute (5 sec intervals)
energy_consumption = np.random.normal(loc=16, scale=0.7, size=num_intervals)  # Random normal distribution

# Introduce idle time
idle_end_index = 0
total_idle_time = 0.0
i = 0
while idle_end_index < num_intervals-360:
    idle_start_index = idle_end_index + np.random.randint(720, 1440)  # Random start index for idle time (at least 20 minutes)
    idle_end_index = idle_start_index + np.random.randint(60, 360)  # Idle time lasts for 20 minutes (1200 intervals)
    energy_consumption[idle_start_index:idle_end_index] = 2 # Set energy consumption to a low value during idle time
    total_idle_time += (idle_end_index - idle_start_index)

    
# Create time intervals at 5-second intervals
start_time = pd.Timestamp('2024-02-14 00:00:00')
time_intervals = pd.date_range(start=start_time, periods=num_intervals, freq='5s')

# Zoom into a 6-hour window
end_time = start_time + pd.Timedelta(hours=24)
mask = (time_intervals >= start_time) & (time_intervals <= end_time)
zoomed_time_intervals = time_intervals[mask]
zoomed_energy_consumption = energy_consumption[mask]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(zoomed_time_intervals, zoomed_energy_consumption,color='blue', linestyle='-')
plt.title('Energy Consumption of Welding Machine')
plt.xlabel('Time')
plt.ylabel('Energy Consumption')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# calculate total energy consumption
time_interval = 5
total_energy_consumption = np.trapz(energy_consumption, dx=time_interval / 3600)
print(total_energy_consumption)

# calculate total idle and active time in hours
total_active_time = num_intervals - total_idle_time
total_active_time /= 12*60
total_idle_time /= 12*60
print("Total active time: ", total_active_time)
print("Total idle time: ", total_idle_time)
print("num_intervals: ", num_intervals)