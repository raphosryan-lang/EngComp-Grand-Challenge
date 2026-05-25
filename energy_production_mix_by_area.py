import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import Axes

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns


def plot(axes: Axes, example_df: pd.DataFrame):
    # Hi I'm here@!@@
    pass
print('yo')
# loading # im goated
def load_power_stations() -> pd.DataFrame:
    df = pd.read_csv('data/power_stations.csv')

    # Rename X/Y to lon/lat for clarity
    df = df.rename(columns={'X': 'lon', 'Y': 'lat'})

    # Drop rows with missing coordinates
    df = df.dropna(subset=['lon', 'lat'])

    return df

# Plotting

def plot_power_station_map(ax: Axes, df: pd.DataFrame):
    ax.set_title('Australian Power Stations')

    # Set projection
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    # Zoom to Australia
    ax.set_extent([110, 155, -45, -10], crs=ccrs.PlateCarree())

    # Plot stations
    scatter = ax.scatter(
        df['lon'],
        df['lat'],
        c=df['primaryfueltype'].astype('category').cat.codes,
        s=df['generationmw'].fillna(20) / 2,  # scale bubble size
        cmap='tab20',
        alpha=0.8,
        transform=ccrs.PlateCarree()
    )

    return ax

def plot_energy_mix(ax: Axes, df: pd.DataFrame):
    mix = (
        df.groupby('primaryfueltype')['generationmw']
        .sum()
        .sort_values(ascending=False)
    )

    ax.bar(mix.index, mix.values, color='skyblue')
    ax.set_title('Australian Energy Mix (by Installed Capacity)')
    ax.set_ylabel('Total Capacity (MW)')
    ax.set_xticklabels(mix.index, rotation=45, ha='right')

    return ax

df = load_power_stations()

fig, ax = plt.subplots(figsize=(10, 8))
plot_energy_mix(ax, df)
plt.show()

fig = plt.figure(figsize=(12, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
plot_power_station_map(ax, df)
plt.show()

