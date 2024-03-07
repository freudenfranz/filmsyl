import streamlit as st
import requests
from datetime import datetime
from data_source import get_api, post_api
import pandas as pd
from io import StringIO
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px


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

        st.header("Your films in numbers.")
        st.subheader(":blue[1200]")

        # Pull data to display horizontal bar chart
        st.write("total movies watched.")

        # Pull data to display horizontal bar chart
        genres_data = pd.DataFrame({
        'Genre': ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Thriller'],
        'Count': [350, 300, 250, 200, 150]  # Sample data
        }).sort_values(by='Count', ascending=False)

        st.subheader("Your top genres.")
        fig = px.bar(genres_data, x='Count', y='Genre', orientation='h', color='Genre')
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig)

         # Pull data to display bar chart for most watched years
        years_data = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'Count': [100, 150, 200, 300, 210, 180, 20]  # Sample data
        }).sort_values(by='Count', ascending=False)

        st.header("Most watched years.")
        fig2 = px.bar(years_data, x='Year', y='Count', color='Year')
        fig2.update_traces(showlegend=False)  # Remove legend
        fig2.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
        fig2.update_xaxes(tickvals=years_data['Year'], ticktext=[str(int(year)) for year in years_data['Year']])
        st.plotly_chart(fig2)

if selected == "Discovery films":
    st.title('Uncovering :blue[the latest] films to watch 🎬')
    #st.title('_Streamlit_ is :blue[cool] :sunglasses:')

    zip_code = st.text_input("Enter Zip Code:")

   # Sample movie data
    movie_data = pd.DataFrame({
    'Name': ['Movie 1', 'Movie 2', 'Movie 3'],
    'Rating': [4.5, 3.8, 4.2],
    'Location': ['New York', 'Los Angeles', 'Chicago'],
    'Latitude': [40.7128, 34.0522, 41.8781],
    'Longitude': [-74.0060, -118.2437, -87.6298],
    'Image': ['https://via.placeholder.com/150', 'https://via.placeholder.com/150', 'https://via.placeholder.com/150']
})

    # Create a new DataFrame for mapping
    map_data = pd.DataFrame({
    'LAT': movie_data['Latitude'],
    'LON': movie_data['Longitude'],
    'Name': movie_data['Name']
})

    # Boolean variable to track whether to show the map
    show_map = False

    # Display movie information
    for index, row in movie_data.iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(row['Image'], width=150, caption=row['Name'])
        with col2:
            st.write(f"Name: {row['Name']}")
            st.write(f"Rating: {row['Rating']}")
            st.write(f"Location: {row['Location']}")

        # Display movie button
        if st.button(f"Show Location Map for {row['Name']}"):
            # Show movie location on map when button is clicked
            show_map = True
            selected_movie = row['Name']

        # Show the map if the show_map variable is True
        if show_map and selected_movie == row['Name']:
            st.write(f"Location Map for {selected_movie}")
            st.map(map_data[map_data['Name'] == selected_movie])

            # Button to close the map and go back to initial layout
            if st.button("Close Map"):
                show_map = False


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
