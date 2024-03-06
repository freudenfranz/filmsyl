import streamlit as st
import requests
from datetime import datetime
from data_source import call_api

#base_url = f'https://taxifare.lewagon.ai/predict'
base_url = 'https://films-you-like-2h7mcggcwa-ew.a.run.app'
params = {}

clusters = call_api(f'{base_url}/cluster', params)

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
   for i, cluster in enumerate(clusters):
       st.header(f"cluster {i}")
       for movie in cluster:
           st.text(movie)


with netflix:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)




with cinemas:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)




#?pickup_latitude=pi&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41
