"""
API for films you like package.
Paths:
    POST: /upload-netflix
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from filmsyl.netflix.netflix import get_nf_matches_from_iMDb



app = FastAPI()
#app.state.model=load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/cluster")
def clusterize():
    #X_pred = pd.DataFrame({
    #        'pickup_datetime':[pd.Timestamp(pickup_datetime, tz='UTC')],
    #        'pickup_longitude':[pickup_longitude],
    #        'pickup_latitude':[pickup_latitude],
    #        'dropoff_longitude':[dropoff_longitude],
    #        'dropoff_latitude':[dropoff_latitude],
    #        'passenger_count':[passenger_count],
    #    }
    #)

    #X_processed = preprocess_features(X_pred)
    #y_pred = app.state.model.predict(X_processed)
    cluster1 = [
        "movie1c1", "movie1c2", "movie1c3"
    ]
    cluster2 = [
        "movie2c1", "movie2c2", "movie2c3"
    ]
    cluster3 = [
        "movie3c1", "movie3c2", "movie3c3"
    ]
    return [cluster1, cluster2, cluster3]


@app.post("/upload-netflix")
def upload_nf(netflix_json: dict) -> dict :
    #try:
        # Process the JSON data as needed
        #print(f"LOG: got netflix json:\n {netflix_json}")
        iMDb_stats = get_nf_matches_from_iMDb(netflix_json)
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
