"""
    Handles reading and writing the imdb csv/data, and cleaning the dataset
"""

import os
import pandas as pd
import settings

def get_imdb(path: str=settings.IMDB_PATH,
                filename: str=settings.IMDB_FILNAME) -> pd.DataFrame:
    """
    Read imdb csv and returns a clean pandas df
    """
    imdb_db = read_imdb_csv(path, filename)
    cleaned_imdb_db = clean_data(imdb_db)
    return cleaned_imdb_db

def read_imdb_csv(path: str, filename: str)->pd.DataFrame:
    """
    Import IMDb movie csv
    """
    csv = os.path.join(path, filename)
    imdb_df = pd.read_csv(csv)
    return imdb_df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by
    - assigning correct dtypes to each column
    - removing buggy or irrelevant transactions
    """
    # Compress raw_data by setting types to DTYPES_RAW
    df = df.astype(DTYPES_RAW)

    # Remove buggy transactions
    df = df.drop_duplicates()  # TODO: handle whether data is consumed in chunks directly in the data source
    df = df.dropna(how='any', axis=0)

    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0) |
                    (df.pickup_latitude != 0) | (df.pickup_longitude != 0)]

    df = df[df.passenger_count > 0]
    df = df[df.fare_amount > 0]

    # Remove geographically irrelevant transactions (rows)
    df = df[df.fare_amount < 400]
    df = df[df.passenger_count < 8]

    df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
    df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
    df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]

    print("✅ data cleaned")

    return df
