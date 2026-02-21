# main.py

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from generator import generate_secure_password
from config import DEFAULT_PASSWORD_LENGTH

app = FastAPI(
    title="Enterprise Secure Password API",
    description="Generate cryptographically secure passwords with entropy calculation.",
    version="1.1.0"
)

class PasswordResponse(BaseModel):
    password: str
    length: int
    entropy_bits: float

class BatchResponse(BaseModel):
    passwords: List[PasswordResponse]
    count: int

@app.get("/generate", response_model=PasswordResponse, summary="Generate a secure password")
def get_password(
    length: int = Query(DEFAULT_PASSWORD_LENGTH, ge=8, le=128, description="Length of the password"),
    avoid_ambiguous: bool = Query(True, description="Exclude similar-looking characters (e.g., l, 1, O, 0)")
):
    try:
        pw, entropy = generate_secure_password(length=length, avoid_ambiguous=avoid_ambiguous)
        return {"password": pw, "length": length, "entropy_bits": entropy}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate_batch", response_model=BatchResponse, summary="Generate multiple secure passwords")
def get_password_batch(
    count: int = Query(5, ge=1, le=100, description="Number of passwords to generate"),
    length: int = Query(DEFAULT_PASSWORD_LENGTH, ge=8, le=128),
    avoid_ambiguous: bool = True
):
    results = []
    for _ in range(count):
        pw, entropy = generate_secure_password(length=length, avoid_ambiguous=avoid_ambiguous)
        results.append({"password": pw, "length": length, "entropy_bits": entropy})
    
    return {"passwords": results, "count": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)