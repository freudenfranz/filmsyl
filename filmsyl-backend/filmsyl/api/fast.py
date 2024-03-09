"""
API for films you like package.
Paths:
    POST: /upload-netflix
"""

import pandas as pd
from typing import Annotated
from fastapi import Body, FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from filmsyl.netflix.netflix import clean_titles, find_and_return_matches, get_nf_imdb_matches
from filmsyl.model.basemodel import get_rec
from filmsyl.data.data import find_titles_in_imdb, get_imdb
from filmsyl.cinemas.cinemas import get_running_movies_closeby
from filmsyl.settings import MOVIEGLU_CREDENTIALS
app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app = FastAPI()


#class NetflixHistory(BaseModel):
    #"""Descriptor for Netflix history as pandas object transmitted"""
    #Title: {
        #str: str
    #}
    #Date: {
        #str
    #}

class RecommendationBody(BaseModel):
    """
    Descriptor for post request body
    """
    lat: float
    lon: float
    netflix: dict


@app.post("/get-recommendations")
def get_recommendations(netflix_json: Annotated[
        RecommendationBody,
        Body(
            examples=[
                {   'lat': 52.5068927,
                    'lng': 13.3564182,
                    "netflix": {
                         "Title": {

                         },
                         "Date": {

                         }
                    }
                }
            ],
        ),
    ],) -> dict :
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

        print(f"✅ netflix_json.keys contains {netflix_json.keys()}")
        #get subset of movies containing only movies from users netflix history
        iMDb_stats = get_nf_imdb_matches(netflix_json)

        #get statistics on users watching habits

        #get recommendations on movies user could watch from imdb list
        imdb_df = get_imdb()
        nf_df = pd.DataFrame(netflix_json)['Title']
        cleaned = clean_titles(nf_df)
        found = find_titles_in_imdb(cleaned, imdb_df)
        recs_result = get_rec(6, imdb_df=imdb_df, netflix_df=found)

        #get currently running movies in closeby cinemas
        cine_recommendations = {}#get_running_movies_closeby(
            #lat=52.5068927, lng=3.3564182, credentials=MOVIEGLU_CREDENTIALS)

        #return all combined results
        result = {
            "statistics": iMDb_stats['statistics'],
            'matched_rows':iMDb_stats['matched_rows'],
            "recommendations": recs_result.to_dict(),
            "cinerec": cine_recommendations
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    netflix = pd.read_csv('./filmsyl/data/NetflixViewingHistory.csv')
    nf_dict=netflix.to_dict()

    recs= get_recommendations(netflix_json=nf_dict)

    print(recs)
