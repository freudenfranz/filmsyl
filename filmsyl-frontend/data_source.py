from datetime import datetime
import requests

timeout = 6 #s
def get_api(base_url: str, params):
    """Wrapper for an api GET"""
    result =  requests.get(base_url, params=params, timeout=timeout)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json
    else:
        print(f'Api call returned with code {result.status_code}')



def post_api(base_url: str, params, data):
    """Wrapper for an api post"""
    result =  requests.post(base_url, params=params, data=data, timeout=timeout)
    print(result.url)
    if result.status_code < 300:
        json = result.json()
        return json
    else:
        print(f'Api call returned with code {result.status_code}')
