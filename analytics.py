import re
from collections import Counter

import pandas as pd
from nltk.corpus import stopwords

from inference import predict_sentiment


# ==========================================
# Sentiment Prediction
# ==========================================

def analyze_reviews(df):

    if df.empty:
        return df

    sentiments = []
    confidences = []

    for review in df["content"]:

        review = str(review)

        sentiment, confidence = predict_sentiment(review)

        sentiments.append(sentiment)
        confidences.append(confidence)

    result_df = df.copy()

    result_df["predicted_sentiment"] = sentiments
    result_df["confidence"] = confidences

    return result_df


# ==========================================
# Sentiment Summary
# ==========================================

def get_sentiment_summary(df):

    counts = df["predicted_sentiment"].value_counts()

    percentages = (
        df["predicted_sentiment"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    return counts, percentages


# ==========================================
# Language Detection
# ==========================================

def detect_languages(df):
    # Copy to avoid mutating the caller's DataFrame in-place (Bug 5 fix)
    df = df.copy()

    languages = []

    for text in df["content"]:

        text = str(text)

        # Hindi
        if re.search(r'[\u0900-\u097F]', text):
            languages.append("Hindi")

        # Tamil
        elif re.search(r'[\u0B80-\u0BFF]', text):
            languages.append("Tamil")

        # Telugu
        elif re.search(r'[\u0C00-\u0C7F]', text):
            languages.append("Telugu")

        # Kannada
        elif re.search(r'[\u0C80-\u0CFF]', text):
            languages.append("Kannada")

        # Malayalam
        elif re.search(r'[\u0D00-\u0D7F]', text):
            languages.append("Malayalam")

        # Bengali
        elif re.search(r'[\u0980-\u09FF]', text):
            languages.append("Bengali")

        else:
            languages.append("English")

    df["language"] = languages

    return df


# ==========================================
# Language Distribution
# ==========================================

def get_language_distribution(df):

    return df["language"].value_counts()


# ==========================================
# Stopwords
# ==========================================

CUSTOM_STOPWORDS = set(stopwords.words("english"))

CUSTOM_STOPWORDS.update({

    # ── App names / brand words ──────────────────────────────────────────
    "app", "apps", "phonepe", "paytm", "gpay", "google", "whatsapp",
    "instagram", "amazon", "flipkart", "meesho", "zomato", "swiggy",
    "netflix", "youtube", "spotify", "telegram",

    # ── Generic positive filler ──────────────────────────────────────────
    "good", "nice", "super", "best", "awesome", "excellent", "great",
    "love", "liked", "helpful", "useful", "amazing", "wonderful",
    "fantastic", "perfect", "brilliant", "better", "smooth",

    # ── Generic negative filler ──────────────────────────────────────────
    "bad", "worst", "horrible", "terrible", "pathetic", "useless",
    "rubbish", "waste", "poor", "worst",

    # ── Common function words / verbs ────────────────────────────────────
    "very", "really", "just", "also", "using", "used", "uses", "use",
    "make", "made", "making", "work", "works", "working", "worked",
    "give", "given", "giving", "takes", "take", "taken", "taking",
    "need", "needs", "needed", "want", "wants", "wanted", "said",
    "going", "come", "came", "coming", "back", "done", "doing",
    "know", "knew", "think", "thought", "feels", "feel", "felt",
    "seem", "seems", "seemed", "look", "looks", "looked", "show",
    "open", "opened", "close", "closed", "send", "sent", "receive",
    "received", "install", "installed", "uninstall", "uninstalled",
    "download", "downloaded", "update", "updated", "upgrade",

    # ── Numbers / counters ───────────────────────────────────────────────
    "one", "two", "three", "four", "five", "star", "stars", "time",
    "times", "day", "days", "year", "years", "month", "months",

    # ── Modal / auxiliary verbs ──────────────────────────────────────────
    "get", "got", "gets", "can", "could", "would", "should", "must",
    "may", "might", "shall", "will",

    # ── Prepositions / conjunctions ──────────────────────────────────────
    "but", "not", "this", "that", "from", "for", "with", "when",
    "where", "what", "which", "who", "how", "why", "then", "than",
    "after", "before", "because", "since", "while", "even", "only",
    "still", "never", "always", "every", "many", "much", "more",
    "most", "some", "any", "all", "they", "their", "there", "these",
    "those", "into", "onto", "upon", "over", "under",

    # ── Indian filler / politeness ───────────────────────────────────────
    "hai", "kar", "acha", "accha", "aap", "pls", "please", "sir",
    "bro", "thankyou", "thanks", "bhai", "yaar", "iska", "uska",
    "mera", "meri", "karo", "karna", "nahi", "nhi",

    # ── Review meta-words ────────────────────────────────────────────────
    "review", "rating", "rated", "gave", "give", "star", "stars",
    "feedback", "recommend", "recommended",
})


# ==========================================
# Keyword Extraction
# ==========================================

def _extract_keywords_from_list(texts):
    """Extract meaningful keywords from a list of text strings."""
    words = []

    for text in texts:

        text = str(text).lower()

        # Minimum 4 chars to filter out 3-letter noise (pay, bad, try, two…)
        tokens = re.findall(
            r"\b[a-z]{4,}\b",
            text
        )

        words.extend(tokens)

    words = [
        word
        for word in words
        if word not in CUSTOM_STOPWORDS
    ]

    return Counter(words).most_common(10)


# ==========================================
# Top Complaints
# ==========================================

def get_top_complaints(df):

    negative_reviews = df[
        (df["predicted_sentiment"] == "negative")
        &
        (df["confidence"] >= 0.80)
    ]

    return _extract_keywords_from_list(
        negative_reviews["content"]
    )


# ==========================================
# Top Praises
# ==========================================

def get_top_praises(df):

    positive_reviews = df[
        (df["predicted_sentiment"] == "positive")
        &
        (df["confidence"] >= 0.80)
    ]

    return _extract_keywords_from_list(
        positive_reviews["content"]
    )


# ==========================================
# Average Confidence
# ==========================================

def get_average_confidence(df):

    return round(
        df["confidence"].mean(),
        4
    )

def get_dashboard_metrics(df):

    counts, percentages = get_sentiment_summary(df)

    metrics = {
        "positive": float(percentages.get("positive", 0)),
        "negative": float(percentages.get("negative", 0)),
        "neutral": float(percentages.get("neutral", 0)),
        "avg_confidence": float(get_average_confidence(df))
    }

    return metrics


# ==========================================
# Wrapper Functions for App
# ==========================================

def calculate_sentiment_distribution(df):
    """Calculate sentiment distribution from reviews dataframe."""
    counts, percentages = get_sentiment_summary(df)
    return {
        "positive": float(percentages.get("positive", 0)),
        "negative": float(percentages.get("negative", 0)),
        "neutral": float(percentages.get("neutral", 0)),
    }


def calculate_language_distribution(df):
    """Calculate language distribution from reviews dataframe."""
    df_with_lang = detect_languages(df)
    return df_with_lang["language"].value_counts().to_dict()


def extract_keywords(df, sentiment_type="positive"):
    """
    Extract keywords from a sentiment-filtered dataframe.

    Args:
        df: Dataframe with 'content' column
        sentiment_type: 'positive' or 'negative' (for context, not filtering)

    Returns:
        List of (keyword, count) tuples
    """
    if df.empty:
        return []

    texts = df["content"].tolist()

    words = []

    for text in texts:
        text = str(text).lower()
        # Minimum 4 chars — eliminates 3-letter noise like 'pay', 'bad', 'try'
        tokens = re.findall(r"\b[a-z]{4,}\b", text)
        words.extend(tokens)

    words = [
        word
        for word in words
        if word not in CUSTOM_STOPWORDS
    ]

    return Counter(words).most_common(10)