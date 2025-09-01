import streamlit as st
import math
from smash_or_pass_logic import SmashOrPassManager

st.set_page_config(
    page_title="Smash or Pass",
    page_icon="🔥",
    layout="wide"
)

# Function definitions first
def display_sop_voting_interface(sop_manager, current_item):
    """Display voting interface for current item"""
    current_pos, total_items = sop_manager.get_progress()
    
    # Progress indicator
    st.progress(current_pos / total_items)
    st.markdown(f"**Item {current_pos} of {total_items}**")
    
    # Current item display - name first, then centered image
    st.markdown(f"<h1 style='text-align: center'>{current_item}</h1>", unsafe_allow_html=True)
    
    # Display image centered below the name
    image_url = sop_manager.get_item_image(current_item)
    if image_url:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_url, width=300, use_container_width=True)
    else:
        # Fallback: show a placeholder centered
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📷")
            st.markdown("*(No image found)*")
    
    # Show current results if there are votes
    votes = sop_manager.get_item_votes(current_item)
    total_votes = votes['smash'] + votes['pass']
    if total_votes > 0:
        smash_percentage = (votes['smash'] / total_votes) * 100
        st.markdown(f"<div style='text-align: center'><b>Current result: {smash_percentage:.1f}% Smash, {100-smash_percentage:.1f}% Pass</b></div>", unsafe_allow_html=True)
    
    # Move voting interface outside columns
    st.markdown("---")
    
    # Voting interface
    vote_col1, vote_col2 = st.columns(2)
    
    with vote_col1:
        st.markdown("### 💥 SMASH")
        st.markdown(f"**Votes: {votes['smash']}**")
        
        # Smash voting buttons
        smash_col1, smash_col2 = st.columns(2)
        with smash_col1:
            if st.button("+ ", key="smash_plus", use_container_width=True, type="primary"):
                sop_manager.vote_smash(current_item)
                st.rerun()
        with smash_col2:
            if st.button("− ", key="smash_minus", use_container_width=True):
                sop_manager.remove_smash_vote(current_item)
                st.rerun()
    
    with vote_col2:
        st.markdown("### 👋 PASS")
        st.markdown(f"**Votes: {votes['pass']}**")
        
        # Pass voting buttons
        pass_col1, pass_col2 = st.columns(2)
        with pass_col1:
            if st.button("+ ", key="pass_plus", use_container_width=True, type="primary"):
                sop_manager.vote_pass(current_item)
                st.rerun()
        with pass_col2:
            if st.button("− ", key="pass_minus", use_container_width=True):
                sop_manager.remove_pass_vote(current_item)
                st.rerun()

def display_sop_navigation(sop_manager):
    """Display navigation controls"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=sop_manager.current_index == 0):
            sop_manager.previous_item()
            st.rerun()
    
    with col2:
        current_pos, total_items = sop_manager.get_progress()
        st.markdown(f"<div style='text-align: center'><b>Item {current_pos} of {total_items}</b></div>", unsafe_allow_html=True)
    
    with col3:
        if sop_manager.current_index == len(sop_manager.items) - 1:
            if st.button("🏁 Finish Game", type="primary"):
                sop_manager.game_complete = True
                st.rerun()
        else:
            if st.button("Next ➡️"):
                sop_manager.next_item()
                st.rerun()

def display_sop_results(sop_manager):
    """Display final results"""
    st.balloons()
    st.success("🎉 Game Complete!")
    
    results = sop_manager.get_results()
    total_votes = sop_manager.get_total_votes()
    
    st.markdown(f"### Final Results")
    st.markdown(f"**Total votes cast:** {total_votes}")
    
    # Results table
    st.markdown("### Rankings")
    
    for i, result in enumerate(results, 1):
        # Create columns for ranking display
        col1, col2, col3 = st.columns([1, 3, 2])
        
        with col1:
            # Medal emojis for top 3
            if i == 1:
                st.markdown("🥇")
            elif i == 2:
                st.markdown("🥈")
            elif i == 3:
                st.markdown("🥉")
            else:
                st.markdown(f"**{i}.**")
        
        with col2:
            st.markdown(f"**{result['item']}**")
        
        with col3:
            if result['total_votes'] > 0:
                st.markdown(f"{result['smash_percentage']:.1f}% Smash")
                st.markdown(f"({result['smash_votes']} smash, {result['pass_votes']} pass)")
            else:
                st.markdown("No votes")
        
        st.markdown("---")
    
    # Play again button
    if st.button("🔄 Play Again", type="primary"):
        sop_manager.reset_game()
        st.rerun()

# Main app starts here
st.title("🔥 Smash or Pass")
st.markdown("Rate items one by one - Smash 💥 or Pass 👋")

# Initialize session state for Smash or Pass
if 'sop_manager' not in st.session_state:
    st.session_state.sop_manager = SmashOrPassManager()

sop_manager = st.session_state.sop_manager

# Sidebar for game setup
with st.sidebar:
    st.header("Game Setup")
    
    # Subject topic entry
    st.subheader("Subject Topic (Optional)")
    subject_topic = st.text_input(
        "Subject Topic",
        placeholder="e.g., reptile, car, food, etc.",
        help="This will be added to each item search for better image results"
    )
    
    # Item list entry
    st.subheader("Items to Rate")
    st.markdown("Enter items to rate (one per line):")
    
    items_text = st.text_area(
        "Items List",
        height=180,
        placeholder="Enter items here...\nOne item per line\n\nExample:\nIguana\nGecko\nPython\nTurtle\nChameleon",
        label_visibility="collapsed"
    )
    
    # Parse items from text area
    items = []
    if items_text.strip():
        items = [item.strip() for item in items_text.strip().split('\n') if item.strip()]
    
    # Show current count
    st.markdown(f"**Items entered:** {len(items)}")
    
    # Create game button
    if st.button("Start Smash or Pass", type="primary"):
        if len(items) >= 2:
            with st.spinner("Creating game and loading images..."):
                sop_manager.create_game(items, subject_topic.strip() if subject_topic.strip() else None)
            st.success("Game started!")
            st.rerun()
        else:
            st.error("Please enter at least 2 items to rate.")
    
    # Reset game button
    if st.button("Reset Game"):
        sop_manager.reset_game()
        st.success("Game reset!")
        st.rerun()

# Main content area
if not sop_manager.game_created:
    st.info("👆 Use the sidebar to start your Smash or Pass game!")
    st.markdown("""
    ### How to use:
    1. Enter items to rate in the sidebar (one per line)
    2. Click "Start Smash or Pass" to begin
    3. Vote with multiple people by clicking Smash/Pass buttons
    4. Use +/- buttons to adjust votes before moving on
    5. Navigate through items and see final results!
    """)
else:
    # Check if game is complete
    if sop_manager.is_game_complete():
        display_sop_results(sop_manager)
    else:
        # Display current item voting interface
        current_item = sop_manager.get_current_item()
        if current_item:
            display_sop_voting_interface(sop_manager, current_item)
        
        # Navigation and progress
        display_sop_navigation(sop_manager)