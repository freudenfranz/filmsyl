"""
Querries api for cinemas in the vicinity of a location, and then gets all
movies running in these cinemas.
"""


import json
from datetime import datetime, timedelta
import requests
from settings import MOVIEGLU_CREDENTIALS

def get_running_movies_closeby(lat: float, lon:float, credentials)->dict:
    def get_show_times(cinema_id, date, device_datetime, authorization, x_api_key):
        url = f"https://api-gate2.movieglu.com/cinemaShowTimes/?cinema_id={cinema_id}&date={date}&sort=popularity"
        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "territory": "DE",
            "client": "LEWA"
        }

        response = requests.get(url, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            api_response = response.json()
            return api_response
        else:
            return None

    # Get tomorrow's date
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Set device datetime
    device_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def get_nearby_cinemas(lat, lng, authorization, x_api_key):
        url = "https://api-gate2.movieglu.com/cinemasNearby/?n=5"

        headers = {
            "api-version": "v200",
            "Authorization": authorization,
            "x-api-key": x_api_key,
            "device-datetime": device_datetime,
            "geolocation": f"{lat};{lng}",
            "territory": "DE",
            "client": "LEWA"
        }

        response = requests.get(url, headers=headers)

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
            return None

    # Iterate over credentials
    for authorization, x_api_key in MOVIEGLU_CREDENTIALS:
        # Get nearby cinemas
        cinemas_info = get_nearby_cinemas(lat, lng, authorization, x_api_key)

        # If no cinemas are retrieved, proceed to the next credentials
        if cinemas_info is None:
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

            # Return the combined dictionary as JSON
            return result_dict

    # If no successful response is obtained, return None
    return None


if __name__ == '__main__':
    lat = "52.49"
    lng = "13.42"

    result_dict = get_running_movies_closeby(lat, lng, MOVIEGLU_CREDENTIALS)
    result_dict
