# generator.py

import secrets
import math
from config import (
    LOWERCASE, UPPERCASE, DIGITS, SYMBOLS, 
    AMBIGUOUS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
)

def calculate_entropy(length: int, pool_size: int) -> float:
    """Calculates the Shannon entropy of the password."""
    if pool_size <= 0:
        return 0.0
    return round(length * math.log2(pool_size), 2)

def generate_secure_password(length=16, avoid_ambiguous=True):
    if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}")

    # Define the pools
    pools = [LOWERCASE, UPPERCASE, DIGITS, SYMBOLS]
    
    # Filter ambiguous characters if requested
    if avoid_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]

    # Ensure no pool is empty (safety check)
    pools = [p for p in pools if p]
    all_chars = "".join(pools)
    
    # 1. Guarantee at least one character from each active pool
    password = [secrets.choice(p) for p in pools]

    # 2. Fill the rest of the length
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_chars))

    # 3. Securely shuffle the result
    # We use secrets.SystemRandom() which is cryptographically secure
    rng = secrets.SystemRandom()
    rng.shuffle(password)
    
    password_str = "".join(password)
    entropy = calculate_entropy(len(password_str), len(all_chars))
    
    return password_str, entropy