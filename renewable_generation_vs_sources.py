from matplotlib.pylab import Axes
import matplotlib as mpl
import geopandas as geo_pd


def plot(axes: Axes, power_stations_df: geo_pd.GeoDataFrame, lga_df: geo_pd.GeoDataFrame):
    axes.axis("equal")
    
    lga_df.simplify(0.01).boundary.plot(ax=axes)

    renewable_power_stations_df = power_stations_df[power_stations_df["primaryfueltype"].isin(["Water", "Wind", "Solar", "Biogas", "Biomass"])]
    renewable_power_stations_df = renewable_power_stations_df[renewable_power_stations_df["operationalstatus"] == "Operational"]

    renewable_power_stations_df["primaryfueltype"] = renewable_power_stations_df["primaryfueltype"].cat.remove_unused_categories()

    cmap = mpl.colormaps["viridis"]

    cat_mapping = dict(enumerate(renewable_power_stations_df["primaryfueltype"].cat.categories))
    max_mapping_code = len(cat_mapping) - 1

    axes.scatter(
        renewable_power_stations_df["geometry"].x,
        renewable_power_stations_df["geometry"].y,
        c=cmap(renewable_power_stations_df["primaryfueltype"].cat.codes / max_mapping_code),
        alpha=0.7,
        edgecolor='k',
        zorder=2.5
    )

    for code, cat in cat_mapping.items():
        axes.scatter([], [], color=cmap(code / max_mapping_code), alpha=0.7, edgecolor='k', label=cat)

    axes.legend(scatterpoints=1, title='Power Stations', loc='upper left')
