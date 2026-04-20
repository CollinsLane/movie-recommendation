import streamlit as st
import pandas as pd
import time

# ==================== 1. PAGE CONFIG & STYLING ====================
st.set_page_config(
    page_title="AI Movie Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #05070a 0%, #0a0f1c 100%);
        color: #ffffff;
    }
    
    /* Movie Card - Premium Look */
    div[data-testid="stVerticalBlock"] div[style*="border"] {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 20px !important;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
        transform: translateY(-8px) scale(1.03);
        border-color: #6366f1 !important;
        box-shadow: 0 25px 50px -12px rgb(99 102 241 / 0.25);
    }
    
    .movie-info-container { padding: 20px; }
    
    .match-bar-bg {
        background: #1e293b;
        border-radius: 9999px;
        height: 8px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
    }
    .match-bar-fill {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        height: 100%;
        border-radius: 9999px;
        transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05070a 0%, #0f122b 100%) !important;
        border-right: 2px solid rgba(168, 85, 247, 0.4) !important;
        box-shadow: 8px 0 30px rgba(168, 85, 247, 0.15);
    }
    
    /* Logic Box */
    .logic-box {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# ==================== 2. DATA LOADER ====================
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Title': ['The Dark Knight', 'Inception', 'Interstellar', 'Avengers: Endgame', 'John Wick', 
                 'The Matrix', 'Dune', 'Blade Runner 2049', 'Oppenheimer', 'Dune: Part Two'],
        'Image_URL': [
            'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg',
            'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg',
            'broken_url_test',
            'https://upload.wikimedia.org/wikipedia/en/8/8e/Dune_%282021_film%29_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/9b/Blade_Runner_2049_poster.png',
            'https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/5/5e/Dune_Part_Two_poster.jpg'
        ],
        'Genres': [
            ['Action', 'Crime'], ['Action', 'Sci-Fi'], ['Sci-Fi', 'Adventure'],
            ['Action', 'Sci-Fi'], ['Action', 'Thriller'], ['Action', 'Sci-Fi'],
            ['Sci-Fi', 'Adventure'], ['Sci-Fi', 'Drama'], ['Biography', 'Drama'],
            ['Sci-Fi', 'Adventure']
        ],
        'Rating': [9.0, 8.8, 8.6, 8.4, 7.4, 8.7, 8.0, 8.1, 8.9, 8.8],
        'Description': [
            "Batman faces the Joker in Gotham.",
            "A thief steals secrets from dreams.",
            "Explorers travel through a wormhole.",
            "The Avengers assemble once more.",
            "An ex-hitman seeks vengeance.",
            "A hacker learns the true nature of reality.",
            "A noble family entangled in a war for spice.",
            "A blade runner unearths a long-buried secret.",
            "The story of J. Robert Oppenheimer and the atomic bomb.",
            "Paul Atreides unites the desert people of Arrakis."
        ]
    })

# ==================== 3. HELPERS ====================
def render_poster(url):
    if pd.isna(url) or url == 'broken_url_test':
        st.image("https://via.placeholder.com/300x450/0f172a/6366f1?text=NO+SIGNAL", use_container_width=True)
    else:
        try:
            st.image(url, use_container_width=True)
        except Exception:
            st.image("https://via.placeholder.com/300x450/0f172a/6366f1?text=NO+SIGNAL", use_container_width=True)

def calculate_matches(df, selected_genres, min_rating, search_query):
    """Core neural engine logic - clean & reusable"""
    if search_query:
        results = df[df['Title'].str.contains(search_query, case=False, na=False)].copy()
        if not results.empty:
            results = results.sort_values(by='Rating', ascending=False)
            results['Match_Score'] = 100
            results['Matches'] = results['Title'].apply(lambda x: ["Direct Title Match"])
        else:
            results = pd.DataFrame()
        max_possible = 100
        return results, max_possible
    
    # Genre + Rating filtering
    if not selected_genres:
        return pd.DataFrame(), 0
    
    df_copy = df.copy()
    df_copy['Matches'] = df_copy['Genres'].apply(lambda x: list(set(x) & set(selected_genres)))
    df_copy['Match_Score'] = df_copy['Matches'].apply(len)
    max_possible = len(selected_genres)
    
    results = df_copy[
        (df_copy['Match_Score'] > 0) & 
        (df_copy['Rating'] >= min_rating)
    ].sort_values(by=['Match_Score', 'Rating'], ascending=False)
    
    return results, max_possible

