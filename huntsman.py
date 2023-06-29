import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Creating new data frame
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')



st.markdown("<h4 style='color: grey'>How would you like to be Recommended?</h2>", unsafe_allow_html=True)
selected_movie_name = st.selectbox(
    "",
    movies['title'].values
)



# For hitting API requests is required and there we have function get
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=1204e2fcdcf14caab8db41fb04d09683&language=en-US'.format(
            movie_id))
    data = response.json()  # converting to json
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# For fetching recommended movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from api
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommend_movies_posters

# Changing background
import streamlit as st

def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.pexels.com/photos/3709370/pexels-photo-3709370.jpeg?auto=compress&cs=tinysrgb&w=600");
            background-attachment: fixed;
            background-size: cover;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0, 0, 0, 0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()


# Displaying poster and names
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols_row1 = st.columns(3)
    cols_row2 = st.columns(3)

    for i in range(3):
        with cols_row1[i]:
            st.image(posters[i], width=200)
            st.markdown(f"<span style='font-weight: bold; font-size: 18px;'>{names[i]}</span>", unsafe_allow_html=True)

    for i in range(3, 5):
        with cols_row2[i-3]:
            st.image(posters[i], width=200)
            st.markdown(f"<span style='font-weight: bold; font-size: 18px;'>{names[i]}</span>", unsafe_allow_html=True)
