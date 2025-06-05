from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# NLP-Modell vorbereiten
sentiment_analyzer = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-lib")

app = FastAPI()

# CORS (damit z. B. Web-Frontend zugreifen kann)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenstruktur für eingehende Daten
class UserInput(BaseModel):
    text: str

@app.post("/analyze/")
async def analyze_input(user_input: UserInput):
    text = user_input.text.strip()
    if not text:
        return {"error": "Kein Text übermittelt."}

    # NLP-Analyse
    result = sentiment_analyzer(text)[0]  # gibt {"label": ..., "score": ...}
    sentiment = {
        "label": result["label"],
        "score": round(result["score"], 3)
    }

    # Ausgabe (später Übergabe an mood_service, rule_engine etc.)
    return {
        "text": text,
        "nlp_analysis": {
            "sentiment": sentiment
        }
    }

@app.get("/")
async def root():
    return {"message": "Clara API mit NLP ist aktiv."}
