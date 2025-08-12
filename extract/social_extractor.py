# extract/social_extractor.py

import re
import logging
from transformers import pipeline

# Suppress transformers info messages
logging.getLogger("transformers").setLevel(logging.ERROR)

def preprocess_text(text):
    """Clean text for sentiment analysis."""
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text

def fetch_social_sentiment(texts):
    """
    Perform sentiment analysis on a list of texts using transformers.
    Returns a list of sentiment results.
    """
    nlp_sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    cleaned_texts = [preprocess_text(text) for text in texts]
    sentiments = nlp_sentiment(cleaned_texts)
    return sentiments

if __name__ == "__main__":
    sample_texts = [
        "Traffic is horrible!",
        "The city environment is amazing today.",
        "Public transport is really unreliable."
    ]
    sentiments = fetch_social_sentiment(sample_texts)
    for text, sentiment in zip(sample_texts, sentiments):
        print(f"Text: {text}\nSentiment: {sentiment}\n")