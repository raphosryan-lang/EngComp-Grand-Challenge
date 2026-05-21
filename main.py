import pandas as pd
import geopandas as geo_pd
import rioxarray
from rasterio.enums import Resampling


power_stations_df = pd.read_csv("data/power_stations.csv")

power_stations_df.index = power_stations_df["objectid"]
power_stations_df.drop("objectid", axis=1, inplace=True)

power_stations_df["geometry"] = geo_pd.points_from_xy(power_stations_df["x_coordinate"], power_stations_df["y_coordinate"])
power_stations_df.drop(["x_coordinate", "y_coordinate"], axis=1, inplace=True)

power_stations_df["operationalstatus"] = power_stations_df["operationalstatus"].astype("category")
power_stations_df["primaryfueltype"] = power_stations_df["primaryfueltype"].astype("category")

power_stations_df = geo_pd.GeoDataFrame(power_stations_df)

transmission_lines_df = pd.read_csv("data/power_stations.csv")

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

# with rioxarray.open_rasterio("data/wind_power_density_50m_4.tif") as wind_file:
#     wind_file = wind_file.rio.write_crs("WGS 84")

#     wind_file = wind_file.rio.reproject(
#         wind_file.rio.crs,
#         shape=(wind_file.rio.width // 8, wind_file.rio.height // 8),
#         resampling=Resampling.bilinear
#     )

#     points = wind_file[0].to_pandas().stack().reset_index().dropna()
#     points.columns = ["y", "x", "power_density"]

#     wind_df = geo_pd.GeoDataFrame(
#         { "power_density": points["power_density"] },
#         geometry=geo_pd.points_from_xy(points["x"] / 100, -points["y"] / 100),
#     )


# Example plot
import matplotlib.pyplot as plt
import renewable_generation_vs_sources

# wind_df.plot(column="power_density", ax=plt.gca())
# lga_df.boundary.plot(color="red", ax=plt.gca())
# plt.show()

renewable_generation_vs_sources.plot(plt.gca(), power_stations_df, lga_df)

plt.show()
