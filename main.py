import pandas as pd
import geopandas as geo_pd
import rioxarray


power_stations_df = pd.read_csv("data/power_stations.csv")

power_stations_df.index = power_stations_df["objectid"]
power_stations_df.drop("objectid", axis=1, inplace=True)

power_station_points = geo_pd.points_from_xy(power_stations_df["x_coordinate"], power_stations_df["y_coordinate"])
power_stations_df.drop(["x_coordinate", "y_coordinate"], axis=1, inplace=True)

power_stations_df["operationalstatus"] = power_stations_df["operationalstatus"].astype("category")
power_stations_df["primaryfueltype"] = power_stations_df["primaryfueltype"].astype("category")

power_stations_df = geo_pd.GeoDataFrame(
    power_stations_df,
    copy=False,
    geometry=power_station_points
)

transmission_lines_df = pd.read_csv("data/transmission_lines.csv")

transmission_lines_df.index = transmission_lines_df["objectid"]
transmission_lines_df.drop("objectid", axis=1, inplace=True)

lga_df = geo_pd.read_file("data/lga/lga.shp")
lga_df["geometry"] = lga_df["geometry"].buffer(0)
lga_df = lga_df.dissolve(by="lga_name", as_index=False)

nsw_electricity_consumption = pd.read_csv("data/nsw_average_electricity_consumption_by_lga.csv")

nsw_electricity_consumption.index = nsw_electricity_consumption["Local Government Area"]
nsw_electricity_consumption.drop("Local Government Area", axis=1, inplace=True)

qld_electricity_consumption = pd.read_csv("data/qld_average_electricity_consumption_by_lga.csv")

qld_electricity_consumption.index = qld_electricity_consumption["Local Government Area"]
qld_electricity_consumption.drop("Local Government Area", axis=1, inplace=True)


#region Converting Solar and Wind GeoTIFF to GeoDataFrame
with rioxarray.open_rasterio("data/solar_power.tif") as solar_file:
    points = solar_file[0].to_pandas().stack().reset_index().dropna()
    points.columns = ["y", "x", "power"]

solar_df = geo_pd.GeoDataFrame(
    { "power": points["power"] },
    geometry=geo_pd.points_from_xy(points["x"], points["y"]),
)

with rioxarray.open_rasterio("data/wind_power_density_50m_downsampled.tif") as wind_50m_file:
    points = wind_50m_file[0].to_pandas().stack().reset_index().dropna()
    points.columns = ["y", "x", "power_density"]

wind_50m_df = geo_pd.GeoDataFrame(
    { "power_density": points["power_density"] },
    geometry=geo_pd.points_from_xy(points["x"], points["y"]),
)

with rioxarray.open_rasterio("data/wind_power_density_100m_downsampled.tif") as wind_100m_file:
    points = wind_100m_file[0].to_pandas().stack().reset_index().dropna()
    points.columns = ["y", "x", "power_density"]

wind_100m_df = geo_pd.GeoDataFrame(
    { "power_density": points["power_density"] },
    geometry=geo_pd.points_from_xy(points["x"], points["y"]),
)

with rioxarray.open_rasterio("data/wind_power_density_150m_downsampled.tif") as wind_150m_file:
    points = wind_150m_file[0].to_pandas().stack().reset_index().dropna()
    points.columns = ["y", "x", "power_density"]

wind_150m_df = geo_pd.GeoDataFrame(
    { "power_density": points["power_density"] },
    geometry=geo_pd.points_from_xy(points["x"], points["y"]),
)

with rioxarray.open_rasterio("data/wind_power_density_200m_downsampled.tif") as wind_200m_file:
    points = wind_200m_file[0].to_pandas().stack().reset_index().dropna()
    points.columns = ["y", "x", "power_density"]

wind_200m_df = geo_pd.GeoDataFrame(
    { "power_density": points["power_density"] },
    geometry=geo_pd.points_from_xy(points["x"], points["y"]),
)
#endregion


import matplotlib.pyplot as plt
import renewable_generation_vs_sources

renewable_generation_vs_sources.plot(plt.gca(), plt.gcf(), power_stations_df, solar_df, lga_df)

plt.show()
