# FlashForge

A flashcard web app built with Flask and TailwindCSS. Create sets, add cards, flip to reveal answers, and study one card at a time.

## Features

- Create and manage flashcard sets with categories
- Add, edit, and delete cards
- 3D flip animation to reveal answers
- Study mode with single-card navigation
- Favourite cards for focused review
- SQLite storage via Python's stdlib `sqlite3`

## Project Structure

```
flashforge/
├── app.py              # Routes and request handling
├── config.py           # Environment-based configuration
├── models.py           # FlashcardManager — all data logic
├── validators.py       # Input validation
├── test_app.py         # Unit tests
├── static/
│   ├── css/flashcard.css
│   └── js/flashcard.js
└── templates/
    ├── base.html
    ├── index.html
    ├── view_set.html
    ├── new_set.html
    ├── new_card.html
    ├── edit_card.html
    ├── edit_set.html
    ├── favorites.html
    ├── 404.html
    ├── 500.html
    └── partials/
```

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

If you have existing data in `flashcards.json`, run the migration first:

```bash
python migrate_json_to_sqlite.py
```

## Configuration

Set via environment variables:

```bash
SECRET_KEY=your-secret-key
DATA_FILE=flashcards.db
FLASK_DEBUG=True
```

## Running Tests

```bash
python -m unittest test_app.py
```
