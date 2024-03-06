import streamlit as st
import requests
from datetime import datetime
from data_source import get_api, post_api
import pandas as pd
from io import StringIO

#base_url = f'https://taxifare.lewagon.ai/predict'
base_url = 'https://films-you-like-2h7mcggcwa-ew.a.run.app'
params = {}

clusters = get_api(f'{base_url}/cluster', params)


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

#@st.cache

st.markdown("""

    ## Please upload your Netflix History:

""")

uploaded_file = st.file_uploader('Upload CSV', accept_multiple_files=False, type=['csv'])


if st.button('Upload File') and uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()

        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        string_data = stringio.read()

        dataframe = pd.read_csv(uploaded_file)
        post_result = post_api(f'{base_url}/upload-netflix', params={}, data=dataframe.to_json())
        st.text(post_result)
        # Save the uploaded file
        #with open(uploaded_file.name, "wb") as f:
         #   f.write(uploaded_file.getbuffer())

        # Display success message
        st.success('File saved successfully')

    except Exception as e:
        st.error(f'An error occurred: {str(e)}')






#if st.button("Upload PDF"):
 #   payload = {"username": username, "filename": uploaded_file.name}
  #  response = requests.post(base_url, params=payload, files={"uploaded_file": uploaded_file.getvalue()})
   # st.write(response)


with cinemas:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)




#?pickup_latitude=pi&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41
