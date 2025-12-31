import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"


# --------------------------------------------------
# Load family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


# --------------------------------------------------
# Reset game
# --------------------------------------------------
def reset_find_game():
    for key in [
        "fm_stage",
        "fm_target",
        "fm_path",
        "fm_index",
        "fm_wrong",
    ]:
        if key in st.session_state:
            del st.session_state[key]


# --------------------------------------------------
# Find My Family Game
# --------------------------------------------------
def find_my_family_screen(go_to):

    st.title("🛤️ Find My Family")
    st.write("Choose the correct path to reach your family 💙")
    st.markdown("---")

    family = load_family_data()

    if len(family) < 2:
        st.warning("Please add at least 2 family members.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # --------------------------------------------------
    # Stage setup
    # --------------------------------------------------
    if "fm_stage" not in st.session_state:
        st.session_state.fm_stage = "intro"

    # --------------------------------------------------
    # INTRO: Show family
    # --------------------------------------------------
    if st.session_state.fm_stage == "intro":
        st.subheader("👨‍👩‍👧 Your Family")

        cols = st.columns(3)
        for i, m in enumerate(family):
            with cols[i % 3]:
                img = os.path.join(IMAGE_FOLDER, m["image"])
                if os.path.exists(img):
                    st.image(Image.open(img), width=140)
                st.write(f"**{m['name']}**")
                st.write(m["relationship"])

        st.markdown("---")
        if st.button("▶ Start Game"):
            st.session_state.fm_stage = "game"
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")

        return

    # --------------------------------------------------
    # GAME SETUP
    # --------------------------------------------------
    if "fm_target" not in st.session_state:
        st.session_state.fm_target = random.choice(family)
        st.session_state.fm_path = [1, 2, 3, 4, 5, 6]
        st.session_state.fm_index = 0
        st.session_state.fm_wrong = None

    target = st.session_state.fm_target
    index = st.session_state.fm_index

    st.info(f"🧒 Task: Go to **{target['relationship']} ({target['name']})**")

    st.markdown("### 🧩 Path")

    # --------------------------------------------------
    # Draw nodes
    # --------------------------------------------------
    for i in range(len(st.session_state.fm_path)):
        node_number = st.session_state.fm_path[i]

        # COLOR LOGIC
        if i < index:
            st.success(f"🟢 Node {node_number}")
        elif i == index:
            st.warning(f"🟡 You are here (Node {node_number})")
        else:
            st.write(f"⚪ Node {node_number}")

        # If current node → show choices
        if i == index:
            st.markdown("#### Choose next path")

            correct = f"Node {node_number + 1}"
            wrong = f"Node {node_number + random.randint(2,4)}"

            col1, col2 = st.columns(2)

            with col1:
                if st.button(correct):
                    st.session_state.fm_index += 1
                    st.session_state.fm_wrong = None
                    st.rerun()

            with col2:
                if st.button(wrong):
                    st.session_state.fm_wrong = "Try again 🙂"
                    st.rerun()

            if st.session_state.fm_wrong:
                st.error(st.session_state.fm_wrong)

        st.markdown("---")

    # --------------------------------------------------
    # FINAL CHOICE
    # --------------------------------------------------
    if st.session_state.fm_index == len(st.session_state.fm_path):

        st.subheader("🎯 Final Choice")

        wrong_person = random.choice(
            [m for m in family if m != target]
        )

        col1, col2 = st.columns(2)

        with col1:
            img = os.path.join(IMAGE_FOLDER, target["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=160)
            if st.button(f"Give to {target['name']}"):
                st.balloons()
                st.success("🎉 You reached the right person!")

        with col2:
            img = os.path.join(IMAGE_FOLDER, wrong_person["image"])
            if os.path.exists(img):
                st.image(Image.open(img), width=160)
            if st.button(f"Give to {wrong_person['name']}"):
                st.error("❌ Try again!")

        st.markdown("---")
        if st.button("🔁 Play Again"):
            reset_find_game()
            st.rerun()

    if st.button("⬅ Back to Home"):
        reset_find_game()
        go_to("home")
