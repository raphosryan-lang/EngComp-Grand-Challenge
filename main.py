import pandas as pd
import geopandas as geo_pd

power_stations_df = pd.read_csv("data/power_stations.csv")

power_stations_df.index = power_stations_df["objectid"]
power_stations_df.drop("objectid", axis=1, inplace=True)

transmission_lines_df = pd.read_csv("data/power_stations.csv")

transmission_lines_df.index = transmission_lines_df["objectid"]
transmission_lines_df.drop("objectid", axis=1, inplace=True)

lga_df = geo_pd.read_file("data/lga.shp")

nsw_electricity_consumption = pd.read_csv("data/nsw_average_electricity_consumption_by_lga.csv")

nsw_electricity_consumption.index = nsw_electricity_consumption["Local Government Area"]
nsw_electricity_consumption.drop("Local Government Area", axis=1, inplace=True)

qld_electricity_consumption = pd.read_csv("data/qld_average_electricity_consumption_by_lga.csv")

qld_electricity_consumption.index = qld_electricity_consumption["Local Government Area"]
qld_electricity_consumption.drop("Local Government Area", axis=1, inplace=True)

# Example plot
import matplotlib.pyplot as plt

lga_df["geometry"].boundary.plot()
plt.scatter(
    power_stations_df["x_coordinate"],
    power_stations_df["y_coordinate"],
    s=power_stations_df["generationmw"] / 3 + 1
)

plt.axis("equal")
plt.show()

