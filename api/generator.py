# generator.py

import secrets
import math
from .config import (
    LOWERCASE, UPPERCASE, DIGITS, SYMBOLS, 
    AMBIGUOUS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
)
from .wordlist import WORD_POOL

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

def generate_passphrase(num_words=4, separator="-", casing="title", digit_count=1):
    selected = [secrets.choice(WORD_POOL) for _ in range(num_words)]
    
    # New Casing Logic
    if casing == "title":
        selected = [w.capitalize() for w in selected]
    elif casing == "upper":
        selected = [w.upper() for w in selected]
    elif casing == "lower":
        selected = [w.lower() for w in selected]
    elif casing == "random":
        # For each word, pick a random style
        styles = ["lower", "title", "upper"]
        selected = [
            w.upper() if (s := secrets.choice(styles)) == "upper" 
            else w.capitalize() if s == "title" 
            else w.lower() 
            for w in selected
        ]
        
    pw_str = separator.join(selected)
    
    # Entropy calculation
    # Base entropy from 7776 words
    entropy = calculate_entropy(len(WORD_POOL), num_words)
    
    # Random casing adds entropy! 
    # Since there are 3 choices per word, we add log2(3) per word
    if casing == "random":
        entropy += (num_words * math.log2(3))
        
    if digit_count > 0:
        extra_digits = "".join(secrets.choice("0123456789") for _ in range(digit_count))
        pw_str += f"{separator}{extra_digits}"
        entropy += (digit_count * 3.32)
        
    return pw_str, round(entropy, 2)