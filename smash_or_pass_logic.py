from typing import List, Dict, Optional
import requests
import os

class SmashOrPassManager:
    def __init__(self):
        self.items = []
        self.current_index = 0
        self.votes = {}  # item_name: {'smash': count, 'pass': count}
        self.images = {}  # item_name: image_url
        self.subject_topic = None  # Optional topic to prefix searches
        self.game_created = False
        self.game_complete = False
    
    def create_game(self, items: List[str], subject_topic: Optional[str] = None):
        """Create a new Smash or Pass game"""
        self.items = items.copy()
        self.subject_topic = subject_topic
        self.current_index = 0
        self.votes = {}
        self.images = {}
        self.game_created = True
        self.game_complete = False
        
        # Initialize votes for all items
        for item in self.items:
            self.votes[item] = {'smash': 0, 'pass': 0}
            
        # Fetch images for all items
        self._fetch_images_for_items()
    
    def get_current_item(self) -> Optional[str]:
        """Get the current item being voted on"""
        if not self.game_created or self.current_index >= len(self.items):
            return None
        return self.items[self.current_index]
    
    def vote_smash(self, item: str):
        """Add a smash vote for the current item"""
        if item in self.votes:
            self.votes[item]['smash'] += 1
    
    def vote_pass(self, item: str):
        """Add a pass vote for the current item"""
        if item in self.votes:
            self.votes[item]['pass'] += 1
    
    def remove_smash_vote(self, item: str):
        """Remove a smash vote for the current item"""
        if item in self.votes and self.votes[item]['smash'] > 0:
            self.votes[item]['smash'] -= 1
    
    def remove_pass_vote(self, item: str):
        """Remove a pass vote for the current item"""
        if item in self.votes and self.votes[item]['pass'] > 0:
            self.votes[item]['pass'] -= 1
    
    def get_item_votes(self, item: str) -> Dict[str, int]:
        """Get vote counts for a specific item"""
        return self.votes.get(item, {'smash': 0, 'pass': 0})
    
    def next_item(self) -> bool:
        """Move to the next item"""
        if self.current_index < len(self.items) - 1:
            self.current_index += 1
            return True
        else:
            self.game_complete = True
            return False
    
    def previous_item(self) -> bool:
        """Move to the previous item"""
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
    
    def get_progress(self) -> tuple:
        """Get current progress (current_index + 1, total_items)"""
        return (self.current_index + 1, len(self.items))
    
    def is_game_complete(self) -> bool:
        """Check if the game is complete"""
        return self.game_complete
    
    def get_results(self) -> List[Dict]:
        """Get final results sorted by smash percentage"""
        results = []
        for item, votes in self.votes.items():
            total_votes = votes['smash'] + votes['pass']
            smash_percentage = (votes['smash'] / total_votes * 100) if total_votes > 0 else 0
            
            results.append({
                'item': item,
                'smash_votes': votes['smash'],
                'pass_votes': votes['pass'],
                'total_votes': total_votes,
                'smash_percentage': smash_percentage
            })
        
        # Sort by smash percentage (highest first)
        results.sort(key=lambda x: x['smash_percentage'], reverse=True)
        return results
    
    def get_total_votes(self) -> int:
        """Get total number of votes cast"""
        total = 0
        for votes in self.votes.values():
            total += votes['smash'] + votes['pass']
        return total
    
    def reset_game(self):
        """Reset the entire game"""
        self.items = []
        self.current_index = 0
        self.votes = {}
        self.images = {}
        self.subject_topic = None
        self.game_created = False
        self.game_complete = False
    
    def _fetch_images_for_items(self):
        """Fetch images for all items using Pexels API"""
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            return
        
        headers = {
            'Authorization': api_key
        }
        
        for item in self.items:
            try:
                # Create search query with optional topic prefix
                search_query = f"{self.subject_topic} {item}" if self.subject_topic else item
                
                # Search for the first image of this item
                response = requests.get(
                    f'https://api.pexels.com/v1/search',
                    headers=headers,
                    params={
                        'query': search_query,
                        'per_page': 1,
                        'orientation': 'square'
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data['photos']:
                        # Get the medium-sized image
                        self.images[item] = data['photos'][0]['src']['medium']
                    else:
                        # Fallback to a generic image or None
                        self.images[item] = None
                else:
                    self.images[item] = None
                    
            except Exception as e:
                # If API call fails, set to None
                self.images[item] = None
    
    def get_item_image(self, item: str) -> Optional[str]:
        """Get the image URL for an item"""
        return self.images.get(item)