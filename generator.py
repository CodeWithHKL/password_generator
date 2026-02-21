# generator.py

import secrets
import math
from config import (
    LOWERCASE, UPPERCASE, DIGITS, SYMBOLS, 
    AMBIGUOUS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
)
from wordlist import WORD_POOL

def calculate_entropy(pool_size: int, length: int) -> float:
    if pool_size <= 0: return 0.0
    return round(length * math.log2(pool_size), 2)

def generate_secure_password(length=16, avoid_ambiguous=True):
    # (Existing character-based logic remains the same)
    pools = [LOWERCASE, UPPERCASE, DIGITS, SYMBOLS]
    if avoid_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]
    pools = [p for p in pools if p]
    all_chars = "".join(pools)
    password = [secrets.choice(p) for p in pools]
    password += [secrets.choice(all_chars) for _ in range(length - len(password))]
    secrets.SystemRandom().shuffle(password)
    pw_str = "".join(password)
    return pw_str, calculate_entropy(len(all_chars), len(pw_str))

def generate_passphrase(num_words=4, separator="-", capitalize=True, include_digit=True):
    """
    Generates a readable passphrase.
    Optional 'Enterprise' complexity: Capitalization and a random digit.
    """
    selected = [secrets.choice(WORD_POOL) for _ in range(num_words)]
    
    if capitalize:
        selected = [w.capitalize() for w in selected]
        
    pw_str = separator.join(selected)
    
    # Base entropy from word selection
    entropy = calculate_entropy(len(WORD_POOL), num_words)
    
    if include_digit:
        digit = secrets.choice("0123456789")
        pw_str += f"{separator}{digit}"
        # Adding 1 of 10 digits adds log2(10) bits
        entropy += 3.32
        
    return pw_str, round(entropy, 2)