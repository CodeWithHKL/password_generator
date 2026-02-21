# generator.py

import secrets
from config import LOWERCASE, UPPERCASE, DIGITS, SYMBOLS, AMBIGUOUS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH

def generate_secure_password(length=16, avoid_ambiguous=True):
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    if length > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters")

    lowercase = ''.join(c for c in LOWERCASE if c not in AMBIGUOUS) if avoid_ambiguous else LOWERCASE
    uppercase = ''.join(c for c in UPPERCASE if c not in AMBIGUOUS) if avoid_ambiguous else UPPERCASE
    digits = ''.join(c for c in DIGITS if c not in AMBIGUOUS) if avoid_ambiguous else DIGITS
    symbols = SYMBOLS

    all_chars = lowercase + uppercase + digits + symbols

    # Ensure at least one of each type
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill remaining length
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)