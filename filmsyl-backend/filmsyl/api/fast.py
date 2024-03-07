"""
API for films you like package.
Paths:
    POST: /upload-netflix
"""
from fastapi import FastAPI, exceptions
from fastapi.middleware.cors import CORSMiddleware
from filmsyl.netflix.netflix import get_nf_imdb_matches
from filmsyl.model.basemodel import get_rec
from filmsyl.model.data import get_imdb
import pandas as pd



app = FastAPI()
app.state.matched_rows = {}

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


@app.post("/upload-netflix")
def upload_nf(netflix_json: dict) -> dict :
    #try:
        # Process the JSON data as needed
        #print(f"LOG: got netflix json:\n {netflix_json}")
        iMDb_stats = get_nf_imdb_matches(netflix_json)
        app.state.matched_rows = iMDb_stats['matched_rows']
        return iMDb_stats
    #except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))

mock_nf = {
  "Title": {
    "0": "Uncharted",
    "1": "The Punisher"
  },
  "Date": {
    "0": "18\/02\/2024",
    "1": "10\/02\/2024"
  }
}

if __name__ == '__main__':
    nf =  upload_nf(mock_nf)
    print(nf)
