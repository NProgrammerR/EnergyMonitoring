import json

# Assuming your JSON data is stored in a file named 'electricity_data.json'
with open('stopcua.json', 'r') as file:
    data = json.load(file)

# Extracting data from the JSON structure
machine_data = data[0]['stOPCUA']['stMachineData']
vision_data = data[0]['stOPCUA']['stVisionData']
time_variables_hourly = data[0]['stOPCUA']['stTimeVariablesHourly']

# Now you can access each variable separately

# Extracting data for welding energy consumption and welding time
welding_energy_consumption = machine_data['arrfWeldingEnergyConsumption']
welding_time = time_variables_hourly['arrtRobotWeldingTime'][0]

# Calculate the total energy consumption for welding per hour
total_welding_energy_per_hour = [(hour + 1, sum(welding_energy_consumption[i:i+1])) for hour, i in enumerate(range(len(welding_time)))]

# Now 'total_welding_energy_per_hour' contains the total welding energy consumption for each hour

print("Welding_energy_consuption: ",welding_energy_consumption)
print("Welding_time: ", welding_time)
print("total_welding_energy_per_hour: ", total_welding_energy_per_hour)