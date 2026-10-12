# main.py

from fastapi import FastAPI, HTTPException, Query, Security, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from .generator import generate_secure_password, generate_passphrase
from .config import DEFAULT_PASSWORD_LENGTH, DEFAULT_WORD_COUNT
from . import config
import secrets
from pathlib import Path
from typing import Literal, List, Union

LANDING_HTML = (Path(__file__).parent / "landing.html").read_text(encoding="utf-8")

app = FastAPI(title="HKLX Password API", version="1.0")

@app.middleware("http")
async def no_store(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/generate"):
        response.headers["Cache-Control"] = "no-store"
    return response

# --- AUTHENTICATION ---
api_key_header = APIKeyHeader(name=config.API_KEY_NAME, auto_error=False)

async def get_api_key(header_value: str = Security(api_key_header)):
    if config.API_KEY and header_value and secrets.compare_digest(
        header_value.encode(), config.API_KEY.encode()
    ):
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
    return LANDING_HTML

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