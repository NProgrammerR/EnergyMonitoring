import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(45)

# Generate random energy consumption data
num_intervals = 24 * 60 * 12  # 24 hours * 60 minutes * 12 intervals per minute (5 sec intervals)
energy_consumption = np.random.normal(loc=16, scale=0.7, size=num_intervals)  # Random normal distribution

# Introduce idle time
idle_consumption = 2
idle_end_index = 0
total_idle_time = 0.0
i = 0
while idle_end_index < num_intervals-360:
    idle_start_index = idle_end_index + np.random.randint(720, 1440)  # Random start index for idle time (at least 20 minutes)
    idle_end_index = idle_start_index + np.random.randint(60, 360)  # Idle time lasts for 20 minutes (1200 intervals)
    energy_consumption[idle_start_index:idle_end_index] = idle_consumption # Set energy consumption to a low value during idle time
    total_idle_time += (idle_end_index - idle_start_index)

    
# Create time intervals at 5-second intervals
start_time = pd.Timestamp('2024-02-14 00:00:00')
time_intervals = pd.date_range(start=start_time, periods=num_intervals, freq='5s')

# Zoom into a 6-hour window
end_time = start_time + pd.Timedelta(hours=6)
mask = (time_intervals >= start_time) & (time_intervals <= end_time)
zoomed_time_intervals = time_intervals[mask]
zoomed_energy_consumption = energy_consumption[mask]

# calculate total energy consumption
time_interval = 5
total_energy_consumption = np.trapz(energy_consumption, dx=time_interval / 3600)
print("Total consumption: ", total_energy_consumption)

# calculate total idle and active time in hours
total_active_time = num_intervals - total_idle_time
total_active_time /= 12*60
total_idle_time /= 12*60
print("Total active time: ", total_active_time)
print("Total idle time: ", total_idle_time)
print("num_intervals: ", num_intervals)

# calculate idle consumption
total_idle_consumption = idle_consumption * total_idle_time
total_active_consumption = total_energy_consumption - total_idle_consumption
print("Total active consumption: ", total_active_consumption)
print("Total idle consumption: ", total_idle_consumption)

# calculate active consumption
total_active_consumption = total_energy_consumption - total_idle_consumption

# Plot the data
fig, axs = plt.subplots(1, 3, figsize=(15, 6))  # 1 row, 2 columns

# First subplot
axs[0].plot(zoomed_time_intervals, zoomed_energy_consumption,color='blue', linestyle='-')
axs[0].set_title('Energy Consumption of Welding Machine')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Energy Consumption')
axs[0].tick_params(axis='x', rotation=45)
axs[0].grid(True)

# Second subplot
labels = 'Idle time', 'Active time'
sizes = [int(total_idle_time), int(total_active_time)]
axs[1].pie(sizes, labels=labels, autopct='%1.1f%%', explode=(0.1, 0))
axs[1].set_title('Idle and Active Time Distribution')

# Third subplot
labels = 'Idle Energy', 'Active Energy'
sizes = [int(total_idle_consumption), int(total_active_consumption)]
total = sum(sizes)
axs[2].pie(sizes, labels=labels, autopct=lambda x: f'{x * total / 100:.1f} kWh', explode=(0.25, 0))
axs[2].set_title('Idle and Active Energy consumption Distribution')

plt.tight_layout()
plt.show()

