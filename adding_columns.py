import pandas as pd
import os

# Set the input and output directories
input_dir = "/Users/kevanskorna/Desktop/smart_meter_data/input"
output_dir = "/Users/kevanskorna/Desktop/smart_meter_data/output/data"

for filename in os.listdir(input_dir):
    if filename.endswith('_profiles.csv'):
        df = pd.read_csv(os.path.join(input_dir, filename))
        # Convert the 'timestamp' column to a datetime index
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        # Add the additional columns
        df['unit'] = 'watts'
        df['hour_of_the_day'] = df.index.hour
        df['weekday'] = df.index.weekday
        df['day_of_the_year'] = df.index.dayofyear
        df['hour_of_the_year'] = df.index.dayofyear * 24 + df.index.hour
        # Convert the power units to watts
        columns_to_divide = ['power', 'power1', 'power2', 'power3']
        df[columns_to_divide] = df[columns_to_divide].div(1000)
        df.info()

        # Save the output data to a CSV file
        df.to_csv(os.path.join(output_dir,'household_profiles_output.csv'))
        # df.head(1000).to_csv(os.path.join(output_dir,'household_profiles_output_1000.csv'))

print("Finished!")


