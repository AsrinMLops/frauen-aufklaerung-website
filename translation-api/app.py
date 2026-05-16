from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class TranslationRequest(BaseModel):
    text: str
    direction: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    if request.direction == "de_to_ku":
        prompt = f"Übersetze folgenden deutschen Text ins Kurdische (Sorani). Gib nur die Übersetzung zurück:\n\n{request.text}"
    else:
        prompt = f"Translate the following Kurdish (Sorani) text to German. Only return the translation:\n\n{request.text}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return {
        "original": request.text,
        "translation": response.text,
        "direction": request.direction
    }

@app.get("/")
def home():
    return {"message": "Uebersetzungs-API laeuft!"}
