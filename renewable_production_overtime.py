import pandas as pd
from matplotlib.pylab import Axes

def plot(axes: Axes, renewable_energy_over_time_df: pd.DataFrame):
    axes.stackplot(renewable_energy_over_time_df.index, renewable_energy_over_time_df.T, labels=renewable_energy_over_time_df.columns)

    axes.set_title('Evolution of Australian Renewable Energy Production (2006 - 2026)', fontsize=14, fontweight='bold')
    axes.set_xlabel('Calendar Year', fontsize=12)
    axes.set_ylabel('Energy Production (PJ)', fontsize=12)

    axes.legend(loc='upper left')
