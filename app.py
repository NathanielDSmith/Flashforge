from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from config import config

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    return app

app = create_app()

# Configuration
DATA_FILE = app.config['DATA_FILE']

class FlashcardManager:
    """Manages flashcard data operations"""
    
    @staticmethod
    def load_data() -> Dict:
        """Load flashcard data from JSON file"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
        return {'sets': []}
    
    @staticmethod
    def save_data(data: Dict) -> bool:
        """Save flashcard data to JSON file"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False
    
    @staticmethod
    def get_next_id(items: List) -> int:
        """Get the next available ID for a list of items"""
        return max([item.get('id', 0) for item in items], default=0) + 1
    
    @staticmethod
    def find_set_by_id(set_id: int) -> Optional[Dict]:
        """Find a flashcard set by ID"""
        data = FlashcardManager.load_data()
        return next((s for s in data['sets'] if s['id'] == set_id), None)
    
    @staticmethod
    def find_card_by_id(flashcard_set: Dict, card_id: int) -> Optional[Dict]:
        """Find a card by ID within a flashcard set"""
        return next((c for c in flashcard_set['cards'] if c['id'] == card_id), None)

def validate_set_data(title: str, description: str = '') -> tuple[bool, str]:
    """Validate flashcard set data"""
    if not title or not title.strip():
        return False, "Set title is required"
    if len(title.strip()) > app.config['MAX_TITLE_LENGTH']:
        return False, f"Set title must be less than {app.config['MAX_TITLE_LENGTH']} characters"
    if description and len(description) > app.config['MAX_DESCRIPTION_LENGTH']:
        return False, f"Description must be less than {app.config['MAX_DESCRIPTION_LENGTH']} characters"
    return True, ""

def validate_card_data(question: str, answer: str) -> tuple[bool, str]:
    """Validate flashcard data"""
    if not question or not question.strip():
        return False, "Question is required"
    if not answer or not answer.strip():
        return False, "Answer is required"
    if len(question.strip()) > app.config['MAX_QUESTION_LENGTH']:
        return False, f"Question must be less than {app.config['MAX_QUESTION_LENGTH']} characters"
    if len(answer.strip()) > app.config['MAX_ANSWER_LENGTH']:
        return False, f"Answer must be less than {app.config['MAX_ANSWER_LENGTH']} characters"
    return True, ""

@app.route('/')
def index():
    """Home page showing all flashcard sets"""
    try:
        data = FlashcardManager.load_data()
        return render_template('index.html', sets=data['sets'])
    except Exception as e:
        flash(f"Error loading flashcard sets: {str(e)}", 'error')
        return render_template('index.html', sets=[])

@app.route('/set/new', methods=['GET', 'POST'])
def new_set():
    """Create a new flashcard set"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        # Validate input
        is_valid, error_message = validate_set_data(title, description)
        if not is_valid:
            flash(error_message, 'error')
            return render_template('new_set.html', title=title, description=description)
        
        try:
            data = FlashcardManager.load_data()
            new_set = {
                'id': FlashcardManager.get_next_id(data['sets']),
                'title': title,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'cards': []
            }
            data['sets'].append(new_set)
            
            if FlashcardManager.save_data(data):
                flash('Flashcard set created successfully!', 'success')
                return redirect(url_for('view_set', set_id=new_set['id']))
            else:
                flash('Error saving flashcard set. Please try again.', 'error')
        except Exception as e:
            flash(f'Error creating flashcard set: {str(e)}', 'error')
    
    return render_template('new_set.html')

@app.route('/set/<int:set_id>')
def view_set(set_id):
    """View a specific flashcard set"""
    try:
        flashcard_set = FlashcardManager.find_set_by_id(set_id)
        
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))
        
        return render_template('view_set.html', flashcard_set=flashcard_set)
    except Exception as e:
        flash(f'Error loading flashcard set: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/set/<int:set_id>/card/new', methods=['GET', 'POST'])
def new_card(set_id):
    """Add a new card to a set"""
    try:
        flashcard_set = FlashcardManager.find_set_by_id(set_id)
        
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()
            
            # Validate input
            is_valid, error_message = validate_card_data(question, answer)
            if not is_valid:
                flash(error_message, 'error')
                return render_template('new_card.html', flashcard_set=flashcard_set, question=question, answer=answer)
            
            try:
                data = FlashcardManager.load_data()
                
                # Find the set in the data structure
                flashcard_set_in_data = None
                for set_item in data['sets']:
                    if set_item['id'] == set_id:
                        flashcard_set_in_data = set_item
                        break
                
                if not flashcard_set_in_data:
                    flash('Flashcard set not found.', 'error')
                    return redirect(url_for('index'))
                
                new_card = {
                    'id': FlashcardManager.get_next_id(flashcard_set_in_data['cards']),
                    'question': question,
                    'answer': answer,
                    'created_at': datetime.now().isoformat()
                }
                flashcard_set_in_data['cards'].append(new_card)
                
                if FlashcardManager.save_data(data):
                    flash('Card added successfully!', 'success')
                    return redirect(url_for('view_set', set_id=set_id))
                else:
                    flash('Error saving card. Please try again.', 'error')
            except Exception as e:
                flash(f'Error adding card: {str(e)}', 'error')
        
        return render_template('new_card.html', flashcard_set=flashcard_set)
    except Exception as e:
        flash(f'Error loading flashcard set: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/set/<int:set_id>/delete', methods=['POST'])
def delete_set(set_id):
    """Delete a flashcard set"""
    try:
        data = FlashcardManager.load_data()
        original_count = len(data['sets'])
        data['sets'] = [s for s in data['sets'] if s['id'] != set_id]
        
        if len(data['sets']) < original_count:
            if FlashcardManager.save_data(data):
                flash('Flashcard set deleted successfully!', 'success')
            else:
                flash('Error saving changes. Please try again.', 'error')
        else:
            flash('Flashcard set not found.', 'error')
    except Exception as e:
        flash(f'Error deleting flashcard set: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/set/<int:set_id>/card/<int:card_id>/delete', methods=['POST'])
def delete_card(set_id, card_id):
    """Delete a card from a set"""
    try:
        data = FlashcardManager.load_data()
        
        # Find the set in the data structure
        flashcard_set = None
        for set_item in data['sets']:
            if set_item['id'] == set_id:
                flashcard_set = set_item
                break
        
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))
        
        # Remove the card from the set
        original_count = len(flashcard_set['cards'])
        flashcard_set['cards'] = [c for c in flashcard_set['cards'] if c['id'] != card_id]
        
        if len(flashcard_set['cards']) < original_count:
            if FlashcardManager.save_data(data):
                flash('Card deleted successfully!', 'success')
            else:
                flash('Error saving changes. Please try again.', 'error')
        else:
            flash('Card not found.', 'error')
    except Exception as e:
        flash(f'Error deleting card: {str(e)}', 'error')
    
    return redirect(url_for('view_set', set_id=set_id))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG']) 