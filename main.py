from fastapi import FastAPI
from nlp_model import analyze_sentiment
from textblob import TextBlob
import mysql.connector
import os

app = FastAPI()


@app.get("/")
def root_check():
    return {"message": "Clara API läuft"}


@app.get("/diagnose/api")
def check_api():
    return {"status": "ok", "info": "API erreichbar"}


@app.get("/diagnose/nlp")
def check_nlp():
    try:
        test = analyze_sentiment("Ich bin sehr glücklich.")
        return {"status": "ok", "result": test}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/diagnose/textblob")
def check_textblob():
    try:
        blob = TextBlob("Test")
        lang = blob.detect_language() if hasattr(blob, "detect_language") else "unbekannt"
        return {"status": "ok", "language": lang}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/diagnose/database")
def check_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "")
        )
        conn.close()
        return {"status": "ok", "info": "Verbindung erfolgreich"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/clara")
def clara_response(message: str):
    try:
        sentiment = analyze_sentiment(message)
        return {"antwort": f"Clara hat verstanden: '{message}'", "emotion": sentiment}
    except Exception as e:
        return {"error": str(e)}
