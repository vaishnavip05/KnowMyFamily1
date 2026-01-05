import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"
AUDIO_FOLDER = "data/audio"

# ================= UI ENHANCEMENT ONLY =================
st.markdown("""
<style>
    /* Full app background */
    body {
        background-color: #6f5f90;
    }

    /* Streamlit app container */
    .stApp {
        background-color: #6f5f90;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .main {
        background-color: #8a5082;
    }
    .card {
        background-color: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        text-align: center;
    }
    .option-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 8px;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)
# ======================================================

# --------------------------------------------------
# Load family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# --------------------------------------------------
# Reset game state
# --------------------------------------------------
def reset_who_speaking():
    for key in [
        "ws_stage",
        "ws_target",
        "ws_options",
    ]:
        if key in st.session_state:
            del st.session_state[key]

# --------------------------------------------------
# Who Is Speaking Game
# --------------------------------------------------
def who_is_speaking_screen(go_to):

    st.title("🔊 Who Is Speaking?")
    st.write("Listen carefully and find whose voice it is 💙")
    st.markdown("---")

    family = load_family_data()

    # Filter only members with audio
    family_with_audio = [m for m in family if m.get("audio")]

    if len(family_with_audio) < 2:
        st.warning("Please add at least 2 family members with voice recordings.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # --------------------------------------------------
    # Stage handling
    # --------------------------------------------------
    if "ws_stage" not in st.session_state:
        st.session_state.ws_stage = "intro"

    # --------------------------------------------------
    # STAGE 1: Familiarization
    # --------------------------------------------------
    if st.session_state.ws_stage == "intro":
        st.subheader("👨‍👩‍👧 Listen to Your Family")

        cols = st.columns(3)
        for idx, member in enumerate(family_with_audio):
            with cols[idx % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                img = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img):
                    st.image(Image.open(img), width=140)

                st.markdown(f"**{member['name']}**")
                st.write(member["relationship"])

                audio = os.path.join(AUDIO_FOLDER, member["audio"])
                if os.path.exists(audio):
                    st.audio(audio)

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        if st.button("▶ Start Game"):
            st.session_state.ws_stage = "game"
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")

        return

    # --------------------------------------------------
    # STAGE 2: Game Mode
    # --------------------------------------------------
    if "ws_target" not in st.session_state:
        st.session_state.ws_target = random.choice(family_with_audio)

        options = family_with_audio.copy()
        random.shuffle(options)
        st.session_state.ws_options = options[:3]

        if st.session_state.ws_target not in st.session_state.ws_options:
            st.session_state.ws_options[-1] = st.session_state.ws_target
            random.shuffle(st.session_state.ws_options)

    target = st.session_state.ws_target

    st.subheader("🎧 Whose voice is this?")
    st.audio(os.path.join(AUDIO_FOLDER, target["audio"]))
    st.markdown("🔁 You can replay the voice as many times as you want")

    st.markdown("---")

    cols = st.columns(len(st.session_state.ws_options))

    for idx, member in enumerate(st.session_state.ws_options):
        with cols[idx]:
            st.markdown("<div class='option-card'>", unsafe_allow_html=True)

            img = os.path.join(IMAGE_FOLDER, member["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=140)

            if st.button(member["name"], key=f"choose_{member['name']}"):
                if member == target:
                    st.balloons()
                    st.success("🎉 Correct! Great listening!")
                else:
                    st.warning("❌ Try again 🙂")

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔁 Play Again"):
        reset_who_speaking()
        st.rerun()

    if st.button("⬅ Back to Home"):
        reset_who_speaking()
        go_to("home")
