import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY')}&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None

def recommend(movie, movies, similarity):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster_path = fetch_poster(movie_id)
            if poster_path:
                recommended_movie_posters.append(poster_path)
                recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return [], []

def main():
    st.header('Movie Recommender System')

    try:
        movies = pickle.load(open('model/movie_list.pkl', 'rb'))
        similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
        if recommended_movie_names:
            cols = st.columns(5)
            for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
                with col:
                    st.text(name)
                    st.image(poster)

if __name__ == '__main__':
    main()
