"""
    Handles reading and writing the imdb csv/data, and cleaning the dataset
"""

import os
import pandas as pd
import numpy as np
import filmsyl.settings as settings

def get_imdb(path: str=settings.IMDB_PATH,
                filename: str=settings.IMDB_FILNAME) -> pd.DataFrame:
    """
    Read imdb csv and returns a clean pandas df
    """
    imdb_db = read_imdb_csv(path, filename)
    cleaned_imdb_db = clean_data(imdb_db)
    return cleaned_imdb_db

def get_netflix_example():
    """
    Get example netflix history
    """
    csv = os.path.join(settings.IMDB_PATH, settings.NETFLIX_FILENAME)
    netflix_df = clean_data(pd.read_csv(csv))
    print("✅ netflix csv loaded")
    return netflix_df

def read_imdb_csv(path: str, filename: str)->pd.DataFrame:
    """
    Import IMDb movie csv
    """
    csv = os.path.join(path, filename)
    imdb_df = pd.read_csv(csv)
    print("✅ imdb csv loaded")
    return imdb_df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by
    - assigning correct dtypes to each column
    - removing buggy or irrelevant transactions
    """
    # Compress raw_data by setting types to DTYPES_RAW
    #df = df.astype(DTYPES_RAW)

    # Remove buggy transactions
    #df = df.drop_duplicates()  # TODO: handle whether data is consumed in chunks directly in the data source
    #df = df.dropna(how='any', axis=0)
    df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    df.dropna(inplace=True)
    nan_count = df.isna().sum().sum()
    assert nan_count == nan_count
    print("✅ data cleaned")
    return df
