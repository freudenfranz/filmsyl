import streamlit as st
import requests
from datetime import datetime
from data_source import call_api


st.set_page_config(
            page_title="Quick reference", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="wide", # centered
            initial_sidebar_state="auto") # collapsed

'''
# Films you like
introduction
'''


categorisation, netflix, cinemas = st.tabs(["Film categorisation", "Netflix upload", "Movie recommendation"])
with categorisation:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with netflix:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with cinemas:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


base_url = f'https://taxifare.lewagon.ai/predict'

#?pickup_latitude=pi&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41

params = {
    'pickup_latitude': 'pickup_lat',
    'pickup_longitude': 'pickup_lon',
    'dropoff_latitude':' dropoff_lat',
    'dropoff_longitude': 'dropoff_lon',
    'passenger_count': 'passengers',
    #'pickup_datetime': f'{'pickup_date'}%{'pickup_time'}'
}
call_api(base_url, params)
requests.get(base_url,  params=params)
