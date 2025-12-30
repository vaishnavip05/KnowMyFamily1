import streamlit as st
import json
import os
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"
AUDIO_FOLDER = "data/audio"

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

        submitted = st.form_submit_button("Add Person")

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

                # ✅ RESET FORM CORRECTLY
                st.session_state.form_counter += 1
                st.stop()   # ⬅ THIS LINE FIXES THE ISSUE

    st.markdown("---")

    # -------------------------------
    # Display Added Members
    # -------------------------------
    if st.session_state.family_members:
        st.subheader("Added Family Members")

        cols = st.columns(3)
        for idx, member in enumerate(st.session_state.family_members):
            with cols[idx % 3]:
                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=150)

                st.write(f"**{member['name']}**")
                st.write(member["relationship"])

                if member.get("audio"):
                    audio_path = os.path.join(AUDIO_FOLDER, member["audio"])
                    if os.path.exists(audio_path):
                        st.audio(audio_path)

                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    st.session_state.family_members.pop(idx)
                    save_family_data(st.session_state.family_members)
                    st.stop()

    st.markdown("---")

    # -------------------------------
    # Navigation Buttons
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.family_members:
            if st.button("✅ Finish Setup"):
                go_to("home")

    with col2:
        if st.button("⬅ Back to Home"):
            go_to("home")
