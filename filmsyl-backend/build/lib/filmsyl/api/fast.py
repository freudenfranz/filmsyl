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

@app.get("/")
def index():
    """Root Endpoint"""
    msg = {"welcome_message":"Welcome to movies you like api. "
     "Please refer to /docs for more information"}
    return msg

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

        #get currently running movies in closeby cinemas
        cine_recommendations = get_running_movies_closeby(
            lat=float(location['lat']),
            lng=float(location['lng']),
            credentials=MOVIEGLU_CREDENTIALS,
            territory= location['countrycode'] if location['countrycode'] else "XX",
            cinemacount=payload['cinemacount']
            )

        if(cine_recommendations):
            rec_titles = pd.DataFrame([rec['Film Name'] for rec in cine_recommendations])
            cine_recs_in_db = imdb_df[imdb_df['primaryTitle'].isin(rec_titles[0])]
            rich_recommends, not_found = enrich_recommendations(cine_recommendations, cine_recs_in_db)
            recs_result = get_movie_recommendation(6, imdb_df=imdb_df, netflix_df=found, new_movies=cine_recs_in_db)
        else:
            rich_recommends= []
            recs_result = []
            not_found = []

        #return all combined results

        result = {
            "statistics": imdb_stats['statistics'],
            'matched_rows':imdb_stats['matched_rows'],
            "recommendations": recs_result,
            "showings": rich_recommends,
            "not_fonud_cine_recs": not_found
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def enrich_recommendations(cine_recommendations:list, cine_recs_in_db: pd.DataFrame)-> list:
    """
    repacked dictionary to a better output
    """
    new_recommendations=[]
    not_found = []
    for rec in cine_recommendations:
        imdb_rec = cine_recs_in_db[cine_recs_in_db['primaryTitle']==rec["Film Name"]]

        if(imdb_rec.shape[0] == 1):
            imdb_rec = imdb_rec.head(1)
            rec["Film Name"]=imdb_rec['title'].head(1).values[0]
            rec["Film Director"]=imdb_rec['Director'].head(1).values[0]
            rec["Film Rating"]=imdb_rec['averageRating'].head(1).values[0]
            rec["Film Votes"]=imdb_rec['numVotes'].head(1).head(1).values[0]
            rec["Film Duration"]=imdb_rec['runtimeMinutes'].head(1).values[0]
            rec["Film Genre"]=imdb_rec['genres'].head(1).values[0]
            rec['Start Year']=imdb_rec['startYear'].head(1).values[0]
            rec['plot']=imdb_rec['plot'].head(1).values[0]
            rec["IMDB ID"]=imdb_rec['titleId'].head(1).values[0]
        else:
            print(f'❗WARNING: Did not find cinema movie {rec["Film Name"]} in imdb db❗')
            not_found.append(rec["Film Name"])
        new_recommendations.append(rec)
    return new_recommendations, not_found


if __name__ == '__main__':
    nf_history = pd.read_csv('./filmsyl/data/NetflixViewingHistory.csv')
    nf_history.dropna(inplace=True)
    location = Location(lat= -22.0, lng=14.0, countrycode="XX")

    hist = [NetflixHistory(Title=h[1].Title, Date=h[1].Date) for h in nf_history.iterrows()]
    body = RecommendationBody(location=location,cinemacount=2, netflix=hist)
    recs= get_recommendations(body)

    print(recs)
