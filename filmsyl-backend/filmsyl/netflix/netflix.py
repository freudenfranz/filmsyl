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


def get_user_stats(df):
    genres_count_dict = {}
    directors_count_dict = {}
    total_films_count = len(df)

    # Filling Na just in case
    df['Director'] = df['Director'].fillna('')
    df['genres'] = df['genres'].fillna('')

    # Count genre occurrences
    for genres_str in df['genres']:
        genres_list = genres_str.split(',')

        for genre in genres_list:
            genre = genre.strip()
            genres_count_dict[genre] = genres_count_dict.get(genre, 0) + 1

    # Count director occurrences
    for director_str in df['Director']:
        directors_list = director_str.split(',')

        for director in directors_list:
            director = director.strip()
            directors_count_dict[director] = directors_count_dict.get(director, 0) + 1

    # Sort genre counts in descending order of frequency
    genres_count_dict = dict(sorted(genres_count_dict.items(), key=lambda item: item[1], reverse=True))

    # Sort director counts in descending order of frequency
    directors_count_dict = dict(sorted(directors_count_dict.items(), key=lambda item: item[1], reverse=True))

    stats = {
        'total_films_count': total_films_count,
        'genres_count': genres_count_dict,
        'directors_count': directors_count_dict
    }

    return stats


def clean_titles(dirty_series: pd.Series)->pd.DataFrame:
    """
    Filter the DataFrame to select rows containing series-related strings in the 'Title' column.
    Clean up (remove NaN and remove series)

    Parameters:
        dirty_series (Series): The Titles to be filtered.

    Returns:
        DataFrame: Non-series-related titles.
    """
    # Drop rows with missing titles
    df_cleaned = dirty_series.dropna()

    # Filter the DataFrame to select rows without series-related strings
    non_series_df = df_cleaned[~df_cleaned.str.contains(
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

    user_stats =  get_user_stats(non_series_df=non_series_df)

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

    cleaned = clean_titles(netflix['Title'])
    found = find_titles_in_imdb(cleaned, imdb)
    print(found)
