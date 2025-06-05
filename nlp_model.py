from textblob import TextBlob

def analyze_sentiment(text):
    if not text:
        return None
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        label = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"

        return {
            "sentiment": {
                "label": label,
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3)
            }
        }
    except Exception as e:
        return { "error": str(e) }
