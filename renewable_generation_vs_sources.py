from matplotlib.pylab import Axes, Figure
import matplotlib as mpl
import geopandas as geo_pd


def plot(
    solar_axes: Axes,
    wind_axes: Axes,
    power_stations_df: geo_pd.GeoDataFrame,
    solar_df: geo_pd.GeoDataFrame,
    wind_50m_df: geo_pd.GeoDataFrame,
    wind_100m_df: geo_pd.GeoDataFrame,
    wind_150m_df: geo_pd.GeoDataFrame,
    wind_200m_df: geo_pd.GeoDataFrame,
    lga_df: geo_pd.GeoDataFrame,
):
    simp_lga = lga_df.simplify(0.01).boundary

    renewable_power_stations_df = power_stations_df[
        power_stations_df["primaryfueltype"].isin(
            ["Water", "Wind", "Solar", "Biogas", "Biomass"]
        )
    ]

    renewable_power_stations_df = renewable_power_stations_df[
        renewable_power_stations_df["operationalstatus"] == "Operational"
    ]

    renewable_power_stations_df["primaryfueltype"] = renewable_power_stations_df[
        "primaryfueltype"
    ].cat.remove_unused_categories()

    wind_df = (
        wind_50m_df.sjoin_nearest(wind_100m_df).drop("index_right", axis=1)
        .sjoin_nearest(wind_150m_df).drop("index_right", axis=1)
        .sjoin_nearest(wind_200m_df).drop("index_right", axis=1)
    )

    plot_solar(solar_axes, renewable_power_stations_df, solar_df, simp_lga)
    plot_wind(wind_axes, renewable_power_stations_df, wind_df, simp_lga)


def plot_solar(
    axes: Axes,
    renewable_power_stations_df: geo_pd.GeoDataFrame,
    solar_df: geo_pd.GeoDataFrame,
    simp_lga: geo_pd.GeoSeries,
):
    simp_lga.plot(ax=axes)

    solar_power_stations_df = renewable_power_stations_df[
        renewable_power_stations_df["primaryfueltype"] == "Solar"
    ]

    code_cat_mapping = dict(
        enumerate(renewable_power_stations_df["primaryfueltype"].cat.categories)
    )

    cmap = mpl.colormaps["tab10"]
    # Tab 10 has 10 different colours, so we map one code to each
    # (and ignore some colours if there aren't enough codes)
    code_dilation_factor = 10

    axes.scatter(
        solar_power_stations_df["geometry"].x,
        solar_power_stations_df["geometry"].y,
        c=cmap(
            solar_power_stations_df["primaryfueltype"].cat.codes / code_dilation_factor
        ),
        edgecolor="k",
        zorder=2.5,
    )

    for code, cat in code_cat_mapping.items():
        axes.scatter(
            [], [], color=cmap(code / code_dilation_factor), edgecolor="k", label=cat
        )

    axes.legend(scatterpoints=1, title="Power Stations", loc="upper left")

    solar_exploded_df = solar_df.explode(index_parts=False)
    x = solar_exploded_df.geometry.x
    y = solar_exploded_df.geometry.y
    solar_power = solar_exploded_df["power"]

    # gridsize controls the resolution of the heatmap
    hb = axes.hexbin(x, y, C=solar_power, gridsize=120, cmap="inferno")

    axes.figure.colorbar(hb, label="Mean Solar Irradiation")
    axes.set_title("Australia Solar Irradiation Heatmap (Hexbin)")
    axes.axis("equal")


def plot_wind(
    axes: Axes,
    renewable_power_stations_df: geo_pd.GeoDataFrame,
    wind_df: geo_pd.GeoDataFrame,
    simp_lga: geo_pd.GeoSeries,
):
    simp_lga.plot(ax=axes)

    wind_power_stations_df = renewable_power_stations_df[
        renewable_power_stations_df["primaryfueltype"] == "Wind"
    ]

    code_cat_mapping = dict(
        enumerate(renewable_power_stations_df["primaryfueltype"].cat.categories)
    )

    cmap = mpl.colormaps["tab10"]
    # Tab 10 has 10 different colours, so we map one code to each
    # (and ignore some colours if there aren't enough codes)
    code_dilation_factor = 10

    axes.scatter(
        wind_power_stations_df["geometry"].x,
        wind_power_stations_df["geometry"].y,
        c=cmap(
            wind_power_stations_df["primaryfueltype"].cat.codes / code_dilation_factor
        ),
        edgecolor="k",
        zorder=2.5,
    )

    for code, cat in code_cat_mapping.items():
        axes.scatter(
            [], [], color=cmap(code / code_dilation_factor), edgecolor="k", label=cat
        )

    axes.legend(scatterpoints=1, title="Power Stations", loc="upper left")

    wind_exploded_df = wind_df.explode(index_parts=False)
    x = wind_exploded_df.geometry.x
    y = wind_exploded_df.geometry.y
    solar_power = wind_exploded_df["50m_power_density"]

    # gridsize controls the resolution of the heatmap
    hb = axes.hexbin(x, y, C=solar_power, gridsize=120, cmap="inferno")

    axes.figure.colorbar(hb, label="Max. Wind Power Density (W/m^2)")
    axes.set_title("Australia Wind Power Density Heatmap (Hexbin)")
    axes.axis("equal")
