import unittest
import tempfile
import os
import app as app_module
from models import FlashcardManager
from validators import validate_set_data, validate_card_data


class FlashForgeTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        os.close(self.db_fd)
        os.unlink(self.db_path)  # let FlashcardManager create a fresh schema

        self.flashcard_manager = FlashcardManager(self.db_path)

        self._orig_manager = app_module.flashcard_manager
        app_module.flashcard_manager = self.flashcard_manager

        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()
        self.app_context = app_module.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        app_module.flashcard_manager = self._orig_manager
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FlashForge', response.data)

    def test_create_set(self):
        response = self.client.post('/set/new', data={
            'title': 'Test Set',
            'description': 'Test Description',
            'category': 'general',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        data = self.flashcard_manager.load_data()
        self.assertEqual(len(data['sets']), 1)
        self.assertEqual(data['sets'][0]['title'], 'Test Set')
        self.assertEqual(data['sets'][0]['category'], 'general')

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
        new_set = self.flashcard_manager.create_set('Test Set', 'Test Description', 'programming')
        self.assertIsNotNone(new_set)
        self.assertEqual(new_set['title'], 'Test Set')
        self.assertEqual(new_set['category'], 'programming')

        new_card = self.flashcard_manager.add_card(new_set['id'], 'Question?', 'Answer.')
        self.assertIsNotNone(new_card)
        self.assertEqual(new_card['question'], 'Question?')

        success, favorite_status = self.flashcard_manager.toggle_favorite(new_set['id'], new_card['id'])
        self.assertTrue(success)
        self.assertTrue(favorite_status)

        count = self.flashcard_manager.get_favorite_count()
        self.assertEqual(count, 1)

        self.assertTrue(self.flashcard_manager.delete_card(new_set['id'], new_card['id']))
        self.assertTrue(self.flashcard_manager.delete_set(new_set['id']))

    def test_update_set(self):
        new_set = self.flashcard_manager.create_set('Original', '', 'general')
        self.assertTrue(self.flashcard_manager.update_set(new_set['id'], 'Updated', 'New desc', 'japanese'))
        fetched = self.flashcard_manager.find_set_by_id(new_set['id'])
        self.assertEqual(fetched['title'], 'Updated')
        self.assertEqual(fetched['category'], 'japanese')

    def test_update_card(self):
        new_set = self.flashcard_manager.create_set('Set', '', 'general')
        new_card = self.flashcard_manager.add_card(new_set['id'], 'Q?', 'A.')
        self.assertTrue(self.flashcard_manager.update_card(new_set['id'], new_card['id'], 'New Q?', 'New A.'))
        fetched = self.flashcard_manager.find_set_by_id(new_set['id'])
        self.assertEqual(fetched['cards'][0]['question'], 'New Q?')

    def test_cascade_delete(self):
        new_set = self.flashcard_manager.create_set('Set', '', 'general')
        self.flashcard_manager.add_card(new_set['id'], 'Q?', 'A.')
        self.flashcard_manager.delete_set(new_set['id'])
        self.assertIsNone(self.flashcard_manager.find_set_by_id(new_set['id']))
        self.assertEqual(len(self.flashcard_manager.load_data()['sets']), 0)


if __name__ == '__main__':
    unittest.main()
