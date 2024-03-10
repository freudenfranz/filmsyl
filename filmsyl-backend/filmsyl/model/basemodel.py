"""
Base
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
#Vectorization and similarity(linear kernel)
from sklearn.metrics.pairwise import linear_kernel

from filmsyl.data.data import get_imdb, get_netflix_example, find_titles_in_imdb
from filmsyl.netflix.netflix import clean_titles


def get_rec(amount: int, imdb_df: pd.DataFrame, netflix_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get movie get_recommendations based on a imdb_database and a netflix history
    """
    imdb_df['text_features'] = imdb_df['genres'] + ' ' + imdb_df['Director']+ ' ' + imdb_df['plot']
    #imdb_df_preprocess=imdb_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])

    joined_nf = netflix_df['title'] + ' ' + netflix_df['genres'] + ' ' + netflix_df['Director']
    netflix_df.loc[:,['text_features']] = joined_nf
    #netflix_df_preprocess=netflix_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])

    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')
    #Replace NaN with an empty string
    imdb_df['text_features'] = imdb_df['text_features'].fillna('')

    tfidf_matrix = tfidf.fit_transform(imdb_df['text_features'])

    netflix_tfidf = tfidf.transform(netflix_df['text_features'])

    #indices = pd.Series(imdb_df.index, index=imdb_df['primaryTitle']).drop_duplicates()

    cosine_sim_netflix = linear_kernel(netflix_tfidf, tfidf_matrix)

    mean_similarity = np.mean(cosine_sim_netflix, axis=0)

    imdb_df['mean_similarity'] = mean_similarity

    sorted_df = imdb_df.sort_values(by='mean_similarity', ascending=False)

    # Return the top 'amount' movie titles as a Series
    return sorted_df['primaryTitle'].head(amount)

    # Display the first [amount] IMDb recommendations


if __name__ == '__main__':
    imdb_test_df = get_imdb()
    netflix_test_df = get_netflix_example()
    cleaned_df = clean_titles(netflix_test_df['Title'])
    matched_nf = find_titles_in_imdb(cleaned_df, imdb_test_df)

    #netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    output = get_rec(5,imdb_test_df,matched_nf)
    print(output)
