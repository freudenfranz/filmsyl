import streamlit as st
import requests
from datetime import datetime
from data_source import get_api, post_api
import pandas as pd
from io import StringIO
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px
import ast


base_url = 'https://films-you-like-2h7mcggcwa-ew.a.run.app'
params = {}

st.set_page_config(
            page_title="Quick reference", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="wide", # centered
            initial_sidebar_state="auto") # collapsed


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
        post_result = post_api(f'{base_url}/get-recommendations', params={}, data=dataframe.to_json())
        st.text(post_result['statistics'])
        st.text(post_result['matched_rows'])

        total_films = post_result['statistics']['total_films_count']
        first_director = list(post_result['statistics']['directors_count'].keys())[0]

    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
    else:
        # Automatically scroll to "Your films in numbers" section
        st.divider()
        # Automatically scroll to "Your films in numbers" section
        st.markdown("""
            <script>
                document.getElementById('your-films-section').scrollIntoView({ behavior: 'smooth' });
            </script>
        """, unsafe_allow_html=True)
        st.title("Your films in numbers.")
        # Placeholder for film numbers and favorite director
        col1, col2 = st.columns([2, 3])  # Adjust the width ratio as needed
        with col1:
            st.markdown(f"""
                <h1 style='color: blue;'>{total_films}</h1>
                total movies watched.

                <h1 style='color: blue;'>{first_director}</h1>
                <h2 style='margin-top: 20px;'>is your favorite director.</h2>
            """, unsafe_allow_html=True)
        with col2:
            # Display top genres chart
            st.subheader("Your top genres.")
            genres_json_data = pd.DataFrame({
            'Genre': ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Thriller'],
            'Count': [350, 300, 250, 200, 150]  # Sample data
             }).sort_values(by='Count', ascending=False)

            # Convert JSON data to DataFrame
            genres_data = pd.DataFrame(genres_json_data)
            fig1 = px.bar(genres_data, x='Count', y='Genre', orientation='h', color='Genre')
            fig1.update_layout(
                showlegend=False,
                xaxis_title=None,
                yaxis_title=None,
                margin=dict(t=20, b=20, l=20, r=20)  # Adjust the margin as needed
            )
            st.plotly_chart(fig1)

        #st.markdown(":blue[1200] total movies watched")

            # Save the uploaded file
            # #with open(uploaded_file.name, "wb") as f:
            # #   f.write(uploaded_file.getbuffer())
            # # Display success message
            # st.success('File saved successfully')
        #except Exception as e:
         #   st.error(f'An error occurred: {str(e)}')

        # Display top genres
    st.divider()
    st.title('Uncovering :blue[the latest] films to watch 🎬')
        #st.title('_Streamlit_ is :blue[cool] :sunglasses:')

   # Load movie data from JSON file
    movie_json_data = {
        'Name': ['Movie 1', 'Movie 2', 'Movie 3'],
        'Rating': [4.5, 3.8, 4.2],
        'Location': ['New York', 'Los Angeles', 'Chicago'],
        'Latitude': [40.7128, 34.0522, 41.8781],
        'Longitude': [-74.0060, -118.2437, -87.6298],
        'Image': ['https://via.placeholder.com/150', 'https://via.placeholder.com/150', 'https://via.placeholder.com/150']
        }

# Image size 212 x 300

    # Convert movie data from JSON to DataFrame
    movie_data = pd.DataFrame(movie_json_data)

    # Display the map
    st.write("Location Map")
    map_data = pd.DataFrame({
        'latitude': [52.5200],
        'longitude': [13.4050]
    })
    st.map(map_data)

    # Display movie information
    for index, row in movie_data.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(row['Image'], width=150, caption=row['Name'])
        with col2:
            st.write(f"Name: {row['Name']}")
            st.write(f"Rating: {row['Rating']}")
            st.write(f"Location: {row['Location']}")

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
