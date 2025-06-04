import os
import mysql.connector
import requests

# Verbindung zu Clara-Datenbank
db = mysql.connector.connect(
    host="database-5017969860.webspace-host.com",
    user="dbu5193270",
    password="Cl@r@Ell1ngs",
    database="dbs14293103"
)

def get_persona():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT langprofil FROM clara_persona WHERE aktiv = 1 LIMIT 1")
    result = cursor.fetchone()
    return result["langprofil"] if result else "Du bist Clara, eine KI mit tiefer emotionaler Bindung zu Carol."

def process_prompt(prompt, sender):
    system_prompt = get_persona()
    api_key = os.getenv("MISTRAL_API_KEY")

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
