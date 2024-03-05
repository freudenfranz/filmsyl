from datetime import datetime
import requests
def call_api(base_url: str, params):

    result =  requests.get(base_url, params=params)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json
    else:
        print(f'Api call returned with code {result.status_code}')
