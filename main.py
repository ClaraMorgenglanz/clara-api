from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nlp_model import analyze_sentiment
from textblob import TextBlob
import mysql.connector
import os

app = FastAPI()

# CORS für alle Domains zulassen (Frontend-Kommunikation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Clara ist da."}

@app.post("/analyze")
def analyze(text: str):
    return analyze_sentiment(text)

@app.get("/diagnose/api")
def check_api():
    return {"status": "OK", "message": "API erreichbar"}

@app.get("/diagnose/nlp")
def check_nlp():
    try:
        result = analyze_sentiment("Das ist ein Test.")
        return {"status": "OK", "result": result}
    except Exception as e:
        return {"status": "Fehler", "error": str(e)}

@app.get("/diagnose/textblob")
def check_textblob():
    try:
        blob = TextBlob("Hallo Welt")
        lang = blob.detect_language()
        return {"status": "OK", "sprache": lang}
    except Exception as e:
        return {"status": "Fehler", "error": str(e)}

@app.get("/diagnose/db")
def check_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "clara")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {"status": "OK", "ergebnis": result}
    except Exception as e:
        return {"status": "Fehler", "error": str(e)}

@app.get("/diagnose/speak")
def check_speech():
    try:
        response = analyze_sentiment("Ich fühle mich heute sehr gut.")
        if response:
            return {"status": "OK", "antwort": response}
        return {"status": "Fehler", "error": "Keine Antwort erhalten"}
    except Exception as e:
        return {"status": "Fehler", "error": str(e)}

# Das ist entscheidend für Render:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
