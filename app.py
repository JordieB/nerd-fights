import streamlit as st
import pandas as pd
import random
import math
from bracket_logic import BracketManager
from smash_or_pass_logic import SmashOrPassManager

def main():
    st.set_page_config(
        page_title="Tournament & Voting App",
        page_icon="🏆",
        layout="wide"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Select Page:", ["🏆 Tournament Bracket", "🔥 Smash or Pass"])
    
    if page == "🏆 Tournament Bracket":
        tournament_page()
    elif page == "🔥 Smash or Pass":
        smash_or_pass_page()

def tournament_page():
    st.title("🏆 Tournament Bracket Creator")
    st.markdown("Create and share tournament brackets with voting functionality!")
    
    # Initialize session state
    if 'bracket_manager' not in st.session_state:
        st.session_state.bracket_manager = BracketManager()
    
    bracket_manager = st.session_state.bracket_manager
    
    # Sidebar for bracket creation and management
    with st.sidebar:
        st.header("Bracket Setup")
        
        # Tournament name
        tournament_name = st.text_input("Tournament Name", value=bracket_manager.tournament_name)
        if tournament_name != bracket_manager.tournament_name:
            bracket_manager.tournament_name = tournament_name
        
        # Number of participants (must be power of 2)
        st.subheader("Number of Participants")
        participant_options = [4, 8, 16, 32, 64]
        num_participants = st.selectbox("Select number of participants:", participant_options)
        
        # Participant entry
        st.subheader("Participants")
        st.markdown(f"Enter {num_participants} participants (one per line):")
        
        participant_text = st.text_area(
            "Participant List",
            height=150,
            placeholder="Enter participant names here...\nOne name per line\n\nExample:\nAlice\nBob\nCharlie\nDiane",
            label_visibility="collapsed"
        )
        
        # Parse participants from text area
        participants = []
        if participant_text.strip():
            participants = [p.strip() for p in participant_text.strip().split('\n') if p.strip()]
        
        # Show current count
        st.markdown(f"**Current count:** {len(participants)}/{num_participants}")
        
        # Create bracket button
        if st.button("Create/Update Bracket", type="primary"):
            if len(participants) == num_participants and all(p.strip() for p in participants):
                bracket_manager.create_bracket(participants)
                st.success("Bracket created successfully!")
                st.rerun()
            elif len(participants) != num_participants:
                st.error(f"Please enter exactly {num_participants} participant names. You have {len(participants)}.")
            else:
                st.error("Please make sure all participant names are filled in.")
        
        # Reset bracket button
        if st.button("Reset Bracket"):
            bracket_manager.reset_bracket()
            st.success("Bracket reset!")
            st.rerun()
        
        # Bracket sharing info
        if bracket_manager.bracket_created:
            st.subheader("Share Bracket")
            st.info("Share this URL to allow others to vote on matchups!")
            st.code(st.get_option("server.baseUrlPath") or "Your Streamlit Cloud URL")
    
    # Main content area
    if not bracket_manager.bracket_created:
        st.info("👆 Use the sidebar to create your tournament bracket!")
        st.markdown("""
        ### How to use:
        1. Enter a tournament name
        2. Select number of participants (4, 8, 16, 32, or 64)
        3. Enter participant names
        4. Click "Create Bracket" to generate the tournament
        5. Share the URL for others to vote!
        """)
        return
    
    # Display tournament info
    if bracket_manager.tournament_name:
        st.header(f"🏆 {bracket_manager.tournament_name}")
    
    # Check if tournament is complete
    if bracket_manager.is_tournament_complete():
        winner = bracket_manager.get_winner()
        st.balloons()
        st.success(f"🎉 Tournament Complete! Winner: **{winner}**")
        
        # Display final bracket
        display_bracket(bracket_manager)
        
        # Tournament stats
        display_tournament_stats(bracket_manager)
        return
    
    # Current round info
    current_round = bracket_manager.get_current_round()
    total_rounds = bracket_manager.get_total_rounds()
    st.subheader(f"Round {current_round} of {total_rounds}")
    
    # Display current matchups for voting
    display_voting_interface(bracket_manager)
    
    # Display bracket visualization
    st.subheader("Bracket Progress")
    display_bracket(bracket_manager)
    
    # Tournament progress
    display_tournament_progress(bracket_manager)

def display_voting_interface(bracket_manager):
    """Display voting interface for current round matchups"""
    current_matchups = bracket_manager.get_current_matchups()
    
    if not current_matchups:
        st.info("All matchups in this round are complete!")
        if st.button("Advance to Next Round", type="primary"):
            bracket_manager.advance_round()
            st.rerun()
        return
    
    st.subheader("Vote on Matchups")
    
    # Create columns for matchups
    cols_per_row = min(2, len(current_matchups))
    rows = math.ceil(len(current_matchups) / cols_per_row)
    
    matchup_index = 0
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            if matchup_index < len(current_matchups):
                with cols[col_idx]:
                    display_matchup_voting(bracket_manager, current_matchups[matchup_index], matchup_index)
                matchup_index += 1
    
    # Check if all current matchups are complete
    if bracket_manager.all_current_matchups_complete():
        st.success("All matchups in this round are complete!")
        if st.button("Advance to Next Round", type="primary"):
            bracket_manager.advance_round()
            st.rerun()

def display_matchup_voting(bracket_manager, matchup, matchup_index):
    """Display individual matchup voting interface"""
    participant1, participant2 = matchup['participants']
    matchup_id = matchup['id']
    
    st.markdown(f"### Matchup {matchup_index + 1}")
    st.markdown(f"**{participant1}** vs **{participant2}**")
    
    # Get current votes
    votes = bracket_manager.get_matchup_votes(matchup_id)
    total_votes = sum(votes.values())
    
    # Display current vote counts
    if total_votes > 0:
        st.markdown(f"**Current Votes:** {total_votes}")
        for participant, vote_count in votes.items():
            percentage = (vote_count / total_votes) * 100 if total_votes > 0 else 0
            st.markdown(f"- {participant}: {vote_count} votes ({percentage:.1f}%)")
    else:
        st.markdown("**No votes yet**")
    
    # Voting buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"Vote for {participant1}", key=f"vote_{matchup_id}_{participant1}", use_container_width=True):
            bracket_manager.vote(matchup_id, participant1)
            st.rerun()
    
    with col2:
        if st.button(f"Vote for {participant2}", key=f"vote_{matchup_id}_{participant2}", use_container_width=True):
            bracket_manager.vote(matchup_id, participant2)
            st.rerun()
    
    # Determine winner button (admin feature)
    if total_votes > 0:
        winner = max(votes.keys(), key=lambda x: votes[x])
        if votes[winner] > votes[list(votes.keys())[0] if list(votes.keys())[0] != winner else list(votes.keys())[1]]:
            if st.button(f"Confirm Winner: {winner}", key=f"confirm_{matchup_id}", type="secondary"):
                bracket_manager.set_matchup_winner(matchup_id, winner)
                st.rerun()

def display_bracket(bracket_manager):
    """Display bracket visualization"""
    bracket_data = bracket_manager.get_bracket_display_data()
    
    if not bracket_data:
        st.info("Bracket will appear here once created.")
        return
    
    # Create a simple text-based bracket visualization
    st.markdown("### Tournament Bracket")
    
    for round_num, round_data in bracket_data.items():
        st.markdown(f"**Round {round_num}**")
        
        for matchup in round_data:
            if matchup['completed']:
                winner = matchup['winner']
                loser = matchup['participants'][0] if matchup['participants'][1] == winner else matchup['participants'][1]
                st.markdown(f"- ~~{loser}~~ vs **{winner}** ✅")
            elif len(matchup['participants']) == 2:
                p1, p2 = matchup['participants']
                votes = bracket_manager.get_matchup_votes(matchup['id'])
                vote_info = f" ({votes[p1]} - {votes[p2]})" if sum(votes.values()) > 0 else ""
                st.markdown(f"- {p1} vs {p2}{vote_info}")
            else:
                st.markdown(f"- {matchup['participants'][0]} (bye)")
        
        st.markdown("---")

def display_tournament_progress(bracket_manager):
    """Display tournament progress statistics"""
    st.subheader("Tournament Progress")
    
    total_matchups = bracket_manager.get_total_matchups()
    completed_matchups = bracket_manager.get_completed_matchups()
    progress_percentage = (completed_matchups / total_matchups) * 100 if total_matchups > 0 else 0
    
    # Progress bar
    st.progress(progress_percentage / 100)
    st.markdown(f"**Progress:** {completed_matchups}/{total_matchups} matchups completed ({progress_percentage:.1f}%)")
    
    # Round progress
    current_round = bracket_manager.get_current_round()
    total_rounds = bracket_manager.get_total_rounds()
    st.markdown(f"**Current Round:** {current_round} of {total_rounds}")

def display_tournament_stats(bracket_manager):
    """Display final tournament statistics"""
    st.subheader("Tournament Statistics")
    
    total_votes = bracket_manager.get_total_votes()
    total_matchups = bracket_manager.get_total_matchups()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Votes", total_votes)
    
    with col2:
        st.metric("Total Matchups", total_matchups)
    
    with col3:
        st.metric("Avg Votes per Matchup", f"{total_votes/total_matchups:.1f}" if total_matchups > 0 else "0")
    
    # Most voted matchup
    most_voted_matchup = bracket_manager.get_most_voted_matchup()
    if most_voted_matchup:
        st.markdown(f"**Most Popular Matchup:** {most_voted_matchup}")

def smash_or_pass_page():
    st.title("🔥 Smash or Pass")
    st.markdown("Rate items one by one - Smash 💥 or Pass 👋")
    
    # Initialize session state for Smash or Pass
    if 'sop_manager' not in st.session_state:
        st.session_state.sop_manager = SmashOrPassManager()
    
    sop_manager = st.session_state.sop_manager
    
    # Sidebar for game setup
    with st.sidebar:
        st.header("Game Setup")
        
        # Item list entry
        st.subheader("Items to Rate")
        st.markdown("Enter items to rate (one per line):")
        
        items_text = st.text_area(
            "Items List",
            height=200,
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
                    sop_manager.create_game(items)
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
        return
    
    # Check if game is complete
    if sop_manager.is_game_complete():
        display_sop_results(sop_manager)
        return
    
    # Display current item voting interface
    current_item = sop_manager.get_current_item()
    if current_item:
        display_sop_voting_interface(sop_manager, current_item)
    
    # Navigation and progress
    display_sop_navigation(sop_manager)

def display_sop_voting_interface(sop_manager, current_item):
    """Display voting interface for current item"""
    current_pos, total_items = sop_manager.get_progress()
    
    # Progress indicator
    st.progress(current_pos / total_items)
    st.markdown(f"**Item {current_pos} of {total_items}**")
    
    # Current item display with image
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display image if available
        image_url = sop_manager.get_item_image(current_item)
        if image_url:
            st.image(image_url, width=300, caption=current_item)
        else:
            # Fallback: show a placeholder or just the text
            st.markdown(f"### 📷")
            st.markdown(f"*(No image found)*")
    
    with col2:
        st.markdown(f"# {current_item}")
        
        # Get current votes
        votes = sop_manager.get_item_votes(current_item)
        
        # Show current results if there are votes
        total_votes = votes['smash'] + votes['pass']
        if total_votes > 0:
            smash_percentage = (votes['smash'] / total_votes) * 100
            st.markdown(f"**Current result:** {smash_percentage:.1f}% Smash, {100-smash_percentage:.1f}% Pass")
    
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
            if st.button("+ Smash", key="smash_plus", use_container_width=True):
                sop_manager.vote_smash(current_item)
                st.rerun()
        with smash_col2:
            if st.button("- Smash", key="smash_minus", use_container_width=True):
                sop_manager.remove_smash_vote(current_item)
                st.rerun()
    
    with vote_col2:
        st.markdown("### 👋 PASS")
        st.markdown(f"**Votes: {votes['pass']}**")
        
        # Pass voting buttons
        pass_col1, pass_col2 = st.columns(2)
        with pass_col1:
            if st.button("+ Pass", key="pass_plus", use_container_width=True):
                sop_manager.vote_pass(current_item)
                st.rerun()
        with pass_col2:
            if st.button("- Pass", key="pass_minus", use_container_width=True):
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

if __name__ == "__main__":
    main()
