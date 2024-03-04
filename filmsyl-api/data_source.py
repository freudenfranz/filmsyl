from datetime import datetime
import requests
def call_api(base_url: str, params):

    result =  requests.get(base_url, params=params)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json['fare']
    else:
        print(f'Api call returned with code {result.status_code}')


base_url = f'https://taxifare.lewagon.ai/predict'
#?pickup_latitude=40.72020&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41'
  #pickup_latitude=53.4      &pickup_longitude=17.5&dropoff_latitude=53.5&dropoff_longitude=16.1&passenger_count=1&pickup_datetime=%3Cbuilt-in+method+date+of+datetime.datetime+object+at+0x1044ba400%3E%25%3Cbuilt-in+method+time+of+datetime.datetime+object+at+0x1044ba400%3E
#Api


params = {
    'pickup_latitude': 53.4,
    'pickup_longitude': 17.5,
    'dropoff_latitude': 53.5,
    'dropoff_longitude': 16.1,
    'passenger_count': 1,
    'pickup_datetime': f'2024-03-01:08:41'
}

result = call_api(base_url=base_url, params=params)
