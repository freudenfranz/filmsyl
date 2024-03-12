import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from streamlit_js_eval import get_geolocation
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time
import json

API_ENDPOINT = "https://films-you-like-dev-2h7mcggcwa-ew.a.run.app/get-recommendations"
#API_ENDPOINT= "http://127.0.0.1:8000/get-recommendations"


def main():
    # Display centered title
    display_title()

    # Get and display geolocation
    geolocation, latitude, longitude = get_and_display_geolocation()

    # Upload Netflix history
    df = upload_netflix_history(geolocation)

    # Process Netflix data
    netflix_data = process_netflix_data(df)

    if netflix_data:
        # Display a spinner while waiting for the API response
        st.markdown("<br><br><br>", unsafe_allow_html=True)  # Add some space before the spinner
        with st.spinner("We are trying to understand your weird taste..."):
            # Send data to API and get response
            response = send_to_api(netflix_data, latitude, longitude)

        # Load JSON file
        #with open('combined_output.json', 'r') as f:
        #    response = json.load(f)

        # Display "scroll down" message
        display_scroll_down_message()

        # Display Netflix history
        display_netflix_history(response)

        # Display "scroll down" message again
        display_scroll_down_message()

        cinemas_info = response["showings"] #data should be the json received from the api, currently we have 'repsonse' which is a

        # Create the map
        create_map(latitude, longitude, cinemas_info)

        # Show films in cinemas
        show_films_in_cinemas(response)

def display_title():
    """
    Display the centered title for the app.
    """
    st.markdown("<h1 style='text-align: center;'>Ready to find films you like screening near you?</h1>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: #808080; '>Upload your Netflix history and decide when and where to go to the cinema</h6>", unsafe_allow_html=True)

def get_and_display_geolocation():
    """
    Get geolocation and display warning if not available.
    """
    geolocation = get_geolocation()
    if geolocation:
        latitude = -22.0### CHANGE WHEN IN PRODUCTION geolocation['coords']['latitude']
        longitude = 14.0### CHANGE WHEN IN PRODUCTION geolocation['coords']['longitude']
        return geolocation, latitude, longitude
    else:
        time.sleep(5)  # Adjust the delay time as needed
        st.warning("Please allow geolocation for this app to work")
        return None, None, None

def upload_netflix_history(geolocation):
    """
    Allow the user to upload their Netflix history and process the data.
    """
    if geolocation:
        latitude = -22.0### CHANGE WHEN IN PRODUCTION geolocation['coords']['latitude']
        longitude = 14.0### CHANGE WHEN IN PRODUCTION geolocation['coords']['longitude']

        uploaded_file = st.file_uploader("To help us understand your taste, upload your Netflix history", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            return df
    return None

def process_netflix_data(df):
    """
    Process Netflix data to filter and format it.
    """
    if df is not None:
        filter_words = ["Episode", "Season", "Seasons", "Chapter", "Series", "Part"]
        mask = df['Title'].str.contains('|'.join(filter_words), case=False, regex=True)
        return df[mask == False].to_dict(orient="records")
    return None

def display_scroll_down_message():
    """
    Display the "scroll down" message with a grey triangle pointing down.
    """
    st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the message
    st.markdown("<p style='text-align: center; font-size: 20px; color: #808080;'>Scroll down</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='50' height='50' fill='#808080'><path d='M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z'/><path fill='none' d='M0 0h24v24H0z'/></svg></div>", unsafe_allow_html=True)


def display_netflix_history(response):
    """
    Display Netflix history statistics.

    Parameters:
        response (dict): API response containing Netflix history statistics.
    """
    # Display centered title
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)  # Add some space before the message
    st.markdown("<h1 style='text-align: center;'>Your Netflix history in numbers</h1>", unsafe_allow_html=True)

    # Placeholder for film numbers and favorite director
    col1, col2 = st.columns([1, 1])  # Adjust the width ratio as needed
    col1.markdown("<br>", unsafe_allow_html=True)  # Add some space before the chart
    col1.markdown(f"<p style='font-size: 16px; color: black;'>You have watched</p>", unsafe_allow_html=True)
    col1.markdown(f"<p style='font-size: 48px; color: #83C9FF;'>{response['statistics']['total_films_count']} films</p>", unsafe_allow_html=True)

    col1.markdown(f"<p style='font-size: 16px; color: black;'>Your favourite film director is</p>", unsafe_allow_html=True)
    col1.markdown(f"<p style='font-size: 48px; color: #83C9FF;line-height: 45px;'>{list(response['statistics']['directors_count'].keys())[0]}</p>", unsafe_allow_html=True)

    # Display right-hand side horizontal bar chart
    col2.markdown("<br>", unsafe_allow_html=True)  # Add some space before the chart
    col2.markdown(f"<p style='font-size: 16px; color: black;'>Your favourite Genres</p>", unsafe_allow_html=True)
    genres_count = response['statistics']['genres_count']
    genres = list(genres_count.keys())[:5]  # Displaying only the first 5 genres for simplicity
    values = [genres_count[genre] for genre in genres]

    # Reverse the order of genres and values
    genres.reverse()
    values.reverse()

    # Define the color gradient for the bar chart
    colors = ['#1E90FF', '#4DAAEB', '#6FC3DF', '#83C9FF', '#D6ED17']  # Example gradient from yellow to blue

    fig = go.Figure(data=[go.Bar(
        x=values,
        y=genres,
        orientation='h',
        marker=dict(color=colors)
    )])

    fig.update_layout(
        plot_bgcolor='#EEEEEE',  # Set the background color of the plot
        paper_bgcolor='#EEEEEE',
        showlegend=False,
        title="",
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        width=250  # Adjust the width of the plot
    )

    col2.plotly_chart(fig)

