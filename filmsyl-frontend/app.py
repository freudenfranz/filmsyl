import streamlit as st
import requests
from datetime import datetime
from data_source import get_api, post_api
import pandas as pd
from io import StringIO
from streamlit_option_menu import option_menu


base_url = 'https://films-you-like-2h7mcggcwa-ew.a.run.app'
params = {}

st.set_page_config(
            page_title="Quick reference", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="wide", # centered
            initial_sidebar_state="auto") # collapsed

clusters = get_api(f'{base_url}/cluster', params)

with st.sidebar:
    selected = option_menu(None, ["Home", 'Discovery films'],
        icons=['house', 'gear'], menu_icon="cast", default_index=0)


if selected == "Home":
    st.title(f'Ready to find the films you like?')
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
            # #with open(uploaded_file.name, "wb") as f:
            # #   f.write(uploaded_file.getbuffer())
            # # Display success message
            # st.success('File saved successfully')
        except Exception as e:
            st.error(f'An error occurred: {str(e)}')

        st.markdown("""


        Your films in numbers.

        """)


if selected == "Discovery films":
    st.title('Uncovering :blue[the latest] films to watch.')
    #st.title('_Streamlit_ is :blue[cool] :sunglasses:')
    location = "Enter your location"
    st.text_input(location)



#categorisation, netflix, cinemas = st.tabs(["Film categorisation", "Netflix upload", "Movie recommendation"])
#with categorisation:
 #  for i, cluster in enumerate(clusters):
  #     st.header(f"cluster {i}")
   #    for movie in cluster:
    #       st.text(movie)


#with netflix:
  # st.header("A dog")
   #st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

#@st.cache


#with cinemas:
 #  st.header("An owl")
  # st.image("https://static.streamlit.io/examples/owl.jpg", width=200)




#?pickup_latitude=pi&pickup_longitude=-82.5359751617647&dropoff_latitude=40.720201&dropoff_longitude=-74.032574&passenger_count=1&pickup_datetime=2024-03-01%2016:08:41
