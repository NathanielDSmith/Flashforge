import unittest
import tempfile
import os
import json
from app import create_app
from models import FlashcardManager
from validators import validate_set_data, validate_card_data


class FlashForgeTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.write('{"sets": []}')
        self.temp_file.close()
        
        self.app = create_app('testing')
        self.app.config['DATA_FILE'] = self.temp_file.name
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.flashcard_manager = FlashcardManager(self.temp_file.name)
    
    def tearDown(self):
        self.app_context.pop()
        os.unlink(self.temp_file.name)
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FlashForge', response.data)
    
    def test_create_set(self):
        response = self.client.post('/set/new', data={
            'title': 'Test Set',
            'description': 'Test Description'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        data = self.flashcard_manager.load_data()
        self.assertEqual(len(data['sets']), 1)
        self.assertEqual(data['sets'][0]['title'], 'Test Set')
    
    def test_validation_set_data(self):
        is_valid, message = validate_set_data('Valid Title', 'Valid Description')
        self.assertTrue(is_valid)
        self.assertEqual(message, '')
        
        is_valid, message = validate_set_data('', 'Description')
        self.assertFalse(is_valid)
        self.assertIn('required', message)
        
        long_title = 'A' * 101
        is_valid, message = validate_set_data(long_title, 'Description')
        self.assertFalse(is_valid)
        self.assertIn('less than', message)
    
    def test_validation_card_data(self):
        is_valid, message = validate_card_data('Question?', 'Answer.')
        self.assertTrue(is_valid)
        self.assertEqual(message, '')
        
        is_valid, message = validate_card_data('', 'Answer.')
        self.assertFalse(is_valid)
        self.assertIn('required', message)
        
        is_valid, message = validate_card_data('Question?', '')
        self.assertFalse(is_valid)
        self.assertIn('required', message)
    
    def test_flashcard_manager(self):
        new_set = self.flashcard_manager.create_set('Test Set', 'Test Description')
        self.assertIsNotNone(new_set)
        if new_set:
            self.assertEqual(new_set['title'], 'Test Set')
            
            new_card = self.flashcard_manager.add_card(new_set['id'], 'Question?', 'Answer.')
            self.assertIsNotNone(new_card)
            if new_card:
                self.assertEqual(new_card['question'], 'Question?')
                
                success, favorite_status = self.flashcard_manager.toggle_favorite(new_set['id'], new_card['id'])
                self.assertTrue(success)
                self.assertTrue(favorite_status)
                
                count = self.flashcard_manager.get_favorite_count()
                self.assertEqual(count, 1)
                
                success = self.flashcard_manager.delete_card(new_set['id'], new_card['id'])
                self.assertTrue(success)
            
            success = self.flashcard_manager.delete_set(new_set['id'])
            self.assertTrue(success)


if __name__ == '__main__':
    unittest.main() 