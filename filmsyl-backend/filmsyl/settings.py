import os
import numpy as np

##################  VARIABLES  ##################
IMDB_PATH = os.path.join(os.path.dirname(__file__),'data')
IMDB_FILNAME =  'final_and_clean_imdb.csv'
NETFLIX_FILENAME = 'NetflixViewingHistory.csv'

# parsing credentials needed for the movieglu api
def parse_credentials():
    credentials = []
    i = 1
    while True:
        credential_key = f"CREDENTIALS_{i}"
        credential_value = os.getenv(credential_key)
        if credential_value is None:
            break
        credentials.append(tuple(credential_value.split(',')))
        i += 1
    return credentials

MOVIEGLU_CREDENTIALS = parse_credentials()
TIMEOUT = 6
