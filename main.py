# main.py

from fastapi import FastAPI, HTTPException, Query, Security, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from generator import generate_secure_password, generate_passphrase
from config import DEFAULT_PASSWORD_LENGTH, DEFAULT_WORD_COUNT
import config
from typing import Literal, List, Union

app = FastAPI(title="Enterprise Password API", version="1.3.0")

# --- AUTHENTICATION ---
api_key_header = APIKeyHeader(name=config.API_KEY_NAME, auto_error=False)

async def get_api_key(header_value: str = Security(api_key_header)):
    if header_value == config.API_KEY:
        return header_value
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key"
    )

class PasswordResponse(BaseModel):
    password: str
    length: int
    entropy_bits: float

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing():
    return """
    <html>
        <head>
            <title>Secure Gen API</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f0f2f5; }
                .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
                h1 { color: #1a73e8; }
                .code-block { background: #202124; color: #e8eaed; padding: 15px; border-radius: 8px; font-family: monospace; overflow-x: auto; }
                .tag { background: #e8f0fe; color: #1967d2; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
                li { margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🔐 Enterprise Password API</h1>
                <p>High-performance password generation with mathematically proven entropy.</p>
                
                <h3>1. Readable Passphrases <span class="tag">DICEWARE</span></h3>
                <p>Customizable word-based passwords. Great for humans.</p>
                <div class="code-block">GET /generate_phrase?words=5&casing=random&digits=2</div>
                
                <h3>2. Complex Strings <span class="tag">ALPHANUMERIC</span></h3>
                <p>Random characters, numbers, and symbols. Great for service accounts.</p>
                <div class="code-block">GET /generate?length=32</div>
                
                <br>
                <a href="/docs" style="background:#1a73e8; color:white; padding:12px 24px; text-decoration:none; border-radius:6px; display: inline-block;">Explore Interactive Docs</a>
            </div>
        </body>
    </html>
    """

# --- ENDPOINT 1: COMPLEX CHARACTERS ---
@app.get("/generate", 
         response_model=Union[PasswordResponse, List[PasswordResponse]], 
         dependencies=[Depends(get_api_key)])
def get_complex(
    length: int = Query(DEFAULT_PASSWORD_LENGTH, ge=8, le=128),
    count: int = Query(1, ge=1, le=50) # Allow up to 50 at once
):
    results = []
    for _ in range(count):
        pw, entropy = generate_secure_password(length=length)
        results.append({"password": pw, "length": length, "entropy_bits": entropy})
    
    return results[0] if count == 1 else results

# --- ENDPOINT 2: READABLE PASSPHRASE ---
@app.get(
    "/generate_phrase", 
    response_model=Union[PasswordResponse, List[PasswordResponse]],
    dependencies=[Depends(get_api_key)])
def get_readable(
    words: int = Query(4, ge=3, le=10),
    sep: str = Query("-", max_length=1),
    casing: Literal["lower", "title", "upper", "random"] = Query("title"),
    digits: int = Query(1, ge=0, le=5),
    count: int = Query(1, ge=1, le=50) # Allow up to 50 at once
):
    results = []
    for _ in range(count):
        pw, entropy = generate_passphrase(
            num_words=words, 
            separator=sep, 
            casing=casing, 
            digit_count=digits
        )
        results.append({"password": pw, "length": len(pw), "entropy_bits": entropy})
        
    return results[0] if count == 1 else results