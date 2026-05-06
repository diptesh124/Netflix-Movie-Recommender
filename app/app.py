import streamlit as st
import pickle
import pandas as pd
import requests
import os


TMDB_API_KEY = "46cc085d386d0cb9bb079a3188abc7b3"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, "model", "movie_list.pkl")
similarity_path = os.path.join(BASE_DIR, "model", "similarity.pkl")

movies_dict = pickle.load(open(movies_path, 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(similarity_path, 'rb'))

st.set_page_config(page_title="Netflix Movie Recommender", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #141414;
        color: white;
    }
    h1, h2, h3 {
        color: #E50914;
    }
    .movie-card {
        padding: 10px;
        border-radius: 10px;
        transition: 0.3s;
    }
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        color: white;
        margin-top: 5px;
    }
    .rating {
        color: #46d369;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)



@st.cache_data
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path", None)
        rating = data.get("vote_average", "N/A")

        if poster_path:
            poster = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster = "https://via.placeholder.com/300x450?text=No+Image"

        return poster, rating

    except:
        return "https://via.placeholder.com/300x450?text=No+Image", "N/A"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        title = movies.iloc[i[0]].title
        poster, rating = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)

    return recommended_movies, recommended_posters, recommended_ratings



st.markdown("<h1>🎬 Netflix Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("#### Find movies like Netflix recommendations")

selected_movie = st.text_input("🔎 Search for a movie")

if st.button("Show Recommendations 🎥"):

    if selected_movie == "":
        st.warning("Please enter a movie name")
    else:
        try:
            names, posters, ratings = recommend(selected_movie)

            st.markdown("## 🍿 Recommended for You")

            # Netflix-style rows (3 rows × 3 cards feel)
            cols = st.columns(5)

            for i in range(10):

                with cols[i % 5]:
                    st.image(posters[i], use_container_width=True)

                    st.markdown(f"""
                        <div style='text-align:center'>
                            <p class='movie-title'>{names[i]}</p>
                            <p class='rating'>⭐ {ratings[i]}</p>
                        </div>
                    """, unsafe_allow_html=True)

        except:
            st.error("Movie not found. Try another title.")