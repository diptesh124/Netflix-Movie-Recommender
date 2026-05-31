import streamlit as st
import pickle
import pandas as pd
import requests
import os

# -----------------------------
# TMDB API Key
# -----------------------------
TMDB_API_KEY = "YOUR_TMDB_API_KEY"

# -----------------------------
# Load Files
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, "model", "movie_list.pkl")
similarity_path = os.path.join(BASE_DIR, "model", "similarity.pkl")

movies_dict = pickle.load(open(movies_path, "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(similarity_path, "rb"))

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Netflix Movie Recommender",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #141414;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
}

.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: white;
    margin-top: 5px;
    text-align: center;
}

.rating {
    color: #46d369;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Fetch Poster & Rating
# -----------------------------
@st.cache_data
def fetch_movie_details(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return (
                "https://via.placeholder.com/300x450?text=No+Image",
                "N/A"
            )

        data = response.json()

        poster_path = data.get("poster_path")
        rating = data.get("vote_average", "N/A")

        if poster_path:
            poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster = "https://via.placeholder.com/300x450?text=No+Image"

        return poster, rating

    except Exception:
        return (
            "https://via.placeholder.com/300x450?text=No+Image",
            "N/A"
        )

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie_name):

    movie_name = movie_name.strip().lower()

    # Partial Search (case-insensitive)
    matches = movies[
        movies["title"].str.lower().str.contains(
            movie_name,
            na=False
        )
    ]

    if matches.empty:
        return None, None

    # First matching movie
    selected_movie_index = matches.index[0]

    selected_movie_title = movies.iloc[selected_movie_index]["title"]

    distances = similarity[selected_movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommendations = []

    for movie in movie_list:

        movie_index = movie[0]

        movie_id = movies.iloc[movie_index]["movie_id"]
        title = movies.iloc[movie_index]["title"]

        poster, rating = fetch_movie_details(movie_id)

        recommendations.append({
            "title": title,
            "poster": poster,
            "rating": rating
        })

    return recommendations, selected_movie_title

# -----------------------------
# UI
# -----------------------------
st.markdown(
    "<h1>🎬 Netflix Movie Recommender</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "#### Search movies like Netflix recommendations"
)

selected_movie = st.text_input(
    "🔎 Search Movie",
    placeholder="Type movie name (e.g. avatar, batman, avengers)"
)

if st.button("Show Recommendations 🎥"):

    if not selected_movie.strip():

        st.warning("Please enter a movie name.")

    else:

        recommendations, matched_movie = recommend(selected_movie)

        if recommendations is None:

            st.error("No matching movie found.")

        else:

            st.success(f"Showing recommendations for: {matched_movie}")

            st.markdown("## 🍿 Recommended For You")

            cols = st.columns(5)

            for i, movie in enumerate(recommendations):

                with cols[i % 5]:

                    st.image(
                        movie["poster"],
                        use_container_width=True
                    )

                    st.markdown(
                        f"""
                        <div class='movie-title'>
                            {movie['title']}
                        </div>

                        <div class='rating'>
                            ⭐ {movie['rating']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

