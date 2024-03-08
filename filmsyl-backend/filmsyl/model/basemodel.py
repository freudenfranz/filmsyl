"""
Base
"""

from filmsyl.data.data import get_imdb, get_netflix_example
from filmsyl.settings import *
import os
import pandas as pd
#Vectorization and similarity(linear kernel)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_rec(amount: int, imdb_df: pd.DataFrame, netflix_df: pd.DataFrame) -> TfidfVectorizer:
    """
    Get movie get_recommendations based on a imdb_database and a netflix history
    """
    imdb_df['text_features']= imdb_df['genres'] + ' ' + imdb_df['Director']+ ' ' + imdb_df['plot']
    imdb_df_preprocess=imdb_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])


    netflix_df['text_features'] = netflix_df['title'] + ' ' + netflix_df['genres'] + ' ' + netflix_df['Director']
    netflix_df_preprocess=netflix_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])

    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')
    #Replace NaN with an empty string
    imdb_df['text_features'] = imdb_df['text_features'].fillna('')

    tfidf_matrix = tfidf.fit_transform(imdb_df['text_features'])

    netflix_tfidf = tfidf.transform(netflix_df['text_features'])

    indices = pd.Series(imdb_df.index, index=imdb_df['primaryTitle']).drop_duplicates()

    cosine_sim_netflix = linear_kernel(netflix_tfidf, tfidf_matrix)

    mean_similarity = np.mean(cosine_sim_netflix, axis=0)

    imdb_df['mean_similarity'] = mean_similarity

    sorted_df = imdb_df.sort_values(by='mean_similarity', ascending=False)

    # Return the top 'amount' movie titles as a Series
    return sorted_df['primaryTitle'].head(amount)

    # Display the first [amount] IMDb recommendations


if __name__ == '__main__':
    imdb_df = get_imdb()
    netflix_df = get_netflix_example()

    #netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    output = get_rec(5,imdb_df,netflix_df)
    print(output)
