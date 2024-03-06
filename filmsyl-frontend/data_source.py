from datetime import datetime
import requests
def get_api(base_url: str, params):

    result =  requests.get(base_url, params=params)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json
    else:
        print(f'Api call returned with code {result.status_code}')



def post_api(base_url: str, params, data):

    result =  requests.post(base_url, params=params, data=data)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json
    else:
        print(f'Api call returned with code {result.status_code}')
