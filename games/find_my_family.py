import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"

GRID_SIZE = 5  # 5x5 maze

# --------------------------------------------------
# Load family data
# --------------------------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# --------------------------------------------------
# Maze Layout (1 = path, 0 = wall)
# --------------------------------------------------
MAZE = [
    [1, 1, 0, 1, 1],
    [0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
]

START_POS = (0, 0)
END_POS = (4, 4)

# --------------------------------------------------
# Find My Family Game
# --------------------------------------------------
def find_my_family_screen(go_to):

    st.title("🧭 Find My Family")

    family = load_family_data()
    if not family:
        st.warning("Please complete Family Setup first.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # ------------------------------
    # Session Init
    # ------------------------------
    if "fmf_started" not in st.session_state:
        st.session_state.fmf_started = False

    if "child_pos" not in st.session_state:
        st.session_state.child_pos = START_POS

    if "target" not in st.session_state:
        st.session_state.target = random.choice(family)

    # ==================================================
    # STEP 1: SHOW FAMILY
    # ==================================================
    if not st.session_state.fmf_started:
        st.subheader("👨‍👩‍👧 My Family")

        cols = st.columns(3)
        for i, member in enumerate(family):
            with cols[i % 3]:
                img_path = os.path.join(IMAGE_FOLDER, member["image"])
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), width=120)
                st.write(f"**{member['name']}**")
                st.write(member["relationship"])

        st.markdown("---")
        if st.button("▶ Start Game"):
            st.session_state.fmf_started = True
            st.stop()

        if st.button("⬅ Back to Home"):
            go_to("home")
        return

    # ==================================================
    # STEP 2: TASK
    # ==================================================
    st.info(f"👶 Task: Help the child reach **{st.session_state.target['relationship']} ({st.session_state.target['name']})**")

    # ==================================================
    # STEP 3: DRAW MAZE
    # ==================================================
    for r in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for c in range(GRID_SIZE):
            with cols[c]:
                if (r, c) == st.session_state.child_pos:
                    st.markdown("👶", unsafe_allow_html=True)
                elif (r, c) == END_POS:
                    img = os.path.join(IMAGE_FOLDER, st.session_state.target["image"])
                    if os.path.exists(img):
                        st.image(Image.open(img), width=50)
                elif MAZE[r][c] == 1:
                    st.markdown("🟣")
                else:
                    st.markdown("⬛")

    # ==================================================
    # STEP 4: MOVEMENT
    # ==================================================
    st.markdown("### Move the child")

    r, c = st.session_state.child_pos

    def move(nr, nc):
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and MAZE[nr][nc] == 1:
            st.session_state.child_pos = (nr, nc)
        else:
            st.warning("🚫 Can't go that way!")
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("⬆ Up"):
            move(r - 1, c)

    with col1:
        if st.button("⬅ Left"):
            move(r, c - 1)

    with col3:
        if st.button("➡ Right"):
            move(r, c + 1)

    with col2:
        if st.button("⬇ Down"):
            move(r + 1, c)

    # ==================================================
    # STEP 5: SUCCESS
    # ==================================================
    if st.session_state.child_pos == END_POS:
        st.balloons()
        st.success(f"🎉 You reached {st.session_state.target['name']}!")

        if st.button("🔁 Play Again"):
            for key in ["fmf_started", "child_pos", "target"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.stop()

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        for key in ["fmf_started", "child_pos", "target"]:
            if key in st.session_state:
                del st.session_state[key]
        go_to("home")
