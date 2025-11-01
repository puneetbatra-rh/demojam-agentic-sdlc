import os

class Config:
    """
    Configuration class for the application.
    """
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_NAME = os.environ.get('DB_NAME', 'home_loan_db')

    API_GATEWAY_URL = os.environ.get('API_GATEWAY_URL', 'http://localhost:5000')

    @staticmethod
    def get_db_url():
        """
        Returns the database URL.
        """
        return f"mysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}"