import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
#import IMDb movie csv
csv = os.path.join("/home/lambert/filmsyl/filmsyl/raw_data", "imdb_movies.csv")
imdb_df = pd.read_csv(csv)
imdb_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
#import Netflix movie csv
csv_ = os.path.join("/home/lambert/filmsyl/filmsyl/raw_data", "jakob_movies.csv")
netflix_df = pd.read_csv(csv_)
netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)
netflix_df.dropna(inplace=True)
imdb_df.dropna(inplace=True)
#combine imdb text features.
imdb_df['text_features']= imdb_df['genres'] + ' ' + imdb_df['Director']
imdb_dfnew=imdb_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])
netflix_df['text_features'] = netflix_df['title'] + ' ' + netflix_df['genres'] + ' ' + netflix_df['Director']
netflix_dfnew=netflix_df.drop(columns=['genres','Director','averageRating','titleId','startYear','numVotes','runtimeMinutes'])
# Initialize CountVectorizer
vectorizer = CountVectorizer(stop_words='english')
# Fit and transform the text data for IMDb
imdb_text_matrix = vectorizer.fit_transform(imdb_df['text_features'])
# Fit and transform the text data for Netflix
netflix_text_matrix = vectorizer.transform(netflix_df['text_features'])
knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
knn_model.fit(imdb_text_matrix)
# Preprocess the text features of the new movie
new_movie = "Drugs, and family James Wan "  # Example text features of the new movie
new_movie_text_matrix = vectorizer.transform([new_movie])

# Nearest neighbors for the new movie
distances, indices = knn_model.kneighbors(new_movie_text_matrix)

# Get the indices of the nearest neighbors in the IMDb dataset
nearest_neighbor_indices = indices[0]

# Get the title of the suggested movie
suggested_movie_title = imdb_df.iloc[nearest_neighbor_indices]['title'].values[0]
print("IMDb Suggestion:", suggested_movie_title)
