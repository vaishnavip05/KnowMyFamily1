import streamlit as st
import json
import os
import random
from PIL import Image

DATA_FILE = "data/family_data.json"
IMAGE_FOLDER = "data/images"

GRID_SIZE = 5

# ✅ FIXED SOLVABLE MAZE (1 = path, 0 = wall)
MAZE = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1],
]

START = (0, 0)
END = (4, 4)

# -----------------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# -----------------------------------
def find_my_family_screen(go_to):

    st.title("🧭 Find My Family")

    family = load_family_data()
    if not family:
        st.warning("Please complete Family Setup first.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # -----------------------------------
    # SESSION STATE INIT
    # -----------------------------------
    if "started" not in st.session_state:
        st.session_state.started = False

    if "pos" not in st.session_state:
        st.session_state.pos = START

    if "target" not in st.session_state:
        st.session_state.target = random.choice(family)

    if "msg" not in st.session_state:
        st.session_state.msg = ""

    # =====================================================
    # START SCREEN (FAMILY VIEW)
    # =====================================================
    if not st.session_state.started:
        st.subheader("👨‍👩‍👧 My Family")

        cols = st.columns(3)
        for i, m in enumerate(family):
            with cols[i % 3]:
                img = os.path.join(IMAGE_FOLDER, m["image"])
                if os.path.exists(img):
                    st.image(Image.open(img), width=120)
                st.write(f"**{m['name']}**")
                st.write(m["relationship"])

        if st.button("▶ Start Game"):
            st.session_state.started = True
            st.session_state.msg = ""   # ✅ CLEAR ERROR
            st.rerun()

        if st.button("⬅ Back to Home"):
            go_to("home")

        return

    # =====================================================
    # TASK
    # =====================================================
    st.info(
        f"👶 Go to "
        f"**{st.session_state.target['relationship']} "
        f"({st.session_state.target['name']})**"
    )

    # =====================================================
    # DRAW MAZE GRID
    # =====================================================
    for r in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for c in range(GRID_SIZE):
            with cols[c]:
                if (r, c) == st.session_state.pos:
                    st.markdown("👶")
                elif (r, c) == END:
                    img = os.path.join(
                        IMAGE_FOLDER,
                        st.session_state.target["image"]
                    )
                    if os.path.exists(img):
                        st.image(Image.open(img), width=45)
                elif MAZE[r][c] == 1:
                    st.markdown("🟣")
                else:
                    st.markdown("⬛")

    # =====================================================
    # MESSAGE
    # =====================================================
    if st.session_state.msg:
        st.warning(st.session_state.msg)

    # =====================================================
    # MOVE LOGIC
    # =====================================================
    r, c = st.session_state.pos

    def move(nr, nc):
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and MAZE[nr][nc] == 1:
            st.session_state.pos = (nr, nc)
            st.session_state.msg = ""
        else:
            st.session_state.msg = "🚫 Can't go that way!"

    st.markdown("### Move the child")

    col1, col2, col3 = st.columns([1, 1, 1])

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

    # =====================================================
    # SUCCESS
    # =====================================================
    if st.session_state.pos == END:
        st.balloons()
        st.success(f"🎉 You reached {st.session_state.target['name']}!")

        if st.button("🔁 Play Again"):
            for k in ["started", "pos", "target", "msg"]:
                st.session_state.pop(k, None)
            st.rerun()

    if st.button("⬅ Back to Home"):
        for k in ["started", "pos", "target", "msg"]:
            st.session_state.pop(k, None)
        go_to("home")
