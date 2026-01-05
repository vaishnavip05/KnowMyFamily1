import streamlit as st
import json
import os

# Import setup and game modules
from setup.family_setup import family_setup_screen
from games.meet_my_family import meet_my_family_screen
from games.find_my_family import find_my_family_screen
from games.who_is_speaking import who_is_speaking_screen

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Know My Family",
    layout="wide"
)
st.markdown("""
<style>
    /* Full app background */
    body {
        background-color: #8a5082;
    }

    /* Streamlit app container */
    .stApp {
        background-color: #8a5082;
    }
</style>
""", unsafe_allow_html=True)

# ================= UI ENHANCEMENT ONLY =================
st.markdown("""
<style>
    .main {
        background-color: #6f5f90;
    }
    h1 {
        text-align: center;
        color: #3b3b3b;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        height: 100%;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .parent-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)
# =======================================================

DATA_FILE = "data/family_data.json"

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "setup"

# --------------------------------------------------
# Helper: Check if family data exists
# --------------------------------------------------
def is_setup_complete():
    if not os.path.exists(DATA_FILE):
        return False
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return len(data) > 0
    except:
        return False

# --------------------------------------------------
# Navigation Helper (CORRECT)
# --------------------------------------------------
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()   # ✅ Force UI refresh

# --------------------------------------------------
# HOME SCREEN (AFTER SETUP)
# --------------------------------------------------
def home_screen():

    st.markdown("<h1>Know My Family 💙</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Learn your family through simple and friendly games</div>",
        unsafe_allow_html=True
    )

    # ---- Parent option to edit setup ----
    st.markdown("<div class='parent-box'>", unsafe_allow_html=True)
    st.markdown("### 👨‍👩‍👧 Parent Options")
    if st.button("✏️ Edit Family Setup"):
        go_to("setup")
        return
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🎮 Games")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👨‍👩‍👧 Meet My Family")
        st.write("Learn names and relationships with pictures.")
        if st.button("▶ Play", key="meet_family"):
            go_to("meet_my_family")
            return
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🛤️ Find My Family")
        st.write("Guide the child through paths to reach family members.")
        if st.button("▶ Play", key="find_family"):
            go_to("find_my_family")
            return
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔊 Who Is Speaking?")
        st.write("Listen carefully and identify whose voice it is.")
        if st.button("▶ Play", key="who_speaking"):
            go_to("who_is_speaking")
            return
        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# MAIN APP FLOW
# --------------------------------------------------
if st.session_state.page == "setup":
    family_setup_screen(go_to)

elif not is_setup_complete():
    st.session_state.page = "setup"
    st.rerun()

elif st.session_state.page == "home":
    home_screen()

elif st.session_state.page == "meet_my_family":
    meet_my_family_screen(go_to)

elif st.session_state.page == "find_my_family":
    find_my_family_screen(go_to)

elif st.session_state.page == "who_is_speaking":
    who_is_speaking_screen(go_to)
