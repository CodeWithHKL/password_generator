# Password Generator API

![License](https://img.shields.io/badge/license-MIT-blue)

A system capable to produce secure, high-entropy password and passphrase combinations built with **FastAPI**. Supports both complex character-based passwords and human-readable Diceware-style passphrases. Authentication via API key is required for all endpoints.

---

## Features

- Generate cryptographically secure passwords using letters, digits, and symbols.
- Optionally avoid ambiguous characters like `O`, `0`, `l`, `1`, `I`.
- Generate readable Diceware-style passphrases.
- Flexible passphrase casing: `lower`, `upper`, `title`, or `random`.
- Configurable passphrase digit suffix.
- Calculate entropy of generated passwords and passphrases.
- Batch generation for multiple passwords in a single request.
- Secure API key authentication.

---

## Table of Contents

- [Installation](#installation)  
- [Configuration](#configuration)  
- [API Endpoints](#api-endpoints)  
- [Usage Examples](#usage-examples)  
- [Entropy Calculation](#entropy-calculation)  
- [License](#license)  

---

# 📦 Installation & Setup

## 1️⃣ Clone repository

```bash
git clone https://github.com/yourusername/hklx-password-api.git
cd hklx-password-api
```

## 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

## 3️⃣ Set the API key environment variable

```
API_KEY="your-secure-api-key"
```

## 4️⃣ Run the API

```
uvicorn hklx_password_api.main:app --reload
The API will be available at http://127.0.0.1:8000
```

---

## ▶️ Configuration

The config.py file contains all configurable options:

```
API_KEY = os.getenv("API_KEY", "123")
API_KEY_NAME = "X-API-Key"

MIN_PASSWORD_LENGTH = 8
DEFAULT_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 128

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
AMBIGUOUS = "O0l1I"

DEFAULT_WORD_COUNT = 4
MIN_WORD_COUNT = 3
MAX_WORD_COUNT = 10
```

---
## API Endpoints

1. Generate Complex Password
   - Endpoint: GET /generate
   - Returns a random password with letters, digits, and symbols.
   - Query Parameters:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| length    | int  | 16      | Password length (8–128) |
| count     | int  | 1       | Number of passwords to generate (1–50) |


2. Generate Readable Passphrase
   - Endpoint: GET /generate_phrase
   - Returns a Diceware-style passphrase..
   - Query Parameters:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| words     | int  | 4       | Number of words (3–10) |
| sep       | str  | "-"     | Separator between words |
| casing    | str  | "title"| Word casing: lower, title, upper, random |
| digits    | int  | 1       | Number of digits to append (0–5) |
| count     | int  | 1       | Number of passphrases (1–50) |

---

## Response:
```
{
  "password": "Apple-Table-Cloud-9",
  "length": 19,
  "entropy_bits": 51.63
}
```

---

## Usage Examples

Using curl

Generate a single complex password:
```
curl -H "X-API-Key: 123" "http://127.0.0.1:8000/generate?length=20"
```

Generate a 5-word passphrase with digits:
curl -H "X-API-Key: 123" "http://127.0.0.1:8000/generate_phrase?words=5&digits=2&casing=random"

---
