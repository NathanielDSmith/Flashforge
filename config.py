import os
from typing import Dict, Any

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DATA_FILE = os.environ.get('DATA_FILE') or 'flashcards.json'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    MAX_QUESTION_LENGTH = 1000
    MAX_ANSWER_LENGTH = 1000

    CARDS_PER_PAGE = 12
    STUDY_MODE_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'

class TestingConfig(Config):
    TESTING = True
    DATA_FILE = 'test_flashcards.json'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 