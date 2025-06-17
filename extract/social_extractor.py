# extract/social_extractor.py

from transformers import pipeline

def fetch_social_sentiment(texts):
    """
    Perform sentiment analysis on a list of texts using transformers.
    Returns a list of sentiment results.
    """
    nlp_sentiment = pipeline("sentiment-analysis")
    sentiments = [nlp_sentiment(text)[0] for text in texts]
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
