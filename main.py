# main.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from generator import generate_secure_password
from config import DEFAULT_PASSWORD_LENGTH

app = FastAPI(
    title="Enterprise Secure Password API",
    description="Generate cryptographically secure passwords with entropy calculation.",
    version="1.1.0"
)

# Data Models
class PasswordResponse(BaseModel):
    password: str
    length: int
    entropy_bits: float

class BatchResponse(BaseModel):
    passwords: List[PasswordResponse]
    count: int

# --- GUI / LANDING PAGE ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def welcome_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Enterprise Password API</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 40px 20px; background-color: #f9fafb; color: #111827; }
                .container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
                h1 { color: #2563eb; display: flex; align-items: center; gap: 10px; }
                code { background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em; color: #db2777; }
                .btn { display: inline-block; background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 1rem; transition: background 0.2s; }
                .btn:hover { background: #1d4ed8; }
                .endpoint-card { border-left: 4px solid #2563eb; background: #eff6ff; padding: 1rem; margin: 1rem 0; border-radius: 0 6px 6px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔐 Enterprise Password API</h1>
                <p>A cryptographically secure password generation service using Python's <code>secrets</code> module and Shannon entropy scoring.</p>
                
                <div class="endpoint-card">
                    <strong>Single Password:</strong> <code>GET /generate?length=16</code>
                </div>
                <div class="endpoint-card">
                    <strong>Batch Generation:</strong> <code>GET /generate_batch?count=10&length=20</code>
                </div>

                <p>To test the parameters and see full technical specifications, visit the interactive documentation:</p>
                <a href="/docs" class="btn">Explore API Documentation (Swagger UI)</a>
            </div>
        </body>
    </html>
    """

# --- API ENDPOINTS ---

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