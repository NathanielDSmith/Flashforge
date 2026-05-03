import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-secret-do-not-use-in-production'
    DATA_FILE = os.environ.get('DATA_FILE') or 'flashcards.json'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    MAX_QUESTION_LENGTH = 1000
    MAX_ANSWER_LENGTH = 1000

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        secret = os.environ.get('SECRET_KEY')
        if not secret:
            raise RuntimeError(
                'SECRET_KEY environment variable must be set in production. '
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        cls.SECRET_KEY = secret


class TestingConfig(Config):
    TESTING = True
    DATA_FILE = 'test_flashcards.json'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
