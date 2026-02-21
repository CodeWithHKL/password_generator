# main.py

from generator import generate_secure_password
from config import DEFAULT_PASSWORD_LENGTH

def main():
    print("=== Advanced Secure Password Generator ===")
    length = input(f"Enter password length (default {DEFAULT_PASSWORD_LENGTH}): ")
    
    try:
        length = int(length) if length.strip() else DEFAULT_PASSWORD_LENGTH
    except ValueError:
        length = DEFAULT_PASSWORD_LENGTH

    password = generate_secure_password(length)
    print(f"Generated Password: {password}")

    # Optional: generate multiple passwords quickly
    generate_more = input("Generate 5 more passwords? (y/n): ").lower()
    if generate_more == 'y':
        for _ in range(5):
            print(generate_secure_password(length))

if __name__ == "__main__":
    main()