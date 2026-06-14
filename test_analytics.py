from scraper import fetch_reviews_for_app

from analytics import (
    analyze_reviews,
    detect_languages,
    get_sentiment_summary,
    get_language_distribution,
    get_top_complaints,
    get_top_praises,
    get_average_confidence
)


# ==========================================
# Choose App
# ==========================================

app_id = "com.phonepe.app"


# ==========================================
# Fetch Reviews
# ==========================================

df = fetch_reviews_for_app(
    app_id,
    max_reviews=500
)

print("\nReviews Shape:")
print(df.shape)


# ==========================================
# Sentiment Analysis
# ==========================================

df = analyze_reviews(df)

df = detect_languages(df)


# ==========================================
# Summary
# ==========================================

counts, percentages = get_sentiment_summary(df)

print("\nSentiment Counts:")
print(counts)

print("\nSentiment Percentages:")
print(percentages)

print("\nAverage Confidence:")
print(get_average_confidence(df))


# ==========================================
# Language Distribution
# ==========================================

print("\nLanguage Distribution:")
print(
    get_language_distribution(df)
)


# ==========================================
# Complaints
# ==========================================

print("\nTop Complaints:")
print(
    get_top_complaints(df)
)


# ==========================================
# Praises
# ==========================================

print("\nTop Praises:")
print(
    get_top_praises(df)
)


# ==========================================
# Sample Predictions
# ==========================================

print("\nSample Predictions:")

print(
    df[
        [
            "content",
            "predicted_sentiment",
            "confidence"
        ]
    ].head(10)
)