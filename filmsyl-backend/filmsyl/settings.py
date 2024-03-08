import os
import numpy as np

##################  VARIABLES  ##################
IMDB_PATH = os.path.join(os.path.dirname(__file__),'data')
IMDB_FILNAME =  'final_and_clean_imdb.csv'
NETFLIX_FILENAME = 'jakob_movies.csv'

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


##################  CONSTANTS  #####################
#LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "data")
#LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")

#COLUMN_NAMES_RAW = ['fare_amount','pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']

""" DTYPES_RAW = {
    "fare_amount": "float32",
    "pickup_datetime": "datetime64[ns, UTC]",
    "pickup_longitude": "float32",
    "pickup_latitude": "float32",
    "dropoff_longitude": "float32",
    "dropoff_latitude": "float32",
    "passenger_count": "int16"
}

DTYPES_PROCESSED = np.float32
 """


################## VALIDATIONS #################

""" env_valid_options = dict(
    DATA_SIZE=["1k", "200k", "all"],
    MODEL_TARGET=["local", "gcs", "mlflow"],
)

def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


for env, valid_options in env_valid_options.items():
    validate_env_value(env, valid_options)
 """