def create_map(latitude, longitude, cinemas_info, width=800, height=400):
    # Title before map
    st.markdown("<h1 style='text-align: center;'>Two cinemas near your show films you will love!</h1>", unsafe_allow_html=True)

    # Create a map centered around the provided latitude and longitude with custom width and height
    m = folium.Map(location=[latitude, longitude], zoom_start=2, tiles=None, width=width, height=height)

    # Add the CartoDB Positron tile layer
    folium.TileLayer('cartodbpositron').add_to(m)

    # Add a marker for your location
    folium.Marker(location=[latitude, longitude], popup='Your Location',
                  icon=folium.Icon(color='red')).add_to(m)

    # Keep track of cinemas to avoid duplicates
    added_cinemas = set()

    # Add markers for each cinema
    for cinema in cinemas_info:
        cinema_key = (cinema['Cinema Latitude'], cinema['Cinema Longitude'])
        if cinema_key not in added_cinemas:
            folium.Marker(location=[cinema['Cinema Latitude'], cinema['Cinema Longitude']],
                          popup=cinema['Cinema Name']).add_to(m)
            added_cinemas.add(cinema_key)

    # Calculate bounds of all markers
    bounds = [[latitude, longitude]]
    for cinema in cinemas_info:
        bounds.append([cinema['Cinema Latitude'], cinema['Cinema Longitude']])

    # Fit map to bounds
    m.fit_bounds(bounds)

    # Display the map
    folium_static(m)


def show_films_in_cinemas(data):

    st.markdown(f"<p style='font-size: 24px; color: black;'>These films are showing tomorrow:</p>", unsafe_allow_html=True)

    # Keep track of films already visualized
    visualized_films = set()

    # Iterate over films and visualize the first 5 unique films
    for film in data["showings"]:
        # Check if the film has already been visualized
        if film['Film Name'] not in visualized_films:
            # Add film to the set of visualized films
            visualized_films.add(film['Film Name'])

            with open('style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            # Define layout
            left_column, right_column = st.columns([1, 3])

            # Display smaller image of the film on the left side
            left_column.image(film["Poster"], width=100)

            # Display other details on the right side
            right_column.metric(film['Film Director'], film['Film Name'])
            right_column.write(f"<span style='color: darkgrey'>{film['Film Genre']} ‧ {film['Film Rating']}</span>", unsafe_allow_html=True)
            right_column.write(f"<span style='color: darkgrey; margin-bottom: 10px'>{film['Film Duration']}</span>", unsafe_allow_html=True)

            # Add space between films
            st.markdown("<br>", unsafe_allow_html=True)

            # Display screening information for this film
            for screening in data["showings"]:
                if screening['Film Name'] == film['Film Name']:
                    # Display cinema name, address, distance aligned to left, with cinema name in a bigger font size and bold
                    cinema_name_html = f"<span style='font-size: 1.2em; margin-left: 100px;'>| {screening['Cinema Name']}</span> "
                    cinema_info_html = f"<span style='color: darkgrey; font-size: 0.8em;'>{screening.get('Cinema Address', '')} ‧ {screening['Cinema Distance']:.2f} meters</span>"
                    st.write(f"<div style='display: flex; justify-content: space-between;'>"
                                f"{cinema_name_html}{cinema_info_html}"
                                f"<div style='text-align: right;'>"
                                f"{screening['Start Time']}"
                                f"</div>"
                                f"</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)




            # Add space between films
            st.markdown("<br>", unsafe_allow_html=True)

        # Check if 5 unique films have been visualized
        if len(visualized_films) >= 5:
            break


def send_to_api(netflix_data, latitude, longitude):
    payload = {
        "location": {
            "lat": -22, ####### CHANGE WHEN IN PRODUCTION
            "lng": 14,
            "countrycode": "XX"
        },
        "cinemacount": 1,
        "netflix": netflix_data
    }

    #if payload["location"]["lat"] is not None:
    payload["location"]["lat"] = float(payload["location"]["lat"])
    #if payload["location"]["lng"] is not None:
    payload["location"]["lng"] = float(payload["location"]["lng"])

    response = requests.post(API_ENDPOINT, json=payload)

    if response.status_code == 200:
        pass
        #st.success("Data sent to API successfully!")
    else:
        st.error(f"Error sending data to API. Status code: {response.status_code}")

    return response.json()

if __name__ == "__main__":
    main()
