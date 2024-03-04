import streamlit as st
import requests
from datetime import datetime
from data_source import call_api

st.set_page_config(layout="centered") #wide

'''
# Taxi fare new york
'''

col1, col2, col3 = st.columns(3)
with col1:
    st.header("Pickup")
    pickup_date = st.date_input('pickup date', datetime.today())
    pickup_time = st.time_input('pickup time', datetime.now())
    pickup_lon = st.number_input('pickup longitude', min_value=40.000, max_value=42.000, value=40.700)
    pickup_lat = st.number_input('pickup latitude', min_value=-75.000, max_value=-70.000, value=-73.000)

with col2:
    st.header("Dropoff")
    dropoff_lon = st.number_input('dropoff longitude', min_value=40.000, max_value=42.000, value=40.700)
    dropoff_lat= st.number_input('dropoff latitude', min_value=-75.000, max_value=-70.000, value=-73.000)
with col3:
    st.header("Passengers")
    passengers = st.number_input('passenger count', min_value=1, max_value=8, value=1)

st.write(f'{pickup_date}%{pickup_time}')

base_url = f'https://taxifare.lewagon.ai/predict'
'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''
#?pickup_latitude=pi&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41

params = {
    'pickup_latitude': pickup_lat,
    'pickup_longitude': pickup_lon,
    'dropoff_latitude': dropoff_lat,
    'dropoff_longitude': dropoff_lon,
    'passenger_count': passengers,
    'pickup_datetime': f'{pickup_date}%{pickup_time}'
}
call_api(base_url, params)
requests.get(base_url,  params=params)
'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
