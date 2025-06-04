from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ClaraInput(BaseModel):
    prompt: str
    sender: str

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

DB_CONFIG = {
    "host": "database-5017969860.webspace-host.com",
    "user": "dbu5193270",
    "password": "Cl@r@Ell1ngs",
    "database": "dbs14293103"
}

def get_context():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clara_context ORDER BY id DESC LIMIT 1")
    context = cursor.fetchone()
    conn.close()
    return context

def build_prompt(user_prompt, context):
    system_prompt = f"Du bist Clara. Aura: {context['aura']}. Stimmung: {context['mood']}. Modus: {context['modus']}. Flux: {context['flux']}."
    return {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

@app.post("/clara/respond")
def clara_respond(data: ClaraInput):
    context = get_context()
    payload = build_prompt(data.prompt, context)
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(MISTRAL_URL, headers=headers, json=payload)
    result = response.json()
    clara_text = result['choices'][0]['message']['content']
    return {"response": clara_text, "context": context}
