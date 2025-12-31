import streamlit as st
import json
import os
import random

DATA_FILE = "data/family_data.json"

# -----------------------------
# Load family data
# -----------------------------
def load_family_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# -----------------------------
# Maze layout (0 = path, 1 = wall)
# -----------------------------
MAZE = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0],
]

START_POS = (0, 0)

# -----------------------------
# Render Maze
# -----------------------------
def render_maze(player_pos, target_positions, correct_target):
    for r in range(len(MAZE)):
        cols = st.columns(len(MAZE[0]))
        for c in range(len(MAZE[0])):
            cell = "⬜"
            if MAZE[r][c] == 1:
                cell = "⬛"
            if (r, c) == player_pos:
                cell = "🧒"
            if (r, c) in target_positions:
                name = target_positions[(r, c)]["name"]
                cell = "👤"
            cols[c].markdown(f"<h3 style='text-align:center'>{cell}</h3>", unsafe_allow_html=True)

# -----------------------------
# Main Game Screen
# -----------------------------
def find_my_family_screen(go_to):

    st.title("🧭 Find My Family")
    family = load_family_data()

    if not family:
        st.warning("Please complete Family Setup first.")
        if st.button("⬅ Back to Setup"):
            go_to("setup")
        return

    # -----------------------------
    # INIT SESSION STATE
    # -----------------------------
    if "start_game" not in st.session_state:
        st.session_state.start_game = False

    if not st.session_state.start_game:
        st.subheader("👨‍👩‍👧 My Family")
        cols = st.columns(3)
        for i, m in enumerate(family):
            with cols[i % 3]:
                st.write(f"**{m['name']}**")
                st.write(m["relationship"])

        if st.button("▶ Start Game"):
            st.session_state.start_game = True
            st.session_state.player_pos = START_POS
            st.session_state.target = random.choice(family)

            # Place two family members at end
            st.session_state.targets = {
                (4, 4): st.session_state.target,
                (4, 0): random.choice([f for f in family if f != st.session_state.target])
            }
            st.stop()

        if st.button("⬅ Back to Home"):
            go_to("home")
        return

    # -----------------------------
    # GAME PLAY
    # -----------------------------
    target = st.session_state.target
    player_pos = st.session_state.player_pos

    st.info(f"👶 Task: Help the child reach **{target['relationship']} ({target['name']})**")

    render_maze(player_pos, st.session_state.targets, target)

    st.markdown("### Move the child")

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("⬆️ Up"):
            move(-1, 0)
    with col1:
        if st.button("⬅️ Left"):
            move(0, -1)
    with col3:
        if st.button("➡️ Right"):
            move(0, 1)
    with col2:
        if st.button("⬇️ Down"):
            move(1, 0)

    st.markdown("---")
    if st.button("⬅ Back to Home"):
        reset_game()
        go_to("home")

# -----------------------------
# Movement Logic
# -----------------------------
def move(dr, dc):
    r, c = st.session_state.player_pos
    nr, nc = r + dr, c + dc

    if nr < 0 or nc < 0 or nr >= len(MAZE) or nc >= len(MAZE[0]):
        st.warning("🚫 Can't go that way!")
        st.stop()

    if MAZE[nr][nc] == 1:
        st.warning("🚧 That path is blocked!")
        st.stop()

    st.session_state.player_pos = (nr, nc)

    # Check destination
    if (nr, nc) in st.session_state.targets:
        chosen = st.session_state.targets[(nr, nc)]
        if chosen["name"] == st.session_state.target["name"]:
            st.balloons()
            st.success("🎉 You reached the correct family member!")
        else:
            st.error(f"❌ This is {chosen['name']}. Try again!")
            st.session_state.player_pos = START_POS

    st.stop()

# -----------------------------
# Reset
# -----------------------------
def reset_game():
    for key in ["start_game", "player_pos", "targets", "target"]:
        if key in st.session_state:
            del st.session_state[key]
