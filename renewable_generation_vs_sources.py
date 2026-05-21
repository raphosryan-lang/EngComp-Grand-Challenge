from matplotlib.pylab import Axes, Figure
import matplotlib as mpl
import geopandas as geo_pd


def plot(axes: Axes, fig: Figure, power_stations_df: geo_pd.GeoDataFrame, solar_df: geo_pd.GeoDataFrame, lga_df: geo_pd.GeoDataFrame):
    axes.axis("equal")
    
    lga_df.simplify(0.01).boundary.plot(ax=axes)

    renewable_power_stations_df = power_stations_df[power_stations_df["primaryfueltype"].isin(["Water", "Wind", "Solar", "Biogas", "Biomass"])]
    renewable_power_stations_df = renewable_power_stations_df[renewable_power_stations_df["operationalstatus"] == "Operational"]

    renewable_power_stations_df["primaryfueltype"] = renewable_power_stations_df["primaryfueltype"].cat.remove_unused_categories()

    # renewable_power_stations_df = renewable_power_stations_df[renewable_power_stations_df["primaryfueltype"] == "Solar"]

    code_cat_mapping = dict(enumerate(renewable_power_stations_df["primaryfueltype"].cat.categories))
    
    cmap = mpl.colormaps["tab10"]
    # Tab 10 has 10 different colours, so we map one code to each
    # (and ignore some colours if there aren't enough codes)
    code_dilation_factor = 10

    axes.scatter(
        renewable_power_stations_df["geometry"].x,
        renewable_power_stations_df["geometry"].y,
        c=cmap(renewable_power_stations_df["primaryfueltype"].cat.codes / code_dilation_factor),
        edgecolor='k',
        zorder=2.5
    )

    for code, cat in code_cat_mapping.items():
        axes.scatter([], [], color=cmap(code / code_dilation_factor), edgecolor='k', label=cat)

    axes.legend(scatterpoints=1, title='Power Stations', loc='upper left')

    solar_exploded_df = solar_df.explode(index_parts=False)
    x = solar_exploded_df.geometry.x
    y = solar_exploded_df.geometry.y
    solar_power = solar_exploded_df["power"]

    # gridsize controls the resolution of the heatmap
    hb = axes.hexbin(
        x, y,
        C=solar_power,
        gridsize=120,
        cmap="inferno"
    )

    fig.colorbar(hb, label='Mean Solar Irradiation')
    axes.set_title('Australia Solar Irradiation Heatmap (Hexbin)')
    axes.axis("equal")
