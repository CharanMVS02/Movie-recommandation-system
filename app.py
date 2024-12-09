import streamlit as st
import pickle
import pandas as pd
import requests


# Fetch poster function
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e93990d2f63fa35f0bd58759247ca52d&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity1.pkl', 'rb'))

# Apply CSS for custom styling
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        text-align: center;
        background-color: #1a73e8;
        color: white;
        padding: 10px;
        margin-bottom: 20px;
        font-size: 35px;
        font-weight: bold;
    }
    .main-subtitle {
        text-align: center;
        font-size: 18px;
        color: #444444;
        margin-bottom: 40px;
    }
    .movie-card {
        text-align: center;
        padding: 10px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px;
    }
    .movie-title {
        font-size: 16px;
        margin-top: 10px;
        font-weight: bold;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        color: #666666;
        font-size: 14px;
    }
    .social-links img {
        width: 25px;
        margin: 0 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="main-header">🎥 Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Explore personalized movie recommendations!</div>', unsafe_allow_html=True)

# Sidebar with additional information
st.sidebar.header("About the App")
st.sidebar.write("""This application uses machine learning to recommend movies based on your selection. 
It leverages similarity metrics and integrates with The Movie Database (TMDb) API to fetch posters.
""")
st.sidebar.write("#### Key Features:")
st.sidebar.write(
    "- Movie similarity-based recommendations\n- TMDb API integration for posters\n- Interactive user interface")
st.sidebar.write("#### Contact Us:")
st.sidebar.write("Email: support@movierecommender.com")

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    "Select a movie from the list:",
    options=movies['title'].values,
    help="Type to filter movies or scroll to select."
)

# Recommendation button and display
if st.button('Get Recommendations'):
    if selected_movie_name:
        names, posters = recommend(selected_movie_name)

        st.markdown("## Recommendations for you:")
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                st.image(poster)
                st.markdown(f'<div class="movie-title">{name}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Please select a movie to get recommendations!")

# Footer with social links
st.markdown("""
    <div class="footer">
        Developed with ❤️ using Streamlit | Connect with us: 
        <span class="social-links">
            <a href="#"><img src="https://image.flaticon.com/icons/png/512/733/733547.png" alt="Twitter"></a>
            <a href="#"><img src="https://image.flaticon.com/icons/png/512/733/733558.png" alt="LinkedIn"></a>
            <a href="#"><img src="https://image.flaticon.com/icons/png/512/733/733579.png" alt="GitHub"></a>
        </span>
    </div>
""", unsafe_allow_html=True)
