import streamlit as st
import joblib
import requests
import os
from dotenv import load_dotenv
import time  # for demo delay (optional)

st.title("🎬 Movie Recommender System")

# --- Load environment variables ---
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please check your .env file.")

# --- Load model ---
model = joblib.load("model.pkl")
data = model["data"]
similarity = model["similarity"]

# --- Function to fetch poster from TMDB using movie_id ---
def fetch_poster(movie_id):
    """Fetch movie poster URL from TMDB API using movie_id"""
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/300x450?text=No+API+Key"

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        poster_path = movie_data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=No+Image"

# --- Recommendation logic ---
def recommend(movie):
    """Return list of (title, poster_url) for 5 similar movies"""
    try:
        movie_index = data[data["title"] == movie].index[0]
    except IndexError:
        st.error("Movie not found in database!")
        return []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    for i in movie_list:
        movie_title = data.iloc[i[0]]["title"]
        movie_id = data.iloc[i[0]]["movie_id"]
        poster = fetch_poster(movie_id)
        recommendations.append((movie_title, poster))

    return recommendations

# --- Movie selection dropdown ---
movie_name = st.selectbox(
    "🎞️ Select a movie:",
    data["title"].values,
    index=None,
    placeholder="Select..."
)

# --- Show recommendations when button clicked ---
if st.button("Recommend"):
    if movie_name:
        st.subheader("Recommended Movies:")
        # --- Add loading spinner ---
        with st.spinner("Generating recommendations 🎬"):
            recommendations = recommend(movie_name)
            time.sleep(1)  # optional small delay to show spinner nicely
        if recommendations:
            cols = st.columns(5)
            for i, (title, poster) in enumerate(recommendations):
                with cols[i]:
                    st.image(poster, use_container_width=True)
                    st.caption(title)
        else:
            st.info("No recommendations found.")
    else:
        st.warning("Please select a movie first!")


