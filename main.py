import pandas as pd

# Read the input data
input_data = pd.read_csv('input_file.csv')

# Add a new column 'Weights' to the dataset
input_data['Weights'] = input_data['Forecast'] / input_data['Capacity']

# Define the zone forecasts and total state forecast
zone_forecasts = {
    'E': 2800,
    'N': 1500,
    'W': 2000,
    'S': 6500,
}

total_state_forecast = 12000

# Calculate the total regional/zonal forecasts
total_regional_forecast = sum(zone_forecasts.values())

# Calculate zonal weights
zone_weights = {}
for zone in zone_forecasts.keys():
    zone_weights[zone] = input_data[input_data['Plant_Name'].str.startswith(zone)]['Weights'].sum()

# Calculating total state weight
total_state_weight = sum(zone_weights.values())

# Calculating revised forecast for each zone
zone_forecasts_revised = {zone: (zone_weight / total_state_weight) * total_state_forecast for zone, zone_weight in zone_weights.items()}

# Redistribute the power output for each wind farm
def redistribute_forecast(row):
    zone = row['Plant_Name'][0]
    return row['Weights'] / zone_weights[zone] * zone_forecasts_revised[zone]

input_data['Redistributed_Forecast'] = input_data.apply(redistribute_forecast, axis=1)

# Round the redistributed forecast to one decimal place
input_data['Redistributed_Forecast'] = input_data['Redistributed_Forecast'].round(3)

# Check if redistributed forecast exceeds capacity for any wind farm
if any(input_data['Redistributed_Forecast'] > input_data['Capacity']):
    print('There is no feasible solution for this problem because some wind farms have re-dispatched forecast exceeding their capacity.')

# Format the output to the desired form
output_data = input_data[['Plant_Name', 'Redistributed_Forecast']].apply(lambda x: f"{x['Plant_Name']},{x['Redistributed_Forecast']}", axis=1)

# Output the redistributed values
print(input_data[['Plant_Name', 'Redistributed_Forecast']].to_csv(index=False))
