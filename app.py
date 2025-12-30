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
# Navigation Helper
# --------------------------------------------------
def go_to(page_name):
    st.session_state.page = page_name

# --------------------------------------------------
# HOME SCREEN (AFTER SETUP)
# --------------------------------------------------
def home_screen():
    st.title("Know My Family")
    st.write("Learn your family through simple and friendly games 💙")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👨‍👩‍👧 Meet My Family")
        st.write("Learn names and relationships")
        if st.button("Play", key="meet_family"):
            go_to("meet_my_family")

    with col2:
        st.subheader("🛤️ Find My Family")
        st.write("Follow the path to the right person")
        if st.button("Play", key="find_family"):
            go_to("find_my_family")

    with col3:
        st.subheader("🔊 Who Is Speaking?")
        st.write("Match voices to family members")
        if st.button("Play", key="who_speaking"):
            go_to("who_is_speaking")

# --------------------------------------------------
# MAIN APP FLOW
# --------------------------------------------------
if not is_setup_complete():
    # Parent must complete setup first
    family_setup_screen(go_to)

else:
    # After setup is done
    if st.session_state.page == "setup":
        go_to("home")

    if st.session_state.page == "home":
        home_screen()

    elif st.session_state.page == "meet_my_family":
        meet_my_family_screen(go_to)

    elif st.session_state.page == "find_my_family":
        find_my_family_screen(go_to)

    elif st.session_state.page == "who_is_speaking":
        who_is_speaking_screen(go_to)
