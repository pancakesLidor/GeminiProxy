import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# ====== Configuration ======
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_ENDPOINT = os.environ.get("GEMINI_API_ENDPOINT")
SECRET_TOKEN = "Lulita" 
OBFUSCATED_ENDPOINT = "Lidor"       # <- Random-looking path

# ====== Request model ======
class PromptRequest(BaseModel):
    prompt: str

# ====== Endpoint ======
@app.post(f"/{OBFUSCATED_ENDPOINT}")
def proxy_to_gemini(data: PromptRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {"parts": [{"text": data.prompt}]}
        ]
    }

    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# ====== To Run ======
# uvicorn server:app --host 0.0.0.0 --port 8000
