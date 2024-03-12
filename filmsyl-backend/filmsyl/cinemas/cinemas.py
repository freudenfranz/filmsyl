"""
Querries api for cinemas in the vicinity of a location, and then gets all
movies running in these cinemas.
"""
## change lat, lng, territory for staging/production

import os
from datetime import datetime, timedelta
import requests
from filmsyl.settings import TIMEOUT

def get_running_movies_closeby(lat:float, lng:float, credentials, territory="XX", cinemacount=1):
    """
    Finds movies running in cinemas closeby to users location
    """
    # Get tomorrow's date
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    # Set device datetime
    device_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # Iterate over credentials

    for authorization, x_api_key in credentials:
        # Get nearby cinemas
        cinemas_info = get_nearby_cinemas(latitude=lat,
                                          longitude=lng,
                                          authorization=authorization,
                                          device_datetime=device_datetime,
                                          x_api_key=x_api_key,
                                          cinemacount=cinemacount)

        # If no cinemas are retrieved, proceed to the next credentials
        if cinemas_info is None:
            print("Warning: No cinemas info found")
            continue

        # Dictionary to store show times for each cinema
        show_times_dict = []

        # Iterate over cinemas and get show times for tomorrow
        for cinema in cinemas_info:
            cinema_id = cinema['cinema_id']
            show_times = get_show_times(cinema_id=cinema_id,
                                        date=tomorrow_date,
                                        device_datetime=device_datetime,
                                        authorization=authorization,
                                        x_api_key=x_api_key,
                                        territory=territory)
            if show_times:
                for show_time in show_times:
                    show_time.update(cinema)
                show_times_dict.append(show_times)


        # If show times are retrieved successfully, return the result
        if show_times_dict:
            # Combine show_times_dict and cinemas_info into a single dictionary
            print("✅ got cinema/movie infos")
            # Return the combined dictionary as JSON
            return show_times

    # If no successful response is obtained, return None
    print("🚫 Could not get cinema/movie infos")
    return "Too many requests"

def get_nearby_cinemas(latitude: float,
                       longitude:float,
                       authorization,
                       device_datetime,
                       x_api_key,
                       territory="XX",
                       cinemacount=1,):
    """
    Get closeby cinemas based on userlocation
    """
    url = f"https://api-gate2.movieglu.com/cinemasNearby/?n={cinemacount}"
    location = f"{str(latitude)};{str(longitude)}"
    headers = {
        "api-version": "v200",
        "Authorization": authorization,
        "x-api-key": x_api_key,
        "device-datetime": device_datetime,
        "geolocation": location,
        "territory": territory,
        "client": "LEWA"
    }
    print(headers)
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    # Check if the response is successful
    if response.status_code == 200:
        api_response = response.json()
        cinemas_info = []
        for cinema in api_response['cinemas']:
            cinema_info = {
                'Cinema Name': cinema['cinema_name'],
                'cinema_id': cinema['cinema_id'],
                'Cinema Latitude': cinema['lat'],
                'Cinema Longitude': cinema['lng'],
                'Cinema Distance': cinema['distance'],
                'Cinema Address': f"{cinema['address']} {cinema['address2']}, {cinema['postcode']} {cinema['city']}"
            }
            cinemas_info.append(cinema_info)

        return cinemas_info
    else:
        print(f"Error. Cinema API returned status code {response.status_code} and reason {response.reason}")
        return None

def get_show_times(cinema_id,
                    date,
                    device_datetime,
                    authorization,
                    x_api_key,
                    territory="XX"):
    """
    Gets all showings of movies for a certain cinema
    """

    url = f"https://api-gate2.movieglu.com/cinemaShowTimes/?cinema_id={cinema_id}&date={date}&sort=popularity"
    # searchdate = datetime.strptime(date, '%Y-%m-%d')

    headers = {
        "api-version": "v200",
        "Authorization": authorization,
        "x-api-key": x_api_key,
        "device-datetime": device_datetime,
        "date": date,
        "territory": territory,
        "client": "LEWA"
    }
    print(headers)
    response = requests.get(url, headers=headers, timeout=TIMEOUT)

    # Check if the response is successful
    if response.status_code == 200:
        api_response = response.json()
        movie_infos = []
        for movie in api_response['films']:
            for showing in movie["showings"]["Standard"]["times"]:
                movie_info = {
                    'cinema_id': api_response['cinema']['cinema_id'],
                    'Film Name': movie['film_name'],
                    'Poster': movie['images']['poster']['1']['medium']['film_image'],
                    "Start Time": showing["start_time"],
                    "End Time": showing["end_time"],
                    "Date": date,
            }
            movie_infos.append(movie_info)
        return movie_infos
    else:
        print(f"Cinamas responded with code {response.status_code}")
        return None

# Function to parse credentials from environment variables
def parse_credentials():
    """
    Reads a list of credentials for .env file to try out various keys
    """
    credentials = []
    i = 1
    while True:
        credential_key = f"CREDENTIALS_{i}"
        credential_value = os.getenv(credential_key)
        if credential_value is None:
            break
        credentials.append(tuple(credential_value.split(',')))
        i += 1
    if len(credentials) == 0:
        print("ERROR: No cinema credentials found. Did you add them to your .env?")
    return credentials


if __name__ == '__main__':
    LATITUDE =  -22.0
    LONGITUDE = 14.0

    res_dict = get_running_movies_closeby(
        LATITUDE,
        LONGITUDE,
        parse_credentials())
    print(res_dict)
