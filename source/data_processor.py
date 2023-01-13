from typing import TYPE_CHECKING

import pandas as pd

from utils.io import read_csv, save_csv

if TYPE_CHECKING:
    from utils.config import Config


class DataProcessor:

    def __init__(self, cfg: "Config"):
        self.cfg = cfg
        self.household_profiles = self.read_household_profiles(cfg)
        self.household_info = self.read_household_info(cfg)

    @staticmethod
    def read_household_profiles(cfg: "Config"):
        household_profiles = read_csv(cfg.input_data, "household_profiles")
        household_profiles['date'] = pd.to_datetime(household_profiles['date'])
        household_profiles.set_index('date', inplace=True)
        return household_profiles

    @staticmethod
    def read_household_info(cfg: "Config"):
        household_info = read_csv(cfg.input_data, "household_information")
        household_info.set_index('userId', inplace=True)
        return household_info

    def add_date_columns_to_household_profiles(self):
        # Add the additional columns
        self.household_profiles['unit'] = 'watts'
        self.household_profiles['hour_of_day'] = self.household_profiles.index.hour + 1
        self.household_profiles['weekday'] = self.household_profiles.index.weekday + 1
        self.household_profiles['day_of_year'] = self.household_profiles.index.dayofyear
        self.household_profiles['hour_of_year'] = self.household_profiles.index.dayofyear * 24 + \
                                                  self.household_profiles.index.hour + 1
        # Convert the power units to watts
        columns_to_divide = ['power', 'power1', 'power2', 'power3']
        self.household_profiles[columns_to_divide] = self.household_profiles[columns_to_divide].div(1000)

    def filter_households(self):
        selected_households = []
        not_exist_households = []
        print(len(self.household_profiles["userId"].unique()))
        for household_id in self.household_profiles["userId"].unique():
            home_type = self.get_household_param(household_id, "homeType")
            if home_type == "not_exist":
                not_exist_households.append(household_id)
        print(len(not_exist_households))

    @staticmethod
    def condition_pv(df):
        negative_users = df.loc[df['power'] < 0, 'userId'].unique()
        df = df[~df['userId'].isin(negative_users)]
        return df

    def get_household_param(self, household_id: str, param_name: str):
        try:
            return self.household_info.at[household_id, param_name]
        except KeyError:
            print(f'household_id does not exist: {household_id}')
            return "not_exist"

    def save_household_profiles(self):
        # save_csv(self.household_profiles, self.cfg.output_data, 'household_profiles')
        save_csv(self.household_profiles.head(1000), self.cfg.output_data, 'household_profiles')

    def main(self):
        self.add_date_columns_to_household_profiles()
        self.filter_households()
        self.save_household_profiles()
