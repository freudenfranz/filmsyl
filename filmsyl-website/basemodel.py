import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

#import IMDb movie csv
csv = os.path.join("/home/lambert/filmsyl/filmsyl/raw_data", "imdb_movies.csv")
imdb_df = pd.read_csv(csv)
imdb_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)

#import Netflix movie csv
csv_ = os.path.join("/home/lambert/filmsyl/filmsyl/raw_data", "jakob_movies.csv")
netflix_df = pd.read_csv(csv_)
netflix_df.replace({'\\N': np.nan, '': np.nan}, inplace=True)

#combine imdb text features.
imdb_df['text_features']= imdb_df['genres'] + ' ' + imdb_df['title'] + ' ' + imdb_df['Director']
nan_count = imdb_df['text_features'].isna().sum()

#drop NaN values total 70574
netflix_df.dropna(subset=['text_features'], inplace=True)
imdb_df.dropna(subset=['text_features'], inplace=True)

# Initialize CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the text data for IMDb
imdb_text_matrix = vectorizer.fit_transform(imdb_df['text_features'])

# Fit and transform the text data for Netflix
netflix_text_matrix = vectorizer.transform(netflix_df['text_features'])

knn_model = NearestNeighbors(n_neighbors=4, metric='cosine')
knn_model.fit(imdb_text_matrix)

# Find nearest neighbors for Netflix data
distances, indices = knn_model.kneighbors(netflix_text_matrix)

imdb_recommendations = []  # Initialize an empty list to store IMDb recommendations

# Loop through each row in the DataFrame netflix_df
for i in range(len(netflix_df)):
    if len(indices[i]) > 1:  # Check if there are at least two neighbors
        second_nearest_neighbor_index = indices[i][1]  # Get the index of the second closest neighbor for the current row
        imdb_title = imdb_df.iloc[second_nearest_neighbor_index]['title']  # Retrieve the title from the IMDb DataFrame using the second nearest neighbor index
        netflix_title = netflix_df.iloc[i]['title']  # Retrieve the title of the Netflix movie
        imdb_recommendations.append((netflix_title, imdb_title))  # Append a tuple of Netflix title and IMDb recommendation

# Display the first 10 IMDb recommendations
for netflix_title, imdb_title in imdb_recommendations[:5]:
    print(f"We recommends '{imdb_title}'")
