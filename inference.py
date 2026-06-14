# Inference module for BharatReview
# Model loads lazily on first call to get_model() — never at import time.

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import os

# Use local model during development; fall back to HuggingFace Hub on deployment
MODEL_PATH = (
    "models/muril_sentiment"
    if os.path.isdir("models/muril_sentiment")
    else "BharatReview/muril-sentiment"
)

id2label = {
    0: "negative",
    1: "neutral",
    2: "positive",
}

# Module-level cache — populated on first call to get_model()
_model     = None
_tokenizer = None


def get_model():
    """
    Lazily load and cache the MuRIL model + tokenizer.
    First call: loads from disk / Hub (~950 MB).
    Subsequent calls: returns cached instances instantly.
    """
    global _model, _tokenizer
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model     = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()
    return _model, _tokenizer


def load_model():
    """Backward-compatible wrapper — returns just the model."""
    model, _ = get_model()
    return model


def predict_sentiment(text: str):
    """
    Predict sentiment for a single text string.
    Returns: (label, confidence) — label is 'positive', 'negative', or 'neutral'
    """
    model, tokenizer = get_model()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs   = torch.softmax(outputs.logits, dim=-1)

    probs_np   = probs.cpu().numpy()[0]
    prediction = int(np.argmax(probs_np))
    confidence = float(np.max(probs_np))

    return id2label[prediction], confidence


def predict_batch(model_arg, texts: list):
    """
    Predict sentiment for a list of texts.
    model_arg is kept for backward compatibility but unused.
    Returns: {"labels": [...], "scores": [...]}
    """
    labels, scores = [], []
    for text in texts:
        label, score = predict_sentiment(text)
        labels.append(label)
        scores.append(score)
    return {"labels": labels, "scores": scores}