import geopandas as geo_pd
import matplotlib as mpl
import numpy as np

from matplotlib.pylab import Axes


def plot(axes: Axes, power_stations_df: geo_pd.GeoDataFrame, lga_df: geo_pd.GeoDataFrame):
    axes.set_title('Australian Power Stations')

    lga_df.simplify(0.01).boundary.plot(ax=axes)

    cmap = mpl.colormaps["tab20"]
    # Tab 20 has 20 different colours, so we map one code to each
    # (and ignore some colours if there aren't enough codes)
    code_dilation_factor = 20

    generation_dilation_factor = 30

    # Plot stations
    axes.scatter(
        power_stations_df.geometry.x,
        power_stations_df.geometry.y,
        c=power_stations_df['primaryfueltype'].cat.codes,
        s=power_stations_df['generationmw'] / generation_dilation_factor,  # scale bubble size
        cmap=cmap,
        alpha=0.8,
        zorder=2.5
    )

    code_cat_mapping = dict(
        enumerate(power_stations_df["primaryfueltype"].cat.categories)
    )

    for code, cat in code_cat_mapping.items():
        axes.scatter(
            [], [], color=cmap(code / code_dilation_factor), edgecolor="k", label=cat
        )

    for generation in np.linspace(500, 5000, 5):
        axes.scatter(
            [], [], color=cmap(0), edgecolor="k", s=generation / generation_dilation_factor, label=f"{generation} MW"
        )

    axes.legend(scatterpoints=1, title="Power Stations", loc="upper left")
