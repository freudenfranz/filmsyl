"""
Cleans a Netflix history file (.txt) retrieved from the netlix settings
from series and co. and finds all movies in the database of ours.
"""
import pandas as pd
from filmsyl.data.data import get_imdb, find_titles_in_imdb

def get_nf_imdb_matches(nf: dict)->dict:

    """
    Reads a iMDb dataset from file and compares incoming user netflix history
    to it.
    """
    imdb_df = get_imdb()

    nf_df = pd.DataFrame(nf)

    cleaned_df = clean_titles(nf_df['Title'])

    matched_nf = find_and_return_matches(cleaned_df, imdb_df)

    return matched_nf

def get_user_stats(non_series_df, matches: pd.DataFrame):
     # Count the number of films in non_series_df
    total_non_series_films = len(non_series_df)
    # Count the number of matches
    matched_films = len(matches)

    # Calculate the percentage of films with a match

    percentage_matched = (matched_films / total_non_series_films) * 100
    stats = {
        "size_cleaned": total_non_series_films,
        "matched_films": matched_films,
        "percentage_matched": percentage_matched
    }

    return stats

def clean_titles(dirty_df: pd.Series)->pd.DataFrame:
    """
    Filter the DataFrame to select rows containing series-related strings in the 'Title' column.
    Clean up (remove NaN and remove series)

    Parameters:
        dirty_df (Series): The Titles to be filtered.

    Returns:
        DataFrame: Non-series-related titles.
    """
    print(dirty_df.shape)
    # Drop rows with missing titles
    df_cleaned = dirty_df.dropna()

    # Filter the DataFrame to select rows without series-related strings

    non_series_df = df_cleaned[~df_cleaned.iloc[:].str.contains(
                                'Episode|Season|Seasons|Chapter|Series|Part',
                                case=False
                            )]

    print("✅ removed series of dataframe")
    return non_series_df


def find_and_return_matches(non_series_df: pd.Series, imdb_df):
    """
    Match with iMDb DB, return enriched non_series_df (as a json) and percentage of matches
    Find matches between non_series_df and df based on their titles and return the results as JSON.

    Parameters:
        non_series_df (DataFrame): DataFrame containing non-series-related titles.
        imdb_df (DataFrame): DataFrame containing titles to search for matches.

    Returns:
        dict: A dictionary containing the percentage of matches and information about the matched rows.
    """

    # Find matches between non_series_df and df based on the 'Title' column
    matches = find_titles_in_imdb(non_series_df, imdb_df=imdb_df)

    # Select rows of df for which a match was found
    matched_rows_df = find_titles_in_imdb(non_series_df, imdb_df)
    #matched_rows_df = imdb_df[imdb_df['primaryTitle'].isin(non_series_df.loc[matches, 'Title'])]

    # Convert matched rows DataFrame to JSON

    matched_rows_json = matched_rows_df.to_dict(orient='records')

    user_stats =  get_user_stats(non_series_df=non_series_df, matches=matches)

    # Create a dictionary containing the percentage of matches and information about the matched rows
    results = {
        'statistics': user_stats,
        'matched_rows': matched_rows_json
    }

    print("✅ matched nf and imdb")
    return results

if __name__ == '__main__':
    from filmsyl.data.data import read_imdb_csv
    netflix = pd.read_csv('./filmsyl/raw_data/NetflixViewingHistory.csv')
    imdb = get_imdb()
    breakpoint()
    cleaned = clean_titles(pd.DataFrame(netflix)['Title'])
    found = find_titles_in_imdb(cleaned, imdb)
    print(found)
