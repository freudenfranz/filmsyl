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

    #for authorization, x_api_key in credentials:
    # Get nearby cinemas

    cinemas_info = get_nearby_cinemas(latitude=lat,
                                        longitude=lng,
                                        device_datetime=device_datetime,
                                        cinemacount=cinemacount,
                                        territory=territory,
                                        credentials=credentials
                                        )


    # Iterate over cinemas and get show times for tomorrow
    showtimes_for_all_cinemas = []
    for cinema in cinemas_info:
        cinema_id = cinema['cinema_id']
        show_times = get_show_times(cinema_id=cinema_id,
                                    date=tomorrow_date,
                                    device_datetime=device_datetime,
                                    territory=territory,
                                    credentials=credentials
                                    )
        if show_times:
            for show_time in show_times:
                show_time.update(cinema)
                showtimes_for_all_cinemas.append(show_time)

    if showtimes_for_all_cinemas:
        print("✅ got cinema/movie infos")
        return showtimes_for_all_cinemas

    print("❌ Did not find any cinema/movie infos")
    return []

def get_nearby_cinemas(latitude: float,
                       longitude:float,
                       device_datetime,
                       credentials,
                       territory="DE",
                       cinemacount=1
                       ):
    """
    Get closeby cinemas based on userlocation
    """
    url = f"https://api-gate2.movieglu.com/cinemasNearby/?n={cinemacount}"
    location = f"{str(round(latitude, 3))};{str(round(longitude, 3))}"

    ##loop through all credentials until one works
    response = 0

    for authorization, x_api_key in credentials:
        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "geolocation": location,
            "territory": territory,
            "client": "LEWA"
        }
        print(f'▶️ url:{url}')
        print(f'▶️ headers:{headers}\n')

        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code == 200:
            print(f"✅ Found working key {x_api_key}")
            break
        else:
            print(f"❌Error. Key {x_api_key} returned status code '{response.status_code}'('{response.reason}')")

    # Check if the response is successful
    if response.status_code == 200:
        api_response = response.json()
        cinemas_info = []
        for cinema in api_response['cinemas']:
            try:
                cinema_info = {
                    'Cinema Name': cinema['cinema_name'],
                    'cinema_id': cinema['cinema_id'],
                    'Cinema Latitude': cinema['lat'],
                    'Cinema Longitude': cinema['lng'],
                    'Cinema Distance': cinema['distance'],
                    'Cinema Address': f"{cinema['address']} {cinema['address2']}, {cinema['postcode']} {cinema['city']}"
                }
            except IndexError:
                print(f"❌Error. One of the values could not be found for cinema '{cinema}'")
                cinema_info= {}
            cinemas_info.append(cinema_info)

        return cinemas_info
    else:
        print("❌Error. No Cinema API could be found'")
        return []

def get_show_times( cinema_id,
                    date,
                    device_datetime,
                    credentials,
                    territory="XX"
                    ):
    """
    Gets all showings of movies for a certain cinema
    """

    url = f"https://api-gate2.movieglu.com/cinemaShowTimes/?cinema_id={cinema_id}&date={date}&sort=popularity"
    # searchdate = datetime.strptime(date, '%Y-%m-%d')
    response = 0
    for authorization, x_api_key in credentials:
        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "date": date,
            "territory": territory,
            "client": "LEWA"
        }
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            break

    # Check if the response is successful
    if response.status_code == 200:
        api_response = response.json()
        movie_infos = []
        for movie in api_response['films']:
            for showing in movie["showings"]["Standard"]["times"]:
                try:
                    cinema_id = api_response['cinema']['cinema_id']
                except TypeError:
                    print(f"❌Error. Could not find cinema id for showing {showing}'")
                    cinema_id = None
                try:
                    film_name = movie['film_name']
                except TypeError:
                    print(f"❌Error. Could not find film name for showing {showing}'")
                    film_name = None
                try:
                    poster = movie['images']['poster']['1']['medium']['film_image'],
                except TypeError:
                    print(f"❌Error. Could not find poster for showing {showing}'")
                    poster = None
                try:
                    start_time = showing["start_time"]
                except TypeError:
                    print(f"❌Error. Could not find start timefor showing {showing}'")
                    start_time = None
                try:
                    stop_time = showing["end_time"]
                except TypeError:
                    print(f"❌Error. Could not find stop time for showing {showing}'")
                    stop_time = None

                movie_info = {
                    'cinema_id': cinema_id,
                    'Film Name': film_name,
                    'Poster': poster,
                    "Start Time": start_time,
                    "End Time": stop_time,
                    "Date": date
                }

                movie_infos.append(movie_info)
        return movie_infos
    else:
        print(f"▶❌Error. Cinemas api responded with code {response.status_code} for getting show times")
        return []

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
        print("⚠️Warning: No cinema credentials found. Did you add them to your .env?")
    return credentials


if __name__ == '__main__':
    LATITUDE =  -22.0
    LONGITUDE = 14.0

    res_dict = get_running_movies_closeby(
        LATITUDE,
        LONGITUDE,
        parse_credentials())
    print(res_dict)
