import pandas as pd
import numpy as np
from filmsyl.settings import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from filmsyl.data.data import get_imdb, get_netflix_example

def preprocess_data(imdb_df, netflix_df):
    """
    Preprocesses IMDb and Netflix DataFrames by combining relevant columns,
    filling missing values, and creating 'text_features' column.

    Parameters:
        imdb_df (pd.DataFrame): DataFrame containing IMDb data.
        netflix_df (pd.DataFrame): DataFrame containing Netflix data.

    Returns:
        pd.DataFrame, pd.DataFrame: Preprocessed IMDb and Netflix DataFrames.
    """
    # Combine relevant columns and fill missing values for IMDb DataFrame
    imdb_df['text_features'] = imdb_df['genres'] + ' ' + imdb_df['Director'] + ' ' + imdb_df['plot']
    imdb_df['text_features'] = imdb_df['text_features'].fillna('')

    # Combine relevant columns and fill missing values for Netflix DataFrame
    netflix_df['text_features'] = netflix_df['genres'] + ' ' + netflix_df['Director']
    netflix_df['text_features'] = netflix_df['text_features'].fillna('')

    return imdb_df, netflix_df

def calculate_similarity(imdb_df, netflix_df):
    """
    Calculates similarity between IMDb and Netflix movies using TF-IDF vectorization and cosine similarity.

    Parameters:
        imdb_df (pd.DataFrame): Preprocessed IMDb DataFrame.
        netflix_df (pd.DataFrame): Preprocessed Netflix DataFrame.

    Returns:
        pd.DataFrame: IMDb DataFrame with 'mean_similarity' column added.
    """
    # Define TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Fit and transform IMDb text features
    tfidf_matrix = tfidf.fit_transform(imdb_df['text_features'])

    # Transform Netflix text features
    netflix_tfidf = tfidf.transform(netflix_df['text_features'])

    # Compute cosine similarity between Netflix and IMDb movies
    cosine_sim_netflix = linear_kernel(netflix_tfidf, tfidf_matrix)

    # Calculate mean similarity across all Netflix movies
    mean_similarity = np.mean(cosine_sim_netflix, axis=0)

    # Add 'mean_similarity' column to IMDb DataFrame
    imdb_df['mean_similarity'] = mean_similarity

    return imdb_df

def get_movie_recommendation(amount: int, imdb_df, netflix_df, new_movies):
    """
    Get movie recommendations based on IMDb and Netflix data.

    Parameters:
        amount (int): Number of movie recommendations to return.
        imdb_df (pd.DataFrame): DataFrame containing IMDb data.
        netflix_df (pd.DataFrame): DataFrame containing Netflix data.
        new_movies (pd.DataFrame): DataFrame containing new movies data.

    Returns:
        pd.Series: Series containing recommended movie titles.
    """
    # Preprocess IMDb and Netflix DataFrames
    imdb_df, netflix_df = preprocess_data(imdb_df, netflix_df)

    # Calculate similarity between IMDb and Netflix movies
    sorted_imdb_df = calculate_similarity(imdb_df, netflix_df)

    # If new_movies list is empty, recommend top movies based on mean similarity
    if new_movies.empty:
        return sorted_imdb_df.sort_values(by='mean_similarity', ascending=False)['primaryTitle'].head(amount)

    # Otherwise, recommend movies based on new_movies
    new_df = sorted_imdb_df[sorted_imdb_df['primaryTitle'].isin(new_movies['primaryTitle'])]
    rec_df = new_df.sort_values(by='mean_similarity', ascending=False)[['primaryTitle','runtimeMinutes','genres','averageRating','Director']].head(amount)

    index_dict = rec_df.to_dict(orient='index')

    return index_dict


if __name__ == "__main__":
    # Example usage
    imdb_df = get_imdb()
    netflix_df = get_netflix_example()
    new_movies = imdb_df.copy().head(10)  # Define new_movies DataFrame
    print(new_movies)
    amount = int(input("Enter the number of movies you want to be recommended: "))
    recommendations = get_movie_recommendation(amount, imdb_df, netflix_df, new_movies)
    print(recommendations)
