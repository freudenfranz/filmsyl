"""
API for films you like package.
Paths:
    POST: /upload-netflix
"""

import pandas as pd
from fastapi import FastAPI, exceptions
from fastapi.middleware.cors import CORSMiddleware
from filmsyl.netflix.netflix import get_nf_imdb_matches
from filmsyl.model.basemodel import get_rec
from filmsyl.data.data import get_imdb
from filmsyl.cinemas.cinemas import get_running_movies_closeby

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/get-recommendations")
def upload_nf(netflix_json: dict) -> dict :
    """
    accepts:
    Route accepts a json with location closeby to user and it's netflix history
    containing  the columns 'Title' and 'Date'

    returns:
    statistical data on users watching habits
    recommendations for cinemas/movies closeby running
    recommendations for overall movies user could watch
    """
    print(netflix_json)
    try:
        #get subset of movies containing only movies from users netflix history
        iMDb_stats = get_nf_imdb_matches(netflix_json)

        #get statistics on users watching habits

        #get recommendations on movies user could watch from imdb list

        #get currently running movies in closeby cinemas

        #get recommendations for out of currently running movies in cinemas cb
        #return all combined results

        return iMDb_stats
    except Exception as e:
        raise exceptions.HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    netflix = pd.read_csv('./filmsyl/raw_data/NetflixViewingHistory.csv')
    nf_dict=netflix.to_dict()

    upload_nf(netflix_json=nf_dict)
    print('running fast.py')
