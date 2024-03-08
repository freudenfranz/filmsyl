"""
Todo
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from filmsyl.data.data import get_imdb
from filmsyl.netflix.netflix import get_nf_imdb_matches


def join_text_features(imdb_df: pd.DataFrame) -> pd.DataFrame:
    """combine imdb text features."""
    imdb_df['text_features']= imdb_df['genres'] + ' ' + imdb_df['title'] + ' ' + imdb_df['Director']
    #nan_count = imdb_df['text_features'].isna().sum()
    #print(f"LOG: Nan count int text features: {nan_count}")
    return imdb_df

def get_rec(amount: int, imdb_df: pd.DataFrame, netflix_df: pd.DataFrame) -> CountVectorizer:
    """
    Get movie get_recommendations based on a imdb_database and a netflix history
    """
    # Initialize CountVectorizer
    vectorizer = CountVectorizer()
    # Fit and transform the text data for IMDb
    imdb_text_matrix = vectorizer.fit_transform(imdb_df['text_features'])
    # Transform the text data for Netflix
    netflix_text_matrix = vectorizer.transform(netflix_df['text_features'])

    knn_model = NearestNeighbors(n_neighbors=4, metric='cosine')
    knn_model.fit(imdb_text_matrix)

    # Find nearest neighbors for Netflix data
    distances, indices = knn_model.kneighbors(netflix_text_matrix)

    imdb_recommendations = []  # Initialize an empty list to store IMDb recommendations

    # Loop through each row in the DataFrame netflix_df
    for i in range(len(netflix_df)):
        second_nearest_neighbor_index = indices[i][1]  # Get the index of the second closest neighbor for the current row
        imdb_title = imdb_df.iloc[second_nearest_neighbor_index]['title']  # Retrieve the title from the IMDb DataFrame using the second nearest neighbor index
        netflix_title = netflix_df.iloc[i]['title']  # Retrieve the title of the Netflix movie
        imdb_recommendations.append((netflix_title, imdb_title))  # Append a tuple of Netflix title and IMDb recommendation

    # Display the first [amount] IMDb recommendations
    for netflix_title, imdb_title in imdb_recommendations[:amount]:
        print(f"We recommend '{imdb_title}'")
    #TODO
    return imdb_df[:amount]
    return imdb_recommendations[:amount]

if __name__ == '__main__':
    imdb_df = get_imdb()
    csv_ = os.path.join("filmsyl/raw_data", "NetflixViewingHistory.csv")
    netflix_df = pd.read_csv(csv_)
    #netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    nf_df = get_nf_imdb_matches(netflix_df)
    print(nf_df)
