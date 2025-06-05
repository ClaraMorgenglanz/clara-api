from fastapi import FastAPI
import mysql.connector
from transformers import pipeline
from textblob import TextBlob

app = FastAPI()

# NLP-Modell laden (transformers)
sentiment_analyzer = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")

# Datenbankverbindung
def get_db_connection():
    return mysql.connector.connect(
        host="database-5017969860.webspace-host.com",
        user="dbu5193270",
        password="Cl@r@Ell1ngs",
        database="dbs14293103"
    )

@app.get("/")
def home():
    return {"message": "Clara API läuft"}

@app.get("/nlp/test")
def test_nlp():
    text = "Ich bin sehr enttäuscht von deinem Verhalten."
    result = sentiment_analyzer(text)[0]
    return {
        "text": text,
        "sentiment": result["label"],
        "score": round(result["score"], 4)
    }

@app.get("/nlp/textblob")
def test_textblob():
    tb = TextBlob("Das ist ein fantastischer Tag!")
    return {
        "polarity": tb.sentiment.polarity,
        "subjectivity": tb.sentiment.subjectivity
    }

@app.get("/db/test")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return {"status": "OK", "tables": tables}
    except Exception as e:
        return {"status": "ERROR", "details": str(e)}
