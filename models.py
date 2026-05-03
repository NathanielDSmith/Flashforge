import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Generator, List, Optional, Tuple


def _dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict:
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class FlashcardManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _db(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = _dict_factory
        conn.execute('PRAGMA foreign_keys = ON')
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._db() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS flashcard_sets (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    title       TEXT    NOT NULL,
                    description TEXT    NOT NULL DEFAULT '',
                    category    TEXT    NOT NULL DEFAULT 'general',
                    created_at  TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS flashcards (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    set_id     INTEGER NOT NULL REFERENCES flashcard_sets(id) ON DELETE CASCADE,
                    question   TEXT    NOT NULL,
                    answer     TEXT    NOT NULL,
                    favorite   INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT    NOT NULL
                );
            """)

    def _get_cards_for_set(self, conn: sqlite3.Connection, set_id: int) -> List[Dict]:
        rows = conn.execute(
            'SELECT * FROM flashcards WHERE set_id = ? ORDER BY id', (set_id,)
        ).fetchall()
        for row in rows:
            row['favorite'] = bool(row['favorite'])
        return rows

    def _row_to_set(self, conn: sqlite3.Connection, row: Dict) -> Dict:
        row['cards'] = self._get_cards_for_set(conn, row['id'])
        return row

    def load_data(self) -> Dict:
        with self._db() as conn:
            sets = conn.execute(
                'SELECT * FROM flashcard_sets ORDER BY id'
            ).fetchall()
            for s in sets:
                s['cards'] = self._get_cards_for_set(conn, s['id'])
            return {'sets': sets}

    def find_set_by_id(self, set_id: int) -> Optional[Dict]:
        with self._db() as conn:
            row = conn.execute(
                'SELECT * FROM flashcard_sets WHERE id = ?', (set_id,)
            ).fetchone()
            if row is None:
                return None
            return self._row_to_set(conn, row)

    def find_card_by_id(self, flashcard_set: Dict, card_id: int) -> Optional[Dict]:
        return next((c for c in flashcard_set['cards'] if c['id'] == card_id), None)

    def create_set(self, title: str, description: str = '', category: str = 'general') -> Optional[Dict]:
        created_at = datetime.now().isoformat()
        with self._db() as conn:
            cursor = conn.execute(
                'INSERT INTO flashcard_sets (title, description, category, created_at) VALUES (?, ?, ?, ?)',
                (title, description, category, created_at)
            )
            return {
                'id': cursor.lastrowid,
                'title': title,
                'description': description,
                'category': category,
                'created_at': created_at,
                'cards': [],
            }

    def update_set(self, set_id: int, title: str, description: str = '', category: str = 'general') -> bool:
        with self._db() as conn:
            cursor = conn.execute(
                'UPDATE flashcard_sets SET title = ?, description = ?, category = ? WHERE id = ?',
                (title, description, category, set_id)
            )
            return cursor.rowcount > 0

    def delete_set(self, set_id: int) -> bool:
        with self._db() as conn:
            cursor = conn.execute('DELETE FROM flashcard_sets WHERE id = ?', (set_id,))
            return cursor.rowcount > 0

    def add_card(self, set_id: int, question: str, answer: str) -> Optional[Dict]:
        created_at = datetime.now().isoformat()
        with self._db() as conn:
            exists = conn.execute(
                'SELECT id FROM flashcard_sets WHERE id = ?', (set_id,)
            ).fetchone()
            if not exists:
                return None
            cursor = conn.execute(
                'INSERT INTO flashcards (set_id, question, answer, favorite, created_at) VALUES (?, ?, ?, 0, ?)',
                (set_id, question, answer, created_at)
            )
            return {
                'id': cursor.lastrowid,
                'set_id': set_id,
                'question': question,
                'answer': answer,
                'favorite': False,
                'created_at': created_at,
            }

    def update_card(self, set_id: int, card_id: int, question: str, answer: str) -> bool:
        with self._db() as conn:
            cursor = conn.execute(
                'UPDATE flashcards SET question = ?, answer = ? WHERE id = ? AND set_id = ?',
                (question, answer, card_id, set_id)
            )
            return cursor.rowcount > 0

    def delete_card(self, set_id: int, card_id: int) -> bool:
        with self._db() as conn:
            cursor = conn.execute(
                'DELETE FROM flashcards WHERE id = ? AND set_id = ?', (card_id, set_id)
            )
            return cursor.rowcount > 0

    def toggle_favorite(self, set_id: int, card_id: int) -> Tuple[bool, bool]:
        with self._db() as conn:
            row = conn.execute(
                'SELECT favorite FROM flashcards WHERE id = ? AND set_id = ?',
                (card_id, set_id)
            ).fetchone()
            if row is None:
                return False, False
            new_value = 0 if row['favorite'] else 1
            conn.execute(
                'UPDATE flashcards SET favorite = ? WHERE id = ? AND set_id = ?',
                (new_value, card_id, set_id)
            )
            return True, bool(new_value)

    def get_favorite_cards(self) -> List[Dict]:
        with self._db() as conn:
            rows = conn.execute("""
                SELECT
                    f.id, f.question, f.answer, f.favorite, f.created_at,
                    s.id    AS set_id,
                    s.title AS set_title
                FROM flashcards f
                JOIN flashcard_sets s ON s.id = f.set_id
                WHERE f.favorite = 1
                ORDER BY s.id, f.id
            """).fetchall()
            return [
                {
                    'card': {
                        'id':         row['id'],
                        'question':   row['question'],
                        'answer':     row['answer'],
                        'favorite':   bool(row['favorite']),
                        'created_at': row['created_at'],
                    },
                    'set': {
                        'id':    row['set_id'],
                        'title': row['set_title'],
                    },
                }
                for row in rows
            ]

    def get_favorite_count(self) -> int:
        with self._db() as conn:
            row = conn.execute(
                'SELECT COUNT(*) AS n FROM flashcards WHERE favorite = 1'
            ).fetchone()
            return row['n']
