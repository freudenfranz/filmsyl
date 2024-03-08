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

@app.get("/recommendations")
def get_recommendations():
    """
    get movie reccomendations from a previously uploaded netflix history file
    """
    imdb_df = get_imdb()
    if(app.state.matched_rows):
        print(app.state.matched_rows)
        netflix_df = pd.DataFrame(app.state.matched_rows)
        recommendations = get_rec(10,imdb_df=imdb_df, netflix_df=netflix_df)
        print(recommendations)
        return recommendations
    else:
        print("No netflix history uploded")
        return exceptions.HTTPException(status_code=404, detail="no netflix history uploaded")


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
    try:
        #get subset of movies containing only movies from users netflix history
        iMDb_stats = get_nf_imdb_matches(netflix_json)

        #get statistics on users watching habits

        #get recommendations on movies user could watch from imdb list
        #get currently running movies in closeby cinemas
        #get recommendations for out of currently running movies in cinemas cb
        #return all combined results
        app.state.matched_rows = iMDb_stats['matched_rows']
        if(app.state.matched_rows):
            print(f'app state saved: {app.state.matched_rows}')
        return iMDb_stats
    except Exception as e:
        raise exceptions.HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    print('running fast.py')
