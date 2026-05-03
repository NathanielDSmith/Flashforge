import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from config import config
from models import FlashcardManager
from validators import validate_set_data, validate_card_data

logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    return app


app = create_app()
flashcard_manager = FlashcardManager(app.config['DATA_FILE'])


@app.route('/')
def index():
    try:
        data = flashcard_manager.load_data()
        favorite_count = flashcard_manager.get_favorite_count()
        return render_template('index.html', sets=data['sets'], favorite_count=favorite_count)
    except Exception:
        logger.exception('Failed to load index')
        flash('Something went wrong loading your sets. Please try again.', 'error')
        return render_template('index.html', sets=[], favorite_count=0)


@app.route('/set/new', methods=['GET', 'POST'])
def new_set():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        is_valid, error_message = validate_set_data(
            title, description,
            app.config['MAX_TITLE_LENGTH'],
            app.config['MAX_DESCRIPTION_LENGTH']
        )
        if not is_valid:
            flash(error_message, 'error')
            return render_template('new_set.html', title=title, description=description)

        try:
            new_set = flashcard_manager.create_set(title, description)
            if new_set:
                flash('Flashcard set created successfully!', 'success')
                return redirect(url_for('view_set', set_id=new_set['id']))
            flash('Error saving flashcard set. Please try again.', 'error')
        except Exception:
            logger.exception('Failed to create set')
            flash('Something went wrong. Please try again.', 'error')

    return render_template('new_set.html')


@app.route('/set/<int:set_id>')
def view_set(set_id):
    try:
        flashcard_set = flashcard_manager.find_set_by_id(set_id)
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))
        return render_template('view_set.html', flashcard_set=flashcard_set)
    except Exception:
        logger.exception('Failed to load set %s', set_id)
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/set/<int:set_id>/card/new', methods=['GET', 'POST'])
def new_card(set_id):
    try:
        flashcard_set = flashcard_manager.find_set_by_id(set_id)
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))

        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()

            is_valid, error_message = validate_card_data(
                question, answer,
                app.config['MAX_QUESTION_LENGTH'],
                app.config['MAX_ANSWER_LENGTH']
            )
            if not is_valid:
                flash(error_message, 'error')
                return render_template('new_card.html', flashcard_set=flashcard_set,
                                       question=question, answer=answer)

            try:
                new_card = flashcard_manager.add_card(set_id, question, answer)
                if new_card:
                    flash('Card added successfully!', 'success')
                    return redirect(url_for('view_set', set_id=set_id))
                flash('Error saving card. Please try again.', 'error')
            except Exception:
                logger.exception('Failed to add card to set %s', set_id)
                flash('Something went wrong. Please try again.', 'error')

        return render_template('new_card.html', flashcard_set=flashcard_set)
    except Exception:
        logger.exception('Failed to load set %s for new card', set_id)
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/set/<int:set_id>/card/<int:card_id>/edit', methods=['GET', 'POST'])
def edit_card(set_id, card_id):
    try:
        flashcard_set = flashcard_manager.find_set_by_id(set_id)
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))

        card = flashcard_manager.find_card_by_id(flashcard_set, card_id)
        if not card:
            flash('Card not found.', 'error')
            return redirect(url_for('view_set', set_id=set_id))

        if request.method == 'POST':
            question = request.form.get('question', '').strip()
            answer = request.form.get('answer', '').strip()

            is_valid, error_message = validate_card_data(
                question, answer,
                app.config['MAX_QUESTION_LENGTH'],
                app.config['MAX_ANSWER_LENGTH']
            )
            if not is_valid:
                flash(error_message, 'error')
                return render_template('edit_card.html', flashcard_set=flashcard_set, card=card,
                                       question=question, answer=answer)

            if flashcard_manager.update_card(set_id, card_id, question, answer):
                flash('Card updated successfully!', 'success')
                return redirect(url_for('view_set', set_id=set_id))
            flash('Error updating card. Please try again.', 'error')

        return render_template('edit_card.html', flashcard_set=flashcard_set, card=card)
    except Exception:
        logger.exception('Failed to edit card %s in set %s', card_id, set_id)
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('view_set', set_id=set_id))


@app.route('/card/<int:set_id>/<int:card_id>/toggle-favorite', methods=['POST'])
def toggle_favorite(set_id, card_id):
    try:
        success, new_favorite_status = flashcard_manager.toggle_favorite(set_id, card_id)
        if success:
            message = 'Added to favorites!' if new_favorite_status else 'Removed from favorites!'
            return jsonify({'success': True, 'favorite': new_favorite_status, 'message': message})
        return jsonify({'success': False, 'message': 'Card not found'}), 404
    except Exception:
        logger.exception('Failed to toggle favorite for card %s in set %s', card_id, set_id)
        return jsonify({'success': False, 'message': 'Something went wrong'}), 500


@app.route('/favorites')
def favorites():
    try:
        favorite_cards = flashcard_manager.get_favorite_cards()
        return render_template('favorites.html', favorite_cards=favorite_cards)
    except Exception:
        logger.exception('Failed to load favorites')
        flash('Something went wrong loading your favorites.', 'error')
        return render_template('favorites.html', favorite_cards=[])


@app.route('/set/<int:set_id>/edit', methods=['GET', 'POST'])
def edit_set(set_id):
    try:
        flashcard_set = flashcard_manager.find_set_by_id(set_id)
        if not flashcard_set:
            flash('Flashcard set not found.', 'error')
            return redirect(url_for('index'))

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()

            is_valid, error_message = validate_set_data(
                title, description,
                app.config['MAX_TITLE_LENGTH'],
                app.config['MAX_DESCRIPTION_LENGTH']
            )
            if not is_valid:
                flash(error_message, 'error')
                return render_template('edit_set.html', flashcard_set=flashcard_set,
                                       title=title, description=description)

            if flashcard_manager.update_set(set_id, title, description):
                flash('Set updated successfully!', 'success')
                return redirect(url_for('view_set', set_id=set_id))
            flash('Error updating set. Please try again.', 'error')

        return render_template('edit_set.html', flashcard_set=flashcard_set)
    except Exception:
        logger.exception('Failed to edit set %s', set_id)
        flash('Something went wrong. Please try again.', 'error')
        return redirect(url_for('view_set', set_id=set_id))


@app.route('/set/<int:set_id>/delete', methods=['POST'])
def delete_set(set_id):
    try:
        if flashcard_manager.delete_set(set_id):
            flash('Flashcard set deleted.', 'success')
        else:
            flash('Flashcard set not found.', 'error')
    except Exception:
        logger.exception('Failed to delete set %s', set_id)
        flash('Something went wrong. Please try again.', 'error')
    return redirect(url_for('index'))


@app.route('/set/<int:set_id>/card/<int:card_id>/delete', methods=['POST'])
def delete_card(set_id, card_id):
    try:
        if flashcard_manager.delete_card(set_id, card_id):
            flash('Card deleted.', 'success')
        else:
            flash('Card not found.', 'error')
    except Exception:
        logger.exception('Failed to delete card %s in set %s', card_id, set_id)
        flash('Something went wrong. Please try again.', 'error')
    return redirect(url_for('view_set', set_id=set_id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
