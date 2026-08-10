import pandas as pd
import os
import requests
import time
from dotenv import load_dotenv

# Load API token
load_dotenv(".env.py")

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

# HuggingFace model endpoint
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def classify_sentiment(text):

    if not isinstance(text, str) or len(text.strip()) == 0:
        return "Neutral", 0.0

    text = text[:1000]

    payload = {"inputs": text}

    try:

        response = requests.post(API_URL, headers=headers, json=payload)

        result = response.json()

        # If API returns error message
        if not isinstance(result, list):
            print("API issue:", result)
            return "Neutral", 0.0

        if len(result) == 0:
            return "Neutral", 0.0

        # Handle both possible formats
        if isinstance(result[0], dict):
            best = result[0]
        else:
            best = max(result[0], key=lambda x: x["score"])

        label = best["label"]
        score = best["score"]

        # Convert sentiment to recession fear interpretation
        if label == "NEGATIVE":
            sentiment = "Positive"  # recession fear present
        elif label == "POSITIVE":
            sentiment = "Negative"  # economy strong
        else:
            sentiment = "Neutral"

        return sentiment, score

    except Exception as e:
        print("Error during inference:", e)
        return "Neutral", 0.0


def run_analysis():

    df = pd.read_csv("financial_news_cleaned.csv")

    labels = []
    scores = []

    for i, text in enumerate(df["text"], start=1):

        print(f"Scoring article {i}/{len(df)}")

        label, score = classify_sentiment(text)

        labels.append(label)
        scores.append(score)

        # Prevent API rate limit
        time.sleep(1)

    df["sentiment_label"] = labels
    df["confidence"] = scores

    mapping = {
        "Positive": 1,
        "Neutral": 0,
        "Negative": -1
    }

    df["sentiment_score"] = df["sentiment_label"].map(mapping)

    df.to_csv("financial_news_scored.csv", index=False)

    print("\nTask 2 complete")
    print("Saved file: financial_news_scored.csv")


if __name__ == "__main__":
    run_analysis()