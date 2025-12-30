import streamlit as st

def who_is_speaking_screen(go_to):
    st.header("🔊 Who Is Speaking?")
    st.write("Listen to the voice and identify the correct family member.")
    st.markdown("---")

    st.info("This game will be implemented next.")

    if st.button("⬅ Back to Home"):
        go_to("home")
