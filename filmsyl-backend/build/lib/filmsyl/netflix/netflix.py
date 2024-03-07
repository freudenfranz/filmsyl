"""
Cleans a Netflix history file (.txt) retrieved from the netlix settings
from series and co. and finds all movies in the database of ours.
"""
import pandas as pd

def get_iMDb_from_json(nf: dict)->dict:
    """
    Reads a iMDb dataset from file and compares incoming user netflix history
    to it.
    """
    nf_df = pd.DataFrame(nf)
    imdb_df = pd.read_csv('data/imdb_movies.csv')
    filtered_nf = filter_series_titles(nf_df)
    matched_nf = find_and_return_matches(filtered_nf, imdb_df)
    return matched_nf


def filter_series_titles(df):
    """
    Filter the DataFrame to select rows containing series-related strings in the 'Title' column.
    Clean up (remove NaN and remove series)

    Parameters:
        df (DataFrame): The DataFrame to be filtered.

    Returns:
        DataFrame: DataFrame containing rows with non-series-related titles.
    """
    # Drop rows with missing titles
    df_cleaned = df.dropna(subset=['Title'])

    # Filter the DataFrame to select rows without series-related strings
    non_series_df = df_cleaned[~df_cleaned['Title'].str.contains(
        'Episode|Season|Seasons|Chapter|Series|Part', case=False)]

    return non_series_df


## 2. Match with iMDb DB, return enriched non_series_df (as a json) and percentage of matches

def find_and_return_matches(non_series_df, imdb_df):
    """
    Find matches between non_series_df and df based on their titles and return the results as JSON.

    Parameters:
        non_series_df (DataFrame): DataFrame containing non-series-related titles.
        imdb_df (DataFrame): DataFrame containing titles to search for matches.

    Returns:
        dict: A dictionary containing the percentage of matches and information about the matched rows.
    """
    # Count the number of films in non_series_df
    total_non_series_films = len(non_series_df)

    # Find matches between non_series_df and df based on the 'Title' column
    matches = non_series_df['Title'].isin(imdb_df['Title'])

    # Count the number of matches
    matched_films = matches.sum()

    # Calculate the percentage of films with a match
    percentage_matched = (matched_films / total_non_series_films) * 100

    # Select rows of df for which a match was found
    matched_rows_df = imdb_df[imdb_df['Title'].isin(non_series_df.loc[matches, 'Title'])]

    # Convert matched rows DataFrame to JSON
    matched_rows_json = matched_rows_df.to_dict(orient='records')

    # Create a dictionary containing the percentage of matches and information about the matched rows
    results = {
        'percentage_matched': percentage_matched,
        'matched_rows': matched_rows_json
    }

    return results

# Example usage:
# results = find_and_return_matches(non_series_df, imdb_df)
# print(results)

if __name__ == '__main__':
    print('hello world')
