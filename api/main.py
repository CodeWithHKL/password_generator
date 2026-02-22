# main.py

from fastapi import FastAPI, HTTPException, Query, Security, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from .generator import generate_secure_password, generate_passphrase
from .config import DEFAULT_PASSWORD_LENGTH, DEFAULT_WORD_COUNT
from . import config
from typing import Literal, List, Union

app = FastAPI(title="HKLX Password API", version="1.0")

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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HKLX Password Generator API</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
            body { 
                background-color: #050505; 
                font-family: 'Inter', sans-serif;
            }
            .glass { 
                background: rgba(255, 255, 255, 0.03); 
                backdrop-filter: blur(20px); 
                border: 1px solid rgba(255, 255, 255, 0.08); 
            }
            .orange-glow {
                box-shadow: 0 0 40px -10px rgba(255, 107, 0, 0.3);
            }
            .scanline {
                width: 100%;
                height: 2px;
                background: rgba(255, 107, 0, 0.1);
                position: absolute;
                animation: scan 4s linear infinite;
            }
            @keyframes scan {
                0% { top: 0; }
                100% { top: 100%; }
            }
        </style>
    </head>
    <body class="text-white min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
        
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-[#ff6b00]/10 blur-[120px] rounded-full pointer-events-none"></div>

        <div class="fixed top-8 right-8 z-50">
            <a href="https:hklxportfolio.vercel.app" target="_blank" rel="noopener noreferrer" 
               class="w-12 h-12 bg-[#ff6b00] rounded-xl flex items-center justify-center font-black text-black text-xl hover:bg-orange-500 hover:rotate-12 transition-all duration-300 shadow-lg shadow-orange-600/20">
                H
            </a>
        </div>

        <div class="max-w-2xl w-full glass p-10 rounded-[2.5rem] shadow-2xl relative overflow-hidden orange-glow">
            <div class="scanline"></div>
            
            <div class="flex flex-col md:flex-row md:items-center gap-6 mb-12">
                <div class="bg-[#ff6b00] p-4 rounded-2xl w-fit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                </div>
                <div>
                    <h1 class="text-4xl font-black uppercase tracking-tighter leading-none">
                        Password Gen <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#ff6b00] to-orange-400">API</span>
                    </h1>
                    <p class="text-gray-500 text-xs font-bold uppercase tracking-[0.2em] mt-2">Secure Entropy Systems v1.0</p>
                </div>
            </div>

            <div class="space-y-8">
                <section>
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="text-[10px] font-black uppercase tracking-[0.3em] text-[#ff6b00]">Complex Strings</h3>
                        <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest px-2 py-1 bg-white/5 rounded">Alphanumeric</span>
                    </div>
                    <div class="bg-black/60 rounded-2xl p-5 font-mono text-sm border border-white/5 group hover:border-[#ff6b00]/50 transition-all">
                        <span class="text-[#ff6b00] font-bold">GET</span> <span class="text-gray-400">/generate?length=32</span>
                    </div>
                </section>

                <section>
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="text-[10px] font-black uppercase tracking-[0.3em] text-[#ff6b00]">Passphrases</h3>
                        <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest px-2 py-1 bg-white/5 rounded">Diceware</span>
                    </div>
                    <div class="bg-black/60 rounded-2xl p-5 font-mono text-sm border border-white/5 group hover:border-[#ff6b00]/50 transition-all">
                        <span class="text-[#ff6b00] font-bold">GET</span> <span class="text-gray-400">/generate_phrase?words=5</span>
                    </div>
                </section>
            </div>

            <div class="mt-12 space-y-4">
                <a href="/docs" class="block w-full text-center py-5 bg-white text-black rounded-2xl font-black text-xs uppercase tracking-[0.2em] hover:bg-[#ff6b00] hover:text-white transition-all shadow-xl active:scale-95">
                    Launch Documentation
                </a>
                <div class="flex items-center justify-center gap-4 py-2">
                    <div class="h-px bg-white/10 flex-1"></div>
                    <span class="text-[9px] text-gray-600 font-black uppercase tracking-widest">Auth Required</span>
                    <div class="h-px bg-white/10 flex-1"></div>
                </div>
            </div>
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