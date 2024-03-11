"""
Querries api for cinemas in the vicinity of a location, and then gets all
movies running in these cinemas.
"""
## change lat, lng, territory for staging/production

import os
from filmsyl.settings import TIMEOUT
from datetime import datetime, timedelta
import requests

def get_running_movies_closeby(lat:float, lng:float, credentials):
    def get_show_times(cinema_id, date, device_datetime, authorization, x_api_key):
        url = f"https://api-gate2.movieglu.com/cinemaShowTimes/?cinema_id={cinema_id}&date={date}&sort=popularity"
        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "territory": "XX",
            "client": "LEWA"
        }

        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        # Check if the response is successful
        if response.status_code == 200:
            api_response = response.json()
            return api_response
        else:
            return f"Cinamas responded with code {response.status_code}"

    # Get tomorrow's date
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Set device datetime
    device_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def get_nearby_cinemas(latitude: float, longitude:float, authorization, x_api_key):
        url = "https://api-gate2.movieglu.com/cinemasNearby/?n=2"
        location = f"{str(latitude)};{str(longitude)}"
        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "geolocation": "-22.0; 14.0",#location,
            "territory": "XX",
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
                    'name': cinema['cinema_name'],
                    'cinema_id': cinema['cinema_id'],
                    'lat': cinema['lat'],
                    'lng': cinema['lng'],
                    'distance': cinema['distance']
                }
                cinemas_info.append(cinema_info)

            return cinemas_info
        else:
            print(f"Error. Cinema API returned status code {response.status_code} and reason {response.reason}")
            return None

    # Iterate over credentials
    for authorization, x_api_key in credentials:
        # Get nearby cinemas
        cinemas_info = get_nearby_cinemas(lat, lng, authorization, x_api_key)
        # If no cinemas are retrieved, proceed to the next credentials
        if cinemas_info is None:
            print("Warning: No cinemas info found")
            continue

        # Dictionary to store show times for each cinema
        show_times_dict = {}

        # Iterate over cinemas and get show times for tomorrow
        for cinema in cinemas_info:
            cinema_name = cinema['name']
            cinema_id = cinema['cinema_id']
            show_times = get_show_times(cinema_id, tomorrow_date, device_datetime, authorization, x_api_key)
            if show_times:
                show_times_dict[cinema_name] = show_times

        # If show times are retrieved successfully, return the result
        if show_times_dict:
            # Combine show_times_dict and cinemas_info into a single dictionary
            result_dict = {'show_times': show_times_dict, 'cinemas_info': cinemas_info}
            print("✅ got cinema/movie infos")
            # Return the combined dictionary as JSON
            return result_dict

    # If no successful response is obtained, return None
    return None


# Function to parse credentials from environment variables
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
    if len(credentials) == 0:
        print("ERROR: No cinema credentials found. Did you add them to your .env?")
    return credentials


if __name__ == '__main__':
    lat =  -22.0,
    lng = 14.0,

    result_dict = get_running_movies_closeby(lat, lng, parse_credentials())
    print(result_dict)
