import matplotlib.pyplot as plt
import pandas as pd
import os

def clean_data(df):
    negative_users = df.loc[df['power'] < 0, 'userId'].unique()
    df = df[~df['userId'].isin(negative_users)]
    return df

def filter_date_range(df, start_date, end_date):
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

def plot_data(df):
    # Find the unique user IDs in the dataframe and number of users
    unique_users = df['userId'].unique()
    num_users = len(unique_users)
    print(num_users)
    print(df.isna().sum())
    print(df['power'].describe())

    # Rename the 'userId' column according to to number of users
    df['userId'] = df['userId'].replace(unique_users, range(1, num_users+1))

    # Group the data by 'userId', loop through each group and plot power consumption over time
    grouped = df.groupby('userId')
    for userId, group in grouped:
        plt.plot(group['date'], group['power'], label=userId)
    # Add a legend to the plot and show
    plt.legend()
    plt.show()

if __name__ == "__main__":
    input_dir = "/Users/kevanskorna/Desktop/smart_meter_data/output/data"
    output_dir = "/Users/kevanskorna/Desktop/smart_meter_data/output/figures"
    df = pd.read_csv(os.path.join(input_dir, 'household_profiles_output.csv'))
    df['date'] = pd.to_datetime(df['date'])

    # Load the additional information from household information.csv into a dataframe, merge on userId
    hh_info = pd.read_csv('/Users/kevanskorna/Desktop/smart_meter_data/input/household_information.csv')
    df = pd.merge(df, hh_info, on='userId', how='left')

    df = clean_data(df)
    start_date = '2017-01-1'
    end_date = '2018-01-3 23:59:59'
    df = filter_date_range(df, start_date, end_date)

    # min_square_meters = 50
    # max_square_meters = 200
    # home_type = "MULTI_FAMILY"
    # df = filter_data(df, min_square_meters, max_square_meters, home_type)

    plot_data(df)
    print('finished!')
