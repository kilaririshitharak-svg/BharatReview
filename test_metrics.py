from scraper import fetch_reviews_for_app
from analytics import (
    analyze_reviews,
    get_dashboard_metrics
)

df = fetch_reviews_for_app(
    "com.phonepe.app",
    max_reviews=100
)

df = analyze_reviews(df)

metrics = get_dashboard_metrics(df)

print(metrics)