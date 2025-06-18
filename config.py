import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DATA_FILE = os.environ.get('DATA_FILE') or 'flashcards.json'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Validation settings
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    MAX_QUESTION_LENGTH = 1000
    MAX_ANSWER_LENGTH = 1000
    
    # UI settings
    CARDS_PER_PAGE = 12
    STUDY_MODE_ENABLED = True
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATA_FILE = 'test_flashcards.json'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 