import random
import math
from typing import List, Dict, Tuple, Optional

class BracketManager:
    def __init__(self):
        self.tournament_name = ""
        self.participants = []
        self.bracket = {}
        self.votes = {}
        self.bracket_created = False
        self.current_round = 1
        self.total_rounds = 0
    
    def create_bracket(self, participants: List[str]):
        """Create a new tournament bracket"""
        self.participants = participants.copy()
        self.total_rounds = int(math.log2(len(participants)))
        self.current_round = 1
        self.bracket = {}
        self.votes = {}
        self.bracket_created = True
        
        # Shuffle participants for random seeding
        shuffled_participants = participants.copy()
        random.shuffle(shuffled_participants)
        
        # Create first round matchups
        self._create_round_matchups(1, shuffled_participants)
    
    def _create_round_matchups(self, round_num: int, participants: List[str]):
        """Create matchups for a specific round"""
        if round_num not in self.bracket:
            self.bracket[round_num] = []
        
        matchup_id = 0
        for i in range(0, len(participants), 2):
            matchup = {
                'id': f"r{round_num}_m{matchup_id}",
                'participants': [participants[i]],
                'winner': None,
                'completed': False
            }
            
            # Add second participant if available (handle byes)
            if i + 1 < len(participants):
                matchup['participants'].append(participants[i + 1])
            else:
                # Bye - automatically advance
                matchup['winner'] = participants[i]
                matchup['completed'] = True
            
            self.bracket[round_num].append(matchup)
            
            # Initialize votes for this matchup
            self.votes[matchup['id']] = {}
            for participant in matchup['participants']:
                self.votes[matchup['id']][participant] = 0
            
            matchup_id += 1
    
    def vote(self, matchup_id: str, participant: str):
        """Record a vote for a participant in a matchup"""
        if matchup_id in self.votes and participant in self.votes[matchup_id]:
            self.votes[matchup_id][participant] += 1
    
    def get_matchup_votes(self, matchup_id: str) -> Dict[str, int]:
        """Get vote counts for a matchup"""
        return self.votes.get(matchup_id, {})
    
    def set_matchup_winner(self, matchup_id: str, winner: str):
        """Set the winner of a matchup"""
        for round_num in self.bracket:
            for matchup in self.bracket[round_num]:
                if matchup['id'] == matchup_id:
                    matchup['winner'] = winner
                    matchup['completed'] = True
                    return
    
    def get_current_matchups(self) -> List[Dict]:
        """Get all incomplete matchups from the current round"""
        if self.current_round not in self.bracket:
            return []
        
        return [m for m in self.bracket[self.current_round] 
                if not m['completed'] and len(m['participants']) == 2]
    
    def all_current_matchups_complete(self) -> bool:
        """Check if all matchups in current round are complete"""
        if self.current_round not in self.bracket:
            return True
        
        return all(m['completed'] for m in self.bracket[self.current_round])
    
    def advance_round(self):
        """Advance to the next round"""
        if not self.all_current_matchups_complete():
            return False
        
        # Get winners from current round
        winners = []
        for matchup in self.bracket[self.current_round]:
            if matchup['winner']:
                winners.append(matchup['winner'])
        
        # Create next round if we have more than one winner
        if len(winners) > 1:
            self.current_round += 1
            self._create_round_matchups(self.current_round, winners)
            return True
        
        return False
    
    def is_tournament_complete(self) -> bool:
        """Check if the tournament is complete"""
        if not self.bracket_created or self.current_round not in self.bracket:
            return False
        
        # Tournament is complete if current round has only one matchup that's completed
        current_round_matchups = self.bracket[self.current_round]
        return (len(current_round_matchups) == 1 and 
                current_round_matchups[0]['completed'])
    
    def get_winner(self) -> Optional[str]:
        """Get the tournament winner"""
        if not self.is_tournament_complete():
            return None
        
        return self.bracket[self.current_round][0]['winner']
    
    def get_current_round(self) -> int:
        """Get current round number"""
        return self.current_round
    
    def get_total_rounds(self) -> int:
        """Get total number of rounds"""
        return self.total_rounds
    
    def get_bracket_display_data(self) -> Dict:
        """Get formatted bracket data for display"""
        return self.bracket
    
    def get_total_matchups(self) -> int:
        """Get total number of matchups in the tournament"""
        total = 0
        for round_matchups in self.bracket.values():
            total += len(round_matchups)
        return total
    
    def get_completed_matchups(self) -> int:
        """Get number of completed matchups"""
        completed = 0
        for round_matchups in self.bracket.values():
            completed += sum(1 for m in round_matchups if m['completed'])
        return completed
    
    def get_total_votes(self) -> int:
        """Get total number of votes cast"""
        total_votes = 0
        for matchup_votes in self.votes.values():
            total_votes += sum(matchup_votes.values())
        return total_votes
    
    def get_most_voted_matchup(self) -> Optional[str]:
        """Get the matchup with the most votes"""
        max_votes = 0
        most_voted = None
        
        for matchup_id, matchup_votes in self.votes.items():
            total_matchup_votes = sum(matchup_votes.values())
            if total_matchup_votes > max_votes:
                max_votes = total_matchup_votes
                participants = list(matchup_votes.keys())
                if len(participants) >= 2:
                    most_voted = f"{participants[0]} vs {participants[1]} ({max_votes} votes)"
        
        return most_voted
    
    def reset_bracket(self):
        """Reset the entire bracket"""
        self.tournament_name = ""
        self.participants = []
        self.bracket = {}
        self.votes = {}
        self.bracket_created = False
        self.current_round = 1
        self.total_rounds = 0
