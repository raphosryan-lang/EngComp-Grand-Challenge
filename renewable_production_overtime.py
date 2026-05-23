import pandas as py
import numpy as np
import matplotlib.pyplot as mp

print("--- Starting our Energy Analysis Program ---")

years_list = [2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026]
hydro_data = [57.2, 42.1, 43.8, 50.4, 55.1, 57.4, 61.2, 58.9, 60.1, 62.4, 63.5]
wind_data  = [3.1,  6.8,  15.2, 24.8, 38.2, 47.9, 58.3, 81.2, 102.4, 115.8, 122.1]
solar_data = [0.8,  1.2,  3.5,  11.9, 18.4, 28.1, 42.6, 75.3, 118.7, 142.1, 158.4]

raw_data_dictionary = {
    'Year': years_list,
    'Hydro': hydro_data,
    'Wind': wind_data,
    'Solar': solar_data
}

df = py.DataFrame(raw_data_dictionary)
print("Data table created successfully!")
print(df)

print("\nCalculating totals using numpy...")
total_renewables = []

for i in range(len(df)):
    h = df['Hydro'][i]
    w = df['Wind'][i]
    s = df['Solar'][i]
    
    row_sum = np.sum([h, w, s])
    total_renewables.append(row_sum)

df['Total_Renewable_PJ'] = total_renewables

print("Updated data table with calculated totals:")
print(df)

mp.figure(figsize=(10, 6))

mp.plot(df['Year'], df['Hydro'], label='Hydro Power', color='blue', marker='o', linestyle='--')
mp.plot(df['Year'], df['Wind'], label='Wind Power', color='green', marker='s', linestyle='-.')
mp.plot(df['Year'], df['Solar'], label='Solar Power', color='orange', marker='^', linestyle=':')
mp.plot(df['Year'], df['Total_Renewable_PJ'], label='Total Renewable Energy', color='red', marker='x', linewidth=2.5)

mp.title('Evolution of Australian Renewable Energy Production (2006 - 2026)', fontsize=14, fontweight='bold')
mp.xlabel('Calendar Year', fontsize=12)
mp.ylabel('Energy Production (Petajoules - PJ)', fontsize=12)

mp.grid(True)

mp.legend(loc='upper left')

print("\nDisplaying the final trend graph...")
mp.show()

print("--- Program Finished ---")