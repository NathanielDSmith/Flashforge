import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class FlashcardManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
    
    def load_data(self) -> Dict:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
        return {'sets': []}
    
    def save_data(self, data: Dict) -> bool:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_next_id(self, items: List) -> int:
        return max([item.get('id', 0) for item in items], default=0) + 1
    
    def find_set_by_id(self, set_id: int) -> Optional[Dict]:
        data = self.load_data()
        return next((s for s in data['sets'] if s['id'] == set_id), None)
    
    def find_card_by_id(self, flashcard_set: Dict, card_id: int) -> Optional[Dict]:
        return next((c for c in flashcard_set['cards'] if c['id'] == card_id), None)
    
    def create_set(self, title: str, description: str = '') -> Optional[Dict]:
        data = self.load_data()
        new_set = {
            'id': self.get_next_id(data['sets']),
            'title': title,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'cards': []
        }
        data['sets'].append(new_set)
        
        if self.save_data(data):
            return new_set
        return None
    
    def add_card(self, set_id: int, question: str, answer: str) -> Optional[Dict]:
        data = self.load_data()
        
        flashcard_set = None
        for set_item in data['sets']:
            if set_item['id'] == set_id:
                flashcard_set = set_item
                break
        
        if not flashcard_set:
            return None
        
        new_card = {
            'id': self.get_next_id(flashcard_set['cards']),
            'question': question,
            'answer': answer,
            'favorite': False,
            'created_at': datetime.now().isoformat()
        }
        flashcard_set['cards'].append(new_card)
        
        if self.save_data(data):
            return new_card
        return None
    
    def delete_set(self, set_id: int) -> bool:
        data = self.load_data()
        original_count = len(data['sets'])
        data['sets'] = [s for s in data['sets'] if s['id'] != set_id]
        
        if len(data['sets']) < original_count:
            return self.save_data(data)
        return False
    
    def delete_card(self, set_id: int, card_id: int) -> bool:
        data = self.load_data()
        
        flashcard_set = None
        for set_item in data['sets']:
            if set_item['id'] == set_id:
                flashcard_set = set_item
                break
        
        if not flashcard_set:
            return False
        
        original_count = len(flashcard_set['cards'])
        flashcard_set['cards'] = [c for c in flashcard_set['cards'] if c['id'] != card_id]
        
        if len(flashcard_set['cards']) < original_count:
            return self.save_data(data)
        return False
    
    def toggle_favorite(self, set_id: int, card_id: int) -> Tuple[bool, bool]:
        data = self.load_data()
        
        flashcard_set = None
        target_card = None
        
        for set_item in data['sets']:
            if set_item['id'] == set_id:
                flashcard_set = set_item
                for card in set_item['cards']:
                    if card['id'] == card_id:
                        target_card = card
                        break
                break
        
        if not flashcard_set or not target_card:
            return False, False
        
        target_card['favorite'] = not target_card.get('favorite', False)
        
        if self.save_data(data):
            return True, target_card['favorite']
        return False, False
    
    def get_favorite_cards(self) -> List[Dict]:
        data = self.load_data()
        favorite_cards = []
        
        for flashcard_set in data['sets']:
            for card in flashcard_set['cards']:
                if card.get('favorite', False):
                    favorite_cards.append({
                        'card': card,
                        'set': {
                            'id': flashcard_set['id'],
                            'title': flashcard_set['title']
                        }
                    })
        
        return favorite_cards
    
    def get_favorite_count(self) -> int:
        data = self.load_data()
        return sum(
            sum(1 for card in flashcard_set['cards'] if card.get('favorite', False))
            for flashcard_set in data['sets']
        ) 