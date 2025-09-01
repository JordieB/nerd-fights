import streamlit as st

st.set_page_config(
    page_title="Tournament & Voting App",
    page_icon="🏆",
    layout="wide"
)

st.write("# Welcome to Tournament & Voting App! 🏆")

st.markdown(
    """
    Choose from the sidebar to get started:
    
    **🏆 Tournament Bracket** - Create elimination-style tournaments where people can vote on matchups
    
    **🔥 Smash or Pass** - Rate items one by one with automatic image loading
    
    ### Features:
    - Easy participant/item entry (paste lists with one item per line)
    - Real-time voting and results
    - Shareable URLs for collaborative voting
    - Automatic image search for Smash or Pass items
    - Progress tracking and final rankings
    
    **👈 Select a page from the sidebar** to get started!
    """
)

