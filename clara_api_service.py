from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/message")
async def handle_message(request: Request):
    data = await request.json()
    user_input = data.get("user_input", {}).get("text", "")

    # NLP-Analyse
    blob = TextBlob(user_input)
    sentiment = blob.sentiment

    nlp_analysis = {
        "sentiment": {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        }
    }

    # Kontextsynthese
    context = {
        "user_input": {
            "text": user_input,
            "nlp_analysis": nlp_analysis
        }
    }

    # Dummy-Antwort (Platzhalter)
    reply = f"Ich habe dich verstanden. (Stimmung: {sentiment.polarity:.2f}, Subjektivität: {sentiment.subjectivity:.2f})"

    return {
        "response": reply,
        "context": context
    }
