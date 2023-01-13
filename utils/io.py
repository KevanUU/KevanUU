import pandas as pd
import os


def read_csv(dir_path, file_name):
    df = pd.read_csv(os.path.join(dir_path, f"{file_name}.csv"))
    return df


def save_csv(df: pd.DataFrame, dir_path: str, file_name: str):
    df.to_csv(os.path.join(dir_path, f"{file_name}.csv"))

