import streamlit as st
import pandas as pd
import random
import math
from bracket_logic import BracketManager

st.set_page_config(
    page_title="Tournament Bracket",
    page_icon="🏆",
    layout="wide"
)

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
else:
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
    else:
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
        if st.button(f"Vote for {participant1}", key=f"vote_{matchup_id}_{participant1}", width="stretch"):
            bracket_manager.vote(matchup_id, participant1)
            st.rerun()
    
    with col2:
        if st.button(f"Vote for {participant2}", key=f"vote_{matchup_id}_{participant2}", width="stretch"):
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