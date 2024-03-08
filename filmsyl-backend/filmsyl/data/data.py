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
    df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    df.dropna(inplace=True)
    nan_count = df.isna().sum().sum()
    assert nan_count == nan_count
    print("✅ data cleaned")
    return df

def find_titles_in_imdb(titles: pd.Series, imdb_df: pd.DataFrame)->pd.DataFrame:
    """
    Finds Series of titles in imdb df and returns matching subset
    """

    return imdb_df[imdb_df['primaryTitle'].isin(titles.iloc[:])]

if __name__ == '__main__':
    mock = [
    "Sex/Life: Season 1: Empire State of Mind",
    "Spider-Man",
    "The Old Guard",
    "Trevor Noah: Afraid of the Dark",
    "Trevor Noah: Son of Patricia",
    "S.W.A.T.: Season 2: Kangaroo",
    "S.W.A.T.: Season 2: Trigger Creep"]
    imdb = get_imdb()
    from filmsyl.netflix.netflix import clean_titles

    cleaned = clean_titles(pd.DataFrame(mock))
    print(cleaned)

    found = find_titles_in_imdb(cleaned, imdb)
    print(found)

{

"Title":[
  "Sniper: Ghost Shooter",
  "Spectral"
],
"Date":[
  "30/11/2023",
  "30/11/2023"
]
}
