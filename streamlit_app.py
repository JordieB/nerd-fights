import streamlit as st

st.set_page_config(
    page_title="Nerd Fights",
    page_icon="⚔️",
    layout="wide"
)

st.write("# Welcome to Nerd Fights! ⚔️")

st.markdown(
    """
    **Settle the ultimate debates with your friends!** From ranking the best husbandos to determining the supreme pie, Nerd Fights helps you and your crew decide on the best of the best through fair competition and voting.
    
    Choose your battle mode from the sidebar:
    
    **🏆 Tournament Bracket** - Classic elimination-style tournaments where friends vote on head-to-head matchups until only one champion remains
    
    **🔥 Smash or Pass** - Rate items one by one to see what rises to the top and what gets left behind
    
    ### Perfect for settling friend group debates about:
    - Best anime characters, waifus, or husbandos 
    - Ultimate food rankings (pizza toppings, desserts, etc.)
    - Movie/TV show battles
    - Video game tier lists
    - Music artists or songs
    - Literally anything your friend group argues about!
    
    ### Features:
    - Easy setup (just paste your list, one item per line)
    - Real-time collaborative voting
    - Shareable links so everyone can participate
    - Automatic tie-breakers with coin flips
    - Epic final results with medal rankings
    
    **👈 Pick your weapon from the sidebar** and let the fights begin!
    """
)

