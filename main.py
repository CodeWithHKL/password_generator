# main.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from generator import generate_secure_password, generate_passphrase
from config import DEFAULT_PASSWORD_LENGTH, DEFAULT_WORD_COUNT
from typing import Literal

app = FastAPI(title="Enterprise Password API", version="1.3.0")

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
                .code-block { background: #202124; color: #e8eaed; padding: 15px; border-radius: 8px; font-family: monospace; }
                .tag { background: #e8f0fe; color: #1967d2; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🔐 Enterprise Password API</h1>
                <p>Generate high-entropy passphrases or complex character strings.</p>
                
                <h3>Option A: Readable Passphrases <span class="tag">NEW</span></h3>
                <p>Uses a 7,776-word Diceware list. Supports capitalization and digits for legacy compatibility.</p>
                <div class="code-block">GET /generate_phrase?words=4&capitalize=true&include_digit=true</div>
                
                <h3>Option B: Complex Random</h3>
                <p>Standard alphanumeric + symbols generation.</p>
                <div class="code-block">GET /generate?length=24</div>
                
                <br>
                <a href="/docs" style="background:#1a73e8; color:white; padding:12px 24px; text-decoration:none; border-radius:6px;">Open API Documentation</a>
            </div>
        </body>
    </html>
    """

@app.get("/generate_phrase", response_model=PasswordResponse)
def get_readable(
    words: int = Query(4, ge=3, le=10),
    sep: str = Query("-", max_length=1),
    # Added "random" to the allowed list
    casing: Literal["lower", "title", "upper", "random"] = Query("title"),
    digits: int = Query(1, ge=0, le=5)
):
    pw, entropy = generate_passphrase(
        num_words=words, 
        separator=sep, 
        casing=casing, 
        digit_count=digits
    )
    return {"password": pw, "length": len(pw), "entropy_bits": entropy}