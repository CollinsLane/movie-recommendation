import streamlit as st
import pandas as pd
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="AI Movie Engine", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #05070a;
        color: #ffffff;
    }

    /* Selection Logic Header */
    .logic-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid #6366f1;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    /* Enhanced Movie Card */
    div[data-testid="stVerticalBlock"] div[style*="border"] {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
        padding: 0px !important; 
        overflow: hidden;
        transition: 0.3s ease;
    }

    .movie-info-container {
        padding: 15px;
    }

    /* Progress Bar for Match Score */
    .match-bar-bg {
        background: #1e293b;
        border-radius: 5px;
        height: 6px;
        width: 100%;
        margin-top: 8px;
    }
    .match-bar-fill {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        height: 6px;
        border-radius: 5px;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tweaking the expander UI to match the dark theme */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        color: #a855f7 !important;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA & HELPERS ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Title': ['The Dark Knight', 'Inception', 'Interstellar', 'Avengers: Endgame', 'John Wick', 'The Matrix', 'Dune', 'Blade Runner 2049'],
        'Image_URL': [
            'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg',
            'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg',
            'broken_url_test', # Intentionally broken to trigger the NO SIGNAL fail-safe
            'https://upload.wikimedia.org/wikipedia/en/8/8e/Dune_%282021_film%29_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/9b/Blade_Runner_2049_poster.png'
        ],
        'Genres': [['Action', 'Crime'], ['Action', 'Sci-Fi'], ['Sci-Fi', 'Adventure'], ['Action', 'Sci-Fi'], ['Action', 'Thriller'], ['Action', 'Sci-Fi'], ['Sci-Fi', 'Adventure'], ['Sci-Fi', 'Drama']],
        'Rating': [9.0, 8.8, 8.6, 8.4, 7.4, 8.7, 8.0, 8.1],
        'Description': [
            "Batman faces the Joker in Gotham.",
            "A thief steals secrets from dreams.",
            "Explorers travel through a wormhole.",
            "The Avengers assemble once more.",
            "An ex-hitman seeks vengeance.",
            "A hacker learns the true nature of reality.",
            "A noble family entangled in a war for spice.",
            "A blade runner unearths a long-buried secret."
        ]
    })

def render_poster(url):
    """Fallback handler: If image URL is dead, show a custom cyberpunk placeholder."""
    if pd.isna(url) or url == 'broken_url_test':
        st.image("https://via.placeholder.com/300x450/0f172a/6366f1?text=NO+SIGNAL", use_container_width=True)
    else:
        try:
            st.image(url, use_container_width=True)
        except Exception:
            st.image("https://via.placeholder.com/300x450/0f172a/6366f1?text=NO+SIGNAL", use_container_width=True)

df = load_data()
all_genres = sorted(list(set(g for sub in df['Genres'] for g in sub)))

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎛️ AI Parameters")
    st.markdown("Set the criteria the AI uses to rank the database.")
    
    search_query = st.text_input("🔍 Direct Title Search", placeholder="e.g., Dune...")
    st.divider()
    
    selected_genres = st.multiselect("1. Target Genres", all_genres, default=["Action", "Sci-Fi"])
    min_rating = st.slider("2. Quality Floor (Rating)", 5.0, 10.0, 7.0)
    
    st.divider()
    st.markdown("### 🛠️ Developer Info")
    st.caption("UI Optimized for High-Res Displays")
    st.caption("Build: 4.0.2-Alpha")

# --- 4. MAIN DASHBOARD ---
st.header("⚡ Neural Discovery Engine")

# --- 5. FILTER LOGIC & OVERRIDES ---
if search_query:
    # Override filters if the user is searching for a specific movie
    results = df[df['Title'].str.contains(search_query, case=False, na=False)].copy()
    max_possible = 1
    results['Match_Score'] = 1 
    results['Matches'] = results['Genres'] 
else:
    # Standard AI Math Logic
    df['Matches'] = df['Genres'].apply(lambda x: list(set(x).intersection(set(selected_genres))))
    df['Match_Score'] = df['Matches'].apply(lambda x: len(x))
    max_possible = len(selected_genres) if selected_genres else 1
    results = df[(df['Match_Score'] > 0) & (df['Rating'] >= min_rating)].sort_values(by=['Match_Score', 'Rating'], ascending=False)

# --- 6. TOP METRICS DASHBOARD ---
st.markdown("<br>", unsafe_allow_html=True)
col_m1, col_m2 = st.columns(2)
col_m1.metric(label="Total Databanks", value=len(df))
col_m2.metric(label="Matches Found", value=len(results), delta=f"-{len(df) - len(results)} filtered out", delta_color="inverse")
st.markdown("<br>", unsafe_allow_html=True)

# --- 7. DYNAMIC LOGIC EXPLAINER ---
if not search_query and selected_genres:
    st.markdown(f"""
    <div class="logic-box">
        <b>Selection Logic:</b> Highlighting movies with a <b>Rating ≥ {min_rating}</b> 
        that match at least one of these tags: <code>{', '.join(selected_genres)}</code>.
    </div>
    """, unsafe_allow_html=True)
elif search_query:
    st.markdown(f"""
    <div class="logic-box" style="border-color: #a855f7; background: rgba(168, 85, 247, 0.1);">
        <b>Override Active:</b> Searching directly for titles containing: <code>{search_query}</code>.
    </div>
    """, unsafe_allow_html=True)

# --- 8. GRID RENDERING ---
if not selected_genres and not search_query:
    st.info("👋 Select some genres or search a title in the sidebar to begin the analysis.")
elif results.empty:
    st.warning("⚠️ No movies found with that combination. Try lowering the Quality Floor or clearing your search.")
else:
    # Simulated processing delay for the "AI Engine" feel
    with st.spinner("Calibrating Neural Pathways..."):
        time.sleep(0.35) 
        
        cols = st.columns(4)
        for idx, (i, row) in enumerate(results.iterrows()):
            match_pct = min((row['Match_Score'] / max_possible) * 100, 100)
            
            with cols[idx % 4]:
                with st.container(border=True):
                    # Uses the fail-safe function instead of native st.image
                    render_poster(row['Image_URL'])
                    
                    # Content Area
                    st.markdown(f"""
                    <div class="movie-info-container">
                        <div style="font-weight:700; font-size:1.1rem; min-height:55px;">{row['Title']}</div>
                        <div style="display:flex; justify-content:space-between; margin-top:10px;">
                            <span class="stat-label">IMDb</span>
                            <span style="color:#fbbf24; font-weight:700;">★ {row['Rating']}</span>
                        </div>
                        <div style="margin-top:15px;">
                            <span class="stat-label">AI Match Score: {int(match_pct)}%</span>
                            <div class="match-bar-bg">
                                <div class="match-bar-fill" style="width: {match_pct}%;"></div>
                            </div>
                        </div>
                        <div style="margin-top:10px; font-size:0.7rem; color:#6366f1;">
                            Matched: {", ".join(row['Matches']) if row['Matches'] else "Direct Title Match"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Expandable Synopsis 
                    with st.expander("View Synopsis"):
                        st.write(row.get('Description', 'No synopsis available in databanks.'))
                        st.caption("Source: Neural Discovery Engine")
