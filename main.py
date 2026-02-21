# main.py

from fastapi import FastAPI, HTTPException, Query
from generator import generate_secure_password
from config import DEFAULT_PASSWORD_LENGTH

app = FastAPI(
    title="Enterprise Secure Password API",
    description="Generate cryptographically secure passwords with policy enforcement",
    version="1.0.0"
)

@app.get("/generate", summary="Generate a secure password")
def get_password(
    length: int = Query(DEFAULT_PASSWORD_LENGTH, ge=8, le=128),
    avoid_ambiguous: bool = True
):
    try:
        password = generate_secure_password(length=length, avoid_ambiguous=avoid_ambiguous)
        return {"password": password, "length": length}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate_batch", summary="Generate multiple secure passwords")
def get_password_batch(
    count: int = Query(5, ge=1, le=100),
    length: int = Query(DEFAULT_PASSWORD_LENGTH, ge=8, le=128),
    avoid_ambiguous: bool = True
):
    passwords = []
    for _ in range(count):
        passwords.append(generate_secure_password(length=length, avoid_ambiguous=avoid_ambiguous))
    return {"passwords": passwords, "count": count, "length": length}