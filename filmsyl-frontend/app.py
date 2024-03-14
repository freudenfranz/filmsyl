"""
Frontend for 'films you like'
"""
import os
import time
import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from streamlit_js_eval import get_geolocation
import folium
from streamlit_folium import folium_static

API_ENDPOINT = "https://films-you-like-dev-2h7mcggcwa-ew.a.run.app/get-recommendations"
#API_ENDPOINT= "http://127.0.0.1:8000/get-recommendations"


def main():
    # Display centered title
    display_title()

    # Get and display geolocation
    latitude, longitude = get_and_display_geolocation()
    if not latitude or not longitude:
        latitude = -22
        longitude = 14
        countrycode= "XX"
    else:
        #latitude = 52.5092312
        #longitude = 13.3735304
        countrycode = "DE"

    # Upload Netflix history
    df = upload_netflix_history(latitude, longitude)

    # Process Netflix data
    netflix_data = process_netflix_data(df)

    if netflix_data:
        # Display a spinner while waiting for the API response
        st.markdown("<br><br><br>", unsafe_allow_html=True)  # Add some space before the spinner
        with st.spinner("We are trying to understand your weird taste..."):
            # Send data to API and get response
            response = send_to_api(netflix_data, latitude, longitude, countrycode)

        # Load JSON file
        #with open('combined_output.json', 'r') as f:
        #    response = json.load(f)

        # Display "scroll down" message
        #display_scroll_down_message()

        # Display "scroll down" message
        display_scroll_down_message()
        # Display Netflix history
        display_netflix_history(response)
        # Display "scroll down" message again
        st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the message
        display_scroll_down_message()

        cinemas_info = response["showings"] #data should be the json received from the api, currently we have 'repsonse' which is a

        # Create the map
        create_map(latitude, longitude, cinemas_info)

        # Show films in cinemas
        show_films_in_cinemas(response)

        #display_movies_recommendations()
        display_movies_recommendations(response['recommendations'])

def display_title():
    """
    Display the centered title for the app.
    """
    st.markdown("<h1 style='text-align: center;'>Ready to find films you like screening near you?</h1>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: #808080; '>Upload your Netflix history and select your cinema or home viewing.</h6>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the message

def get_and_display_geolocation():
    """
    Get geolocation and display warning if not available.
    """
    geolocation = get_geolocation()
    if geolocation:
        latitude = geolocation['coords']['latitude']
        longitude = geolocation['coords']['longitude']
        return latitude, longitude
    else:
        time.sleep(5)  # Adjust the delay time as needed
        st.warning("Please allow geolocation for this app to work")
        st.warning("If geolocation is not allowed we will use a testlocation")
        return None, None

def upload_netflix_history(latitude, longitude):
    """
    Allow the user to upload their Netflix history and process the data.
    """
    if latitude and longitude:

        uploaded_file = st.file_uploader("To help us understand your taste, upload your Netflix history below:", type=['csv'])

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
    #st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the message
    st.markdown("<p style='text-align: center; font-size: 20px; color: #808080;'>Scroll down</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='50' height='50' fill='#808080'><path d='M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z'/><path fill='none' d='M0 0h24v24H0z'/></svg></div>", unsafe_allow_html=True)

def display_netflix_history(response):
    """
    Display Netflix history statistics.

    Parameters:
        response (dict): API response containing Netflix history statistics.
    """
    if not response or ('statistics' not in response.keys()) :
        return
    # Display centered title
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)  # Add some space before the message
    st.markdown("<h1 style='text-align: center;'>Your Netflix history in numbers</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the message

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

def display_movies_recommendations(recommendations:dict):
    try:
        if recommendations:
            # Initialize lists to store movie information
            titles = []
            genres = []
            directors = []
            durations = []
            ratings = []

            # Extract movie information
            for movie in recommendations:
                titles.append(movie.get('primaryTitle', ''))
                genre_str = movie.get('genres', '')
                genre_list = [genre.strip() for genre in genre_str.split(',')]
                genres.append(', '.join(genre_list))
                directors.append(movie.get('Director', ''))
                durations.append(f"{movie.get('runtimeMinutes', '')} minutes")
                rating = movie.get('averageRating', '')
                rating_emoji = '★'
                ratings.append(f"{rating} {rating_emoji}")

            # Create DataFrame for all movie recommendations
            df = pd.DataFrame({
                "Movie title": titles,
                "Genre": genres,
                "Director": directors,
                "Duration": durations,
                "Rating": ratings
            })

            # Adjust index to start from 1
            df.index += 1

            # Apply CSS to fill the background color of the first row of headers with blue
            styles = [
                dict(selector="th", props=[("font-size", "120%"),
                                            ("text-align", "center")]),
                dict(selector="thead tr th", props=[("background-color", "gray"),  # Apply to the first row of headers
                                                     ("color", "white")])
            ]

            # Display the DataFrame as a single table
            st.markdown("<h1 style='text-align: center;'>Prefer the couch over the cinema?</h1>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center;'>Enjoy these recommended films from the comfort of home!</h4>", unsafe_allow_html=True)
            st.table(df.style.set_table_styles(styles))
        else:
            st.error("No movie recommendations found in the data.")
    except FileNotFoundError:
        st.error("File 'combined_output.json' not found.")

def create_map(latitude, longitude, cinemas_info, width=800, height=400):
    # Title before map
    st.markdown("<h1 style='text-align: center;'>Two cinemas near your show films you will love!</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Create a map centered around the provided latitude and longitude with custom width and height
    m = folium.Map(location=[latitude, longitude], zoom_start=1, tiles=None, width=width, height=height)

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

def show_films_in_cinemas1(data):
    """
    Show films of movies located closeby to browsers location
    """
    star = '\u2605'  # Unicode character for a star

    st.markdown("<p style='font-size: 24px; color: black;'>These films are showing tomorrow:</p>",
                unsafe_allow_html=True)

    # Keep track of films already visualized
    visualized_films = set()

    # Iterate over films and visualize the first 5 unique films
    for film in data["showings"]:

        # Check if the film has already been visualized
        if film['Film Name'] not in visualized_films:
            # Add film to the set of visualized films
            visualized_films.add(film['Film Name'])
            filedir = os.path.dirname(os.path.abspath(__file__))

            with open(os.path.join(filedir,'style.css'), encoding="utf-8") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            # Define layout
            left_column, right_column = st.columns([1, 3])

            # Display smaller image of the film on the left side
            if "Poster" in film.keys() and film["Poster"]:
                left_column.image(film["Poster"], width=100)

            # Display other details on the right side
            if ('Film Director'in film.keys()) and ('Film Name'in film.keys()):
                right_column.write(f"<span style='color: darkgrey'>{film['Film Genre']}  ‧  {film['Film Rating']} {star}</span>",
                               unsafe_allow_html=True)
            if 'Film Duration' in film.keys():
                right_column.write(f"<span style='color: darkgrey; margin-bottom: 10px'>{film['Film Duration']} minutes</span>",
                               unsafe_allow_html=True)

            # Add space between films
            st.markdown("<br>", unsafe_allow_html=True)

            if 'showings' in data.keys():
                # Display screening information for this film
                for screening in data["showings"]:
                    if ('Film Name' in screening.keys()) and ('Cinema Name' in screening.keys()) and ('Cinema Address' in screening.keys()) and ('Cinema Distance'in screening.keys()):
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

def show_films_in_cinemas(data):
    """
    Show films of movies located closeby to browsers location
    """
    star = '\u2605'  # Unicode character for a star
    st.markdown("<p style='font-size: 24px; color: black;'>These films are showing tomorrow:</p>",
                unsafe_allow_html=True)

    # Keep track of films already visualized
    visualized_films = set()

    # Iterate over films and visualize the first 5 unique films
    for film in data.get("showings", []):  # Handle incomplete or missing data["showings"]
        if not film:
            pass

        # Check if the film has already been visualized
        if film.get('Film Name') not in visualized_films:  # Use .get() to handle missing keys
            # Add film to the set of visualized films
            visualized_films.add(film.get('Film Name'))

            filedir = os.path.dirname(os.path.abspath(__file__))

            with open(os.path.join(filedir,'style.css'), encoding="utf-8") as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            # Define layout
            left_column, right_column = st.columns([1, 3])

            # Display smaller image of the film on the left side
            if film.get("Poster"):
                left_column.image(film.get("Poster"), width=100)


            # Display other details on the right side
            if film.get('Film Genre') and film.get('Film Rating'):
                right_column.metric(film['Film Director'], film['Film Name'])
                right_column.write(f"<span style='color: darkgrey'>{film['Film Genre']}  ‧  {film['Film Rating']} {star}</span>",
                                   unsafe_allow_html=True)
            if film.get('Film Duration'):
                right_column.write(f"<span style='color: darkgrey; margin-bottom: 10px'>{film['Film Duration']} minutes</span>",
                                   unsafe_allow_html=True)

            # Add space between films
            st.markdown("<br>", unsafe_allow_html=True)

            # Display screening information for this film
            for screening in data.get("showings", []):  # Handle incomplete or missing data["showings"]
                if screening.get('Film Name') == film.get('Film Name') and all(screening.get(key) for key in ('Cinema Name', 'Cinema Address', 'Cinema Distance', 'Start Time')):
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

def send_to_api(netflix_data, latitude:float, longitude:float, countrycode):
    """
    Send data to backend
    """
    payload = {
        "location": {
            "lat": latitude,
            "lng": longitude,
            "countrycode": countrycode
        },
        "cinemacount": 1,
        "netflix": netflix_data
    }

    print(f"Frontend: using payload {payload}")
    #if payload["location"]["lat"] is not None:
    payload["location"]["lat"] = float(payload["location"]["lat"])
    payload["location"]["lng"] = float(payload["location"]["lng"])

    response = requests.post(API_ENDPOINT, json=payload, timeout=160)

    if response.status_code == 200:
        #st.write(response.json())
        pass
        #st.success("Data sent to API successfully!")
    else:
        st.error(f"Error sending data to API. Status code: {response.status_code}")

    return response.json()

if __name__ == "__main__":
    main()
