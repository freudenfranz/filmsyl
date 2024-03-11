"""
Base
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from filmsyl.netflix.netflix import clean_titles

def preprocess_data(df):
    df['text_features'] = df['genres'] + ' ' + df['Director'] + ' ' + df['plot']
    df['text_features'] = df['text_features'].fillna('')
    return df

def calculate_similarity(imdb_df, netflix_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(imdb_df['text_features'])
    netflix_tfidf = tfidf.transform(netflix_df['text_features'])
    cosine_sim_netflix = linear_kernel(netflix_tfidf, tfidf_matrix)
    mean_similarity = np.mean(cosine_sim_netflix, axis=0)
    imdb_df['mean_similarity'] = mean_similarity
    return imdb_df

def get_rec(amount: int, imdb_df: pd.DataFrame, netflix_df: pd.DataFrame, new_movies: pd.DataFrame) -> pd.DataFrame:
    imdb_df = preprocess_data(imdb_df)
    netflix_df['text_features'] = netflix_df['title'] + ' ' + netflix_df['genres'] + ' ' + netflix_df['Director']

    if new_movies.empty:
        # Filter IMDb movies that are not in Netflix list to give a reccomendation the user can watch
        not_in_netflix = imdb_df[~imdb_df['primaryTitle'].isin(netflix_df['title'])]
        return not_in_netflix.sort_values(by='mean_similarity', ascending=False)['primaryTitle'].head(amount)

    #return a sorted list of new sorted recomendation
    new_df = imdb_df[imdb_df['primaryTitle'].isin(new_movies['title'])]

    return new_df.sort_values(by='mean_similarity', ascending=False)['primaryTitle'].head(amount)

if __name__ == '__main__':
    imdb_test_df = get_imdb()
    netflix_test_df = get_netflix_example()
    cleaned_df = clean_titles(netflix_test_df['Title'])
    matched_nf = find_titles_in_imdb(cleaned_df, imdb_test_df)
     #netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
    output = get_rec(5,imdb_test_df,matched_nf)
    print(output)
