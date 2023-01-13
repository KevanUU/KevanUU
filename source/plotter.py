from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
import pandas as pd

from utils.io import read_csv, save_csv

if TYPE_CHECKING:
    from utils.config import Config


class Plotter:

    def __init__(self, cfg: "Config"):
        self.cfg = cfg

    @staticmethod
    def filter_date_range(df: pd.DataFrame, start_date: str, end_date: str):
        mask = (df['date'] > start_date) & (df['date'] <= end_date)
        df = df.loc[mask]
        return df

    # # I tried to include a filter function for square meters and home type, but it is still incomplete as it does not
    # # include all the other attributes we need in order to filter out households (aircon, solar pv, heatpump)
    # def filter_data(df, min_square_meters, max_square_meters, home_type):
    #     mask = (df['squareMeters'] >= min_square_meters) & (df['squareMeters'] <= max_square_meters) & (df['homeType']
    #                                                                                                     == home_type)
    #     df = df[mask]
    #     return df

    def plot_data(self, df):
        # Find the unique user IDs in the dataframe and number of users
        unique_users = df['userId'].unique()
        num_users = len(unique_users)
        print(num_users)
        print(df.isna().sum())
        print(df['power'].describe())

        # Rename the 'userId' column according to to number of users
        df['userId'] = df['userId'].replace(unique_users, range(1, num_users + 1))

        # Group the data by 'userId', loop through each group and plot power consumption over time
        grouped = df.groupby('userId')
        for userId, group in grouped:
            plt.plot(group['date'], group['power'], label=userId)
        # Add a legend to the plot and show
        plt.legend()
        plt.show()

