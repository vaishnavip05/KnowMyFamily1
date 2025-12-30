import streamlit as st

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Know My Family",
    layout="wide"
)

# --------------------------------------------------
# Session State for Navigation
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# --------------------------------------------------
# Navigation Helper
# --------------------------------------------------
def go_to(page_name):
    st.session_state.page = page_name

# --------------------------------------------------
# HOME SCREEN
# --------------------------------------------------
def home_screen():
    st.title("Know My Family")
    st.write("Learn your family through simple and friendly games 💙")
    st.markdown("---")

    # Three game blocks displayed horizontally
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
# PLACEHOLDER SCREENS FOR GAMES
# (Actual game logic will go in separate files later)
# --------------------------------------------------
def meet_my_family_screen():
    st.header("👨‍👩‍👧 Meet My Family")
    st.write("Game 1 will be implemented here.")
    st.markdown("---")
    if st.button("⬅ Back to Home"):
        go_to("home")

def find_my_family_screen():
    st.header("🛤️ Find My Family")
    st.write("Game 2 will be implemented here.")
    st.markdown("---")
    if st.button("⬅ Back to Home"):
        go_to("home")

def who_is_speaking_screen():
    st.header("🔊 Who Is Speaking?")
    st.write("Game 3 will be implemented here.")
    st.markdown("---")
    if st.button("⬅ Back to Home"):
        go_to("home")

# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------
if st.session_state.page == "home":
    home_screen()

elif st.session_state.page == "meet_my_family":
    meet_my_family_screen()

elif st.session_state.page == "find_my_family":
    find_my_family_screen()

elif st.session_state.page == "who_is_speaking":
    who_is_speaking_screen()