def render_movie_card(row, max_possible):
    """Renders a single premium movie card"""
    match_pct = min((row['Match_Score'] / max_possible) * 100, 100) if max_possible > 0 else 100
    
    with st.container(border=True):
        render_poster(row['Image_URL'])
        
        st.markdown(f"""
        <div class="movie-info-container">
            <div style="font-weight:700; font-size:1.15rem; min-height:62px; line-height:1.3;">
                {row['Title']}
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-top:12px;">
                <span class="stat-label">IMDb</span>
                <span style="color:#fbbf24; font-weight:700; font-size:1.1rem;">★ {row['Rating']}</span>
            </div>
            
            <div style="margin-top:18px;">
                <span class="stat-label">AI MATCH SCORE • {int(match_pct)}%</span>
                <div class="match-bar-bg">
                    <div class="match-bar-fill" style="width: {match_pct}%;"></div>
                </div>
            </div>
            
            <div style="margin-top:12px; font-size:0.8rem; color:#6366f1; font-weight:500;">
                Matched: {", ".join(row['Matches'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.popover("📖 View Synopsis", use_container_width=True):
            st.markdown(f"**{row['Title']}**")
            st.write(row.get('Description', 'No synopsis available.'))
            st.caption("🔬 Powered by Neural Discovery Engine")

# ==================== 4. LOAD DATA ====================
df = load_data()
all_genres = sorted(list(set(g for sub in df['Genres'] for g in sub)))

# ==================== 5. SIDEBAR ====================
with st.sidebar:
    st.title("🎛️ Neural Controls")
    st.markdown("---")
    
    search_query = st.text_input("🔍 Direct Title Search", placeholder="e.g., Dune...")
    st.divider()
    
    st.markdown("**🎯 Target Genres**")
    selected_genres = st.pills(
        "Select tags below:",
        options=all_genres,
        selection_mode="multi",
        default=["Action", "Sci-Fi"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    min_rating = st.slider("⭐ Quality Floor", 5.0, 10.0, 7.0, 0.1)
    
    st.divider()
    
    # Student Info
    st.markdown("### 👨‍💻 Student Details")
    st.caption("**Name:** Mark Elvis Chiemezuo")
    st.caption("**Reg No:** 20231409352")
    st.caption("**Alias:** errorHQ")
    st.caption("**Level:** 300L Cybersecurity")
    
    st.divider()
    
    st.markdown("### 🧠 How The Engine Works")
    st.info(
        "**Neural Match Engine** works in 3 stages:\n\n"
        "1️⃣ **Filter** – Removes anything below your Quality Floor\n"
        "2️⃣ **Match** – Calculates % of your selected genres present\n"
        "3️⃣ **Rank** – Sorts by Match Score → IMDb Rating"
    )

# ==================== 6. MAIN APP ====================
st.header("⚡ Neural Discovery Engine")
st.markdown("**Real-time AI-powered movie recommendations**")

# Calculate results
results, max_possible = calculate_matches(df, selected_genres, min_rating, search_query)

# Metrics
col_m1, col_m2 = st.columns(2)
col_m1.metric("📊 Total Databanks", len(df))
col_m2.metric(
    "🔥 Matches Found", 
    len(results), 
    delta=f"-{len(df) - len(results)} filtered" if len(results) < len(df) else None,
    delta_color="inverse"
)

# Logic Explainer
if search_query:
    st.markdown(f"""
    <div class="logic-box" style="border-color:#a855f7; background:rgba(168,85,247,0.1);">
        <b>🔥 DIRECT SEARCH OVERRIDE ACTIVE</b><br>
        Showing results for: <code>{search_query}</code>
    </div>
    """, unsafe_allow_html=True)
elif selected_genres:
    st.markdown(f"""
    <div class="logic-box">
        <b>Selection Logic:</b> Movies with <b>Rating ≥ {min_rating}</b> 
        that contain at least one of: <code>{', '.join(selected_genres)}</code>
    </div>
    """, unsafe_allow_html=True)

# Render Results
if not (selected_genres or search_query):
    st.info("👋 Select genres in the sidebar or search a title to activate the Neural Engine.")
elif results.empty:
    st.warning("⚠️ No matches found. Try lowering the quality floor or broadening your genres.")
else:
    with st.spinner("Calibrating neural pathways..."):
        time.sleep(0.4)
        
        cols = st.columns(4)
        for idx, (_, row) in enumerate(results.iterrows()):
            with cols[idx % 4]:
                render_movie_card(row, max_possible)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.8rem;'>"
    "🧬 AI Movie Engine • Built as Final Year Project • errorHQ © 2026"
    "</p>",
    unsafe_allow_html=True
)
