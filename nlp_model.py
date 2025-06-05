from transformers import pipeline

# Initialisiere das Sentiment-Analyse-Modell
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="oliverguhr/german-sentiment-bert"
)

def analyze_sentiment(text):
    if not text:
        return None
    try:
        result = sentiment_analyzer(text)[0]
        return {
            "sentiment": {
                "label": result["label"],
                "score": round(result["score"], 4)
            }
        }
    except Exception as e:
        return { "error": str(e) }
