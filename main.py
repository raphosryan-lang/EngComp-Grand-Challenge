import pandas as pd

power_stations_df = pd.read_csv("data/power_stations.csv")

power_stations_df.index = power_stations_df["objectid"]
power_stations_df.drop("objectid", axis=1, inplace=True)

transmission_lines_df = pd.read_csv("data/power_stations.csv")

transmission_lines_df.index = transmission_lines_df["objectid"]
transmission_lines_df.drop("objectid", axis=1, inplace=True)
