# generator.py

import random
from config import LOWERCASE, UPPERCASE, DIGITS, SYMBOLS, AMBIGUOUS, MIN_PASSWORD_LENGTH

def generate_secure_password(length=16, avoid_ambiguous=True):
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password length must be at least {MIN_PASSWORD_LENGTH} characters.")
    
    # Remove ambiguous characters if needed
    lowercase = ''.join(c for c in LOWERCASE if c not in AMBIGUOUS) if avoid_ambiguous else LOWERCASE
    uppercase = ''.join(c for c in UPPERCASE if c not in AMBIGUOUS) if avoid_ambiguous else UPPERCASE
    digits = ''.join(c for c in DIGITS if c not in AMBIGUOUS) if avoid_ambiguous else DIGITS
    symbols = SYMBOLS  # usually symbols are fine
    
    all_chars = lowercase + uppercase + digits + symbols

    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the remaining length
    password += random.choices(all_chars, k=length - 4)

    # Shuffle to remove patterns
    random.shuffle(password)

    return ''.join(password)