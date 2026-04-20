import streamlit as st
import pandas as pd
import time

# --- 1. UI CONFIGURATION & GLASS-MORPHIC THEME ---
st.set_page_config(page_title="Cinema AI | Premium", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f8fafc;
    }

    /* Glassmorphic Card Style */
    div[data-testid="stVerticalBlock"] div[style*="border"] {
        background: rgba(30, 41, 59, 0.5) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 20px;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
        transform: scale(1.02);
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }

    /* Hero Section */
    .hero-container {
        padding: 50px 0px;
        text-align: center;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(to right, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Text Styling */
    .movie-title { font-size: 1.4rem; font-weight: 700; color: #ffffff; margin: 10px 0 5px 0; }
    .movie-rating { color: #fbbf24; font-weight: 600; font-size: 1rem; }
    .badge {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 5px;
    }

    /* Sidebar Tweaks */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data
def get_data():
    api_data = {
        'Title': ['The Dark Knight', 'Inception', 'Interstellar', 'Avengers: Endgame', 'John Wick', 'La La Land', 'The Terminator', 'Gladiator', 'The Conjuring', 'Superbad', 'Dune', 'Blade Runner 2049'],
        'Image_URL': [
            'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg',
            'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/a/ab/La_La_Land_%28film%29.png',
            'https://upload.wikimedia.org/wikipedia/en/7/70/Terminator1984movieposter.jpg',
            'https://upload.wikimedia.org/wikipedia/en/f/fb/Gladiator_%282000_film_poster%29.png',
            'https://upload.wikimedia.org/wikipedia/en/1/1f/Conjuring_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/8/8b/Superbad_Poster.png',
            'https://upload.wikimedia.org/wikipedia/en/8/8e/Dune_%282021_film%29_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/9b/Blade_Runner_2049_poster.png'
        ],
        'Genres': [['Action', 'Crime', 'Drama'], ['Action', 'Sci-Fi'], ['Sci-Fi', 'Adventure'], ['Action', 'Sci-Fi'], ['Action', 'Thriller'], ['Romance', 'Musical'], ['Action', 'Sci-Fi'], ['Action', 'Drama'], ['Horror', 'Thriller'], ['Comedy'], ['Sci-Fi', 'Adventure'], ['Sci-Fi', 'Drama']],
        'Rating': [9.0, 8.8, 8.6, 8.4, 7.4, 8.0, 8.1, 8.5, 7.5, 7.6, 8.0, 8.0],
        'Description': ["Gotham's savior vs the agent of chaos.", "Dream infiltration at the highest stakes.", "A journey beyond time to save our species.", "The final stand against the mad titan.", "Don't touch the dog. Don't touch the car.", "A melody of dreams in the city of stars.", "A relentless machine from the future.", "A general who became a slave to conquer an empire.", "The true files of the Warrens.", "One night. Three friends. Zero sobriety.", "A noble family entangled in a war for spice.", "A new blade runner unearths a long-buried secret."]
    }
    return pd.DataFrame(api_data)

df = get_data()
all_genres = sorted(list(set(g for sub in df['Genres'] for g in sub)))

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#818cf8;'>Settings</h2>", unsafe_allow_html=True)
    selected_genres = st.multiselect("Pick Your Vibes", all_genres, default=["Sci-Fi", "Action"])
    min_rating = st.slider("Quality Threshold", 5.0, 10.0, 7.5)
    
    st.markdown("---")
    st.markdown("### 🟢 System Status")
    st.caption("Engine: Neuro-Link v2.4")
    st.caption("Latency: 14ms")
    st.info("Personalized for your friend")

# --- 4. MAIN CONTENT ---
st.markdown("""
    <div class="hero-container">
        <p class="hero-subtitle">Next-Gen Discovery</p>
        <h1 class="hero-title">Cinema AI Pro</h1>
    </div>
""", unsafe_allow_html=True)

# Filter Logic
df['Match_Count'] = df['Genres'].apply(lambda x: len(set(x).intersection(set(selected_genres))))
results = df[(df['Match_Count'] > 0) & (df['Rating'] >= min_rating)].sort_values(by='Rating', ascending=False)

if results.empty:
    st.info("✨ No matches found. Try adjusting the quality threshold or genres!")
else:
    cols = st.columns(3)
    for idx, (i, row) in enumerate(results.iterrows()):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(row['Image_URL'], use_container_width=True)
                
                # Title & Rating
                st.markdown(f"<div class='movie-title'>{row['Title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-rating'>★ {row['Rating']}</div>", unsafe_allow_html=True)
                
                # Genre Badges
                badge_html = "".join([f"<span class='badge'>{g}</span>" for g in row['Genres']])
                st.markdown(f"<div style='margin-bottom: 15px;'>{badge_html}</div>", unsafe_allow_html=True)
                
                st.write(f"_{row['Description']}_")
                st.divider()
                st.caption(f"Confidence: {row['Match_Count'] * 33}% Match")
