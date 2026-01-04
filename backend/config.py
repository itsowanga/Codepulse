"""
CodePulse Configuration
Centralized configuration and path management for the application
"""

import os
from pathlib import Path

# Project root directory (two levels up from backend/)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directory for database and generated files
DATA_DIR = PROJECT_ROOT / 'data'

# Database file path
DATABASE_PATH = DATA_DIR / 'activity.db'

# Frontend directory
FRONTEND_DIR = PROJECT_ROOT / 'frontend'

# Docs directory
DOCS_DIR = PROJECT_ROOT / 'docs'

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Flask configuration
class Config:
    """Base configuration"""
    DATABASE = str(DATABASE_PATH)
    CORS_ORIGINS = ["*"]
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'  # Use in-memory database for tests

# Get the active config based on environment
def get_config():
    """Get the active configuration"""
    env = os.getenv('FLASK_ENV', 'production').lower()
    if env == 'development':
        return DevelopmentConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return ProductionConfig()

# Ensure data directory exists
def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Get database connection helper
def get_db_path():
    """Get the database path"""
    ensure_data_dir()
    return str(DATABASE_PATH)
