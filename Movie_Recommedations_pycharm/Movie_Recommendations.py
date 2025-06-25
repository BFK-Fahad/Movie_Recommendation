import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie data and similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie_data = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8723e98ff0ec34f15e1c14d273de15be')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movie_data[movie_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # Use the correct column name 'id' instead of 'movie_id'
        movie_id = movie_data.iloc[i[0]]['id']  # Updated to use 'id'
        recommended_movies.append(movie_data.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit app
st.title('Movie Recommendation')

selected_movie = st.selectbox('Choose a movie to get recommendations:', movie_data['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
