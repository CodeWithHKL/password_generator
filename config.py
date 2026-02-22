# config.py
import os

API_KEY = os.getenv("API_KEY", "123")  # Vercel will override this
API_KEY_NAME = "X-API-Key"

MIN_PASSWORD_LENGTH = 8
DEFAULT_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 128

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

AMBIGUOUS = "O0l1I"

# New Passphrase Settings
DEFAULT_WORD_COUNT = 4
MIN_WORD_COUNT = 3
MAX_WORD_COUNT = 10