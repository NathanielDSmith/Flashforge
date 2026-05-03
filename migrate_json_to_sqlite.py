"""
One-time migration: imports flashcards.json into flashcards.db.

Usage:
    python migrate_json_to_sqlite.py
    python migrate_json_to_sqlite.py --json path/to/data.json --db path/to/out.db
"""
import argparse
import json
import os
import sys
from models import FlashcardManager


def migrate(json_path: str, db_path: str) -> None:
    if not os.path.exists(json_path):
        print(f'JSON file not found: {json_path}')
        sys.exit(1)

    if os.path.exists(db_path):
        answer = input(f'{db_path} already exists. Overwrite? [y/N] ').strip().lower()
        if answer != 'y':
            print('Aborted.')
            sys.exit(0)
        os.unlink(db_path)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    manager = FlashcardManager(db_path)
    sets = data.get('sets', [])

    for s in sets:
        category = s.get('category', 'general')
        if not category:
            category = 'japanese' if 'Japanese' in s['title'] else 'programming'

        new_set = manager.create_set(s['title'], s.get('description', ''), category)

        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        for card in s.get('cards', []):
            conn.execute(
                'INSERT INTO flashcards (set_id, question, answer, favorite, created_at) VALUES (?, ?, ?, ?, ?)',
                (new_set['id'], card['question'], card['answer'],
                 1 if card.get('favorite') else 0, card.get('created_at', ''))
            )
        conn.commit()
        conn.close()

    print(f'Migrated {len(sets)} set(s) from {json_path} to {db_path}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate flashcards.json to SQLite')
    parser.add_argument('--json', default='flashcards.json', help='Path to JSON source file')
    parser.add_argument('--db',   default='flashcards.db',   help='Path to SQLite destination')
    args = parser.parse_args()
    migrate(args.json, args.db)
