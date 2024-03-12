"""
API for films you like package.
Paths:
    POST: /upload-netflix
"""

from typing import List, Union
from typing_extensions import Annotated
from pydantic import BaseModel

import pandas as pd
from fastapi import Body, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from filmsyl.netflix.netflix import clean_titles, get_nf_imdb_matches
from filmsyl.model.basemodel import get_movie_recommendation
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

class Location(BaseModel):
    """Location object constisting of latittude and longitude"""
    lat: float
    lng: float
    countrycode: Union[str, None]


class NetflixHistory(BaseModel):
    """Descriptor for Netflix history as pandas object transmitted"""
    Title: str
    Date:  str

class RecommendationBody(BaseModel):
    """
    Descriptor for post request body
    """
    location: Location
    cinemacount: Union[int, None]
    netflix: List[NetflixHistory]

@app.post("/get-recommendations")
def get_recommendations(
    payload:
        Annotated[
            RecommendationBody,
            Body(
                examples=[
                    {
                        "location": {
                            "lat": -22.0,
                            "lng": 14.0,
                            "countrycode": "XX",
                        },
                        "cinemacount": 1,
                        "netflix": [
                            {
                            "Title": "The Godfather",
                            "Date": "27/02/2024"
                            },
                            {
                            "Title": "The Avatar",
                            "Date": "22/06/2024"
                            }
                        ]
                    }
                ],
            ),
        ],
    ) -> dict :
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
        #print(f"✅ netflix_json.keys contains {netflix_json.keys()}")
        #get subset of movies containing only movies from users netflix history
        payload = payload.model_dump()
        location = payload['location']
        netflix_json = payload['netflix']
        nf_df = pd.DataFrame(netflix_json)
        imdb_stats = get_nf_imdb_matches(nf_df)
        #get statistics on users watching habits

        #get recommendations on movies user could watch from imdb list
        imdb_df = get_imdb()

        #nf_df = pd.read_json(netflix_json, orient='records')['Title']
        cleaned = clean_titles(nf_df['Title'])
        found = find_titles_in_imdb(cleaned, imdb_df)

        recs_result = get_movie_recommendation(6, imdb_df=imdb_df, netflix_df=found)

        #get currently running movies in closeby cinemas
        cine_recommendations = get_running_movies_closeby(
            lat=float(location['lat']),
            lng=float(location['lng']),
            credentials=MOVIEGLU_CREDENTIALS,
            territory= location['countrycode'] if location['countrycode'] else "XX",
            cinemacount=payload['cinemacount']
            )

        #return all combined results
        result = {
            "statistics": imdb_stats['statistics'],
            'matched_rows':imdb_stats['matched_rows'],
            "recommendations": recs_result.to_dict(),
            "showings": cine_recommendations
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e




if __name__ == '__main__':
    nf_history = pd.read_csv('./filmsyl/data/NetflixViewingHistory.csv')#.to_dict(orient="records")
    nf_history.dropna(inplace=True)
    location = Location(lat= -22.0, lng=14.0, countrycode="XX")

    hist = [NetflixHistory(Title=h[1].Title, Date=h[1].Date) for h in nf_history.iterrows()]
    body = RecommendationBody(location=location,cinemacount=2, netflix=hist)
    recs= get_recommendations(body)
    print(recs)
