import streamlit as st
import json
import os
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"
AUDIO_FOLDER = "data/audio"

# --------------------------------------------------
# UI ENHANCEMENT (SAFE – NO LOGIC CHANGE)
# --------------------------------------------------
st.markdown("""
<style>
    /* Full app background */
    body {
        background-color: #758eb7;
    }

    /* Streamlit app container */
    .stApp {
        background-color: #758eb7;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .main {
        background-color: #758eb7;
    }
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .member-card {
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

# --------------------------------------------------
# Ensure folders exist
# --------------------------------------------------
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# --------------------------------------------------
# Load existing family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# --------------------------------------------------
# Save family data
# --------------------------------------------------
def save_family_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --------------------------------------------------
# Family Setup Screen
# --------------------------------------------------
def family_setup_screen(go_to):

    st.title("👨‍👩‍👧 Family Setup (Parent Section)")
    st.write("Add, review, or remove family members used in the games.")
    st.markdown("---")

    # Initialize family members
    if "family_members" not in st.session_state:
        st.session_state.family_members = load_family_data()

    # Form reset key
    if "form_counter" not in st.session_state:
        st.session_state.form_counter = 0

    # -------------------------------
    # Input Form
    # -------------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    with st.form(f"add_member_form_{st.session_state.form_counter}"):

        name = st.text_input("Name")
        relationship = st.text_input("Relationship (e.g., Mother, Grandpa, Aunt)")
        image_file = st.file_uploader(
            "Upload Photo",
            type=["jpg", "jpeg", "png"]
        )
        audio_file = st.file_uploader(
            "Upload Voice (optional)",
            type=["mp3", "wav", "ogg"]
        )

        submitted = st.form_submit_button("➕ Add Person")

        if submitted:
            if not name or not relationship or not image_file:
                st.warning("Please enter name, relationship, and upload photo.")
            else:
                # Save image
                image_path = os.path.join(IMAGE_FOLDER, image_file.name)
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())

                # Save audio if provided
                audio_filename = None
                if audio_file:
                    audio_filename = audio_file.name
                    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                    with open(audio_path, "wb") as f:
                        f.write(audio_file.getbuffer())

                # Add member
                st.session_state.family_members.append({
                    "name": name,
                    "relationship": relationship,
                    "image": image_file.name,
                    "audio": audio_filename
                })

                save_family_data(st.session_state.family_members)
                st.success(f"{name} added successfully!")

                # RESET FORM + REFRESH UI
                st.session_state.form_counter += 1
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # Display Added Members
    # -------------------------------
    if st.session_state.family_members:
        st.subheader("👨‍👩‍👧 Added Family Members")

        cols = st.columns(3)
        for idx, member in enumerate(st.session_state.family_members):
            with cols[idx % 3]:
                st.markdown("<div class='member-card'>", unsafe_allow_html=True)

                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=140)

                st.markdown(f"**{member['name']}**")
                st.write(member["relationship"])

                if member.get("audio"):
                    audio_path = os.path.join(AUDIO_FOLDER, member["audio"])
                    if os.path.exists(audio_path):
                        st.audio(audio_path)

                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    st.session_state.family_members.pop(idx)
                    save_family_data(st.session_state.family_members)
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------
    # Navigation Buttons
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.family_members:
            if st.button("✅ Finish Setup"):
                go_to("home")
                st.rerun()

    with col2:
        if st.button("⬅ Back to Home"):
            go_to("home")
            st.rerun()
