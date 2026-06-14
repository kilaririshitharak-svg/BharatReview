import nltk
# Auto-download NLTK data on fresh environments (e.g. HuggingFace Spaces)
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

from scraper import (
    search_apps,
    fetch_reviews_for_app,
    extract_app_id_from_url,
)
from analytics import (
    calculate_sentiment_distribution,
    calculate_language_distribution,
    extract_keywords,
)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="BharatReview — Indian App Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Lazy-load the 950MB MuRIL model with caching
@st.cache_resource(show_spinner="🤖 Loading MuRIL model… (first time only, please wait)")
def load_model_cached():
    from inference import get_model
    return get_model()

# ══════════════════════════════════════════════════════════════════════════════
# DARK THEME CSS — Full Glassmorphism UI
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }

    /* ── Hide default Streamlit decoration ──────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ── Hero header ────────────────────────────────────────────────────── */
    .hero-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.15) 100%);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.4rem 0;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }

    /* ── Section cards ──────────────────────────────────────────────────── */
    .section-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(8px);
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Metric cards ───────────────────────────────────────────────────── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); border-color: rgba(129,140,248,0.4); }
    .metric-label { font-size: 0.78rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #e2e8f0; }
    .metric-value.positive { color: #4ade80; }
    .metric-value.negative { color: #f87171; }
    .metric-value.neutral  { color: #facc15; }
    .metric-sub { font-size: 0.75rem; color: #64748b; margin-top: 0.2rem; }

    /* ── Keyword cards ──────────────────────────────────────────────────── */
    .complaint-card {
        background: rgba(239,68,68,0.1);
        border-left: 3px solid #ef4444;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: background 0.2s;
    }
    .complaint-card:hover { background: rgba(239,68,68,0.18); }
    .complaint-word { font-weight: 600; color: #fca5a5; font-size: 0.95rem; }
    .complaint-bar {
        flex: 1; margin: 0 12px;
        height: 4px; border-radius: 2px;
        background: rgba(239,68,68,0.2);
        overflow: hidden;
    }
    .complaint-bar-fill { height: 100%; background: #ef4444; border-radius: 2px; }
    .kw-count { color: #94a3b8; font-size: 0.8rem; white-space: nowrap; }

    .praise-card {
        background: rgba(34,197,94,0.1);
        border-left: 3px solid #22c55e;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: background 0.2s;
    }
    .praise-card:hover { background: rgba(34,197,94,0.18); }
    .praise-word { font-weight: 600; color: #86efac; font-size: 0.95rem; }
    .praise-bar {
        flex: 1; margin: 0 12px;
        height: 4px; border-radius: 2px;
        background: rgba(34,197,94,0.2);
        overflow: hidden;
    }
    .praise-bar-fill { height: 100%; background: #22c55e; border-radius: 2px; }

    .neutral-card {
        background: rgba(250,204,21,0.08);
        border-left: 3px solid #facc15;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #fde68a;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ── Sidebar ────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: rgba(15,15,26,0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.5rem;
    }
    .sidebar-brand-title {
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-stat {
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #94a3b8;
    }
    .sidebar-stat-val { color: #e2e8f0; font-weight: 600; }

    /* ── Plotly dark override ────────────────────────────────────────────── */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* ── Streamlit overrides ────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
        box-shadow: 0 4px 15px rgba(99,102,241,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(99,102,241,0.45);
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
    }
    .stSlider { padding: 0.5rem 0; }
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    .stAlert { border-radius: 10px; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1, h2, h3 { color: #e2e8f0 !important; }
    p, label, .stMarkdown { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🚀</div>
        <div class="sidebar-brand-title">BharatReview</div>
        <div style="font-size:0.75rem; color:#64748b; margin-top:0.3rem;">Indian App Review Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    input_mode = st.radio(
        "📥 Input Method",
        ["Google Play URL", "App Name Search"],
        help="URL recommended for highest accuracy"
    )

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.6rem;'>About</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-stat"><span>🤖 Model</span><span class="sidebar-stat-val">MuRIL</span></div>
    <div class="sidebar-stat"><span>🎯 Accuracy</span><span class="sidebar-stat-val">98.46%</span></div>
    <div class="sidebar-stat"><span>🌐 Languages</span><span class="sidebar-stat-val">6+</span></div>
    <div class="sidebar-stat"><span>📦 Max Reviews</span><span class="sidebar-stat-val">1,000</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if "analysis_done" in st.session_state and st.session_state.analysis_done:
        rdf = st.session_state.reviews_df
        sd  = st.session_state.sentiment_dist
        st.markdown("<div style='font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.6rem;'>Last Analysis</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sidebar-stat"><span>📝 Reviews</span><span class="sidebar-stat-val">{len(rdf)}</span></div>
        <div class="sidebar-stat"><span>😊 Positive</span><span class="sidebar-stat-val" style="color:#4ade80">{sd.get('positive',0):.1f}%</span></div>
        <div class="sidebar-stat"><span>😠 Negative</span><span class="sidebar-stat-val" style="color:#f87171">{sd.get('negative',0):.1f}%</span></div>
        <div class="sidebar-stat"><span>😐 Neutral</span><span class="sidebar-stat-val" style="color:#facc15">{sd.get('neutral',0):.1f}%</span></div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Results", use_container_width=True):
            for key in ["analysis_done", "reviews_df", "sentiment_dist", "lang_dist",
                        "complaints", "praises", "selected_app_id", "search_results", "last_search_query"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem; color:#475569; text-align:center;'>Built with MuRIL · Streamlit · Plotly<br>© 2024 BharatReview</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero-header">
    <div class="hero-title">🚀 BharatReview</div>
    <p class="hero-sub">
        Multilingual Indian App Review Intelligence · Analyze Google Play reviews in English, Hindi, Tamil, Telugu & more
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════

if "selected_app_id" not in st.session_state:
    st.session_state.selected_app_id = None

selected_app_id = st.session_state.selected_app_id

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — APP SELECTION
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-title">📱 Step 1 — Select Your App</div>', unsafe_allow_html=True)

if input_mode == "Google Play URL":
    st.info("✅ **RECOMMENDED**: Direct, accurate, no guesswork")

    user_input = st.text_input(
        "Paste Google Play URL:",
        placeholder="https://play.google.com/store/apps/details?id=com.whatsapp",
        help="Example: https://play.google.com/store/apps/details?id=com.whatsapp"
    )

    if user_input:
        app_id = extract_app_id_from_url(user_input.strip())
        if app_id:
            st.success(f"✅ App ID extracted: `{app_id}`")
            selected_app_id = app_id
            st.session_state.selected_app_id = app_id
            st.session_state.search_results = pd.DataFrame()
        else:
            st.error("❌ Could not extract valid app ID from URL. Check the URL format.")
            selected_app_id = None
            st.session_state.selected_app_id = None

else:
    st.warning("⚠️ Search mode: Results may be inaccurate for some apps. Verify your selection.")

    selected_app_id = None

    with st.form(key="app_search_form"):
        search_query = st.text_input(
            "Search app name:",
            placeholder="e.g., WhatsApp, Instagram, PhonePe",
        )
        search_submitted = st.form_submit_button("🔍 Search")

    if search_submitted and search_query.strip():
        with st.spinner("Searching..."):
            apps_df = search_apps(search_query.strip(), max_results=5)
        st.session_state.search_results = apps_df
        st.session_state.last_search_query = search_query.strip()

    if "last_search_query" in st.session_state and "search_results" in st.session_state:

        apps_df = st.session_state.search_results

        if apps_df.empty:
            st.error("❌ No results found. Try another search term or use Google Play URL.")
        else:
            valid_apps = apps_df[apps_df["has_app_id"] == True].copy()

            if valid_apps.empty:
                st.error("❌ No valid app IDs found. Try a different search.")
            else:
                st.subheader("Search Results:")

                results_display = valid_apps[["rank", "title", "developer", "confidence", "confidence_level"]].copy()

                def format_confidence(conf):
                    level = "HIGH" if conf >= 0.90 else "MEDIUM" if conf >= 0.70 else "LOW"
                    if level == "HIGH":   return f"🟢 {level} ({conf:.2f})"
                    elif level == "MEDIUM": return f"🟡 {level} ({conf:.2f})"
                    else:                 return f"🔴 {level} ({conf:.2f})"

                results_display["Confidence"] = valid_apps["confidence"].apply(format_confidence)
                results_display = results_display[["rank", "title", "developer", "Confidence"]]
                st.dataframe(results_display, use_container_width=True, hide_index=True)

                low_conf = valid_apps[valid_apps["confidence"] < 0.70]
                if not low_conf.empty:
                    st.warning(f"⚠️ {len(low_conf)} result(s) with LOW confidence. Verify before proceeding.")

                selected_rank = st.selectbox(
                    "Select the correct app (by rank):",
                    options=valid_apps["rank"].values,
                    format_func=lambda r: valid_apps[valid_apps["rank"] == r]["title"].values[0]
                )

                selected_row = valid_apps[valid_apps["rank"] == selected_rank].iloc[0]
                selected_app_id = selected_row["appId"]
                st.session_state.selected_app_id = selected_app_id

                if selected_row["confidence"] < 0.80:
                    st.warning(f"⚠️ **Low Confidence ({selected_row['confidence']:.2f})**: Use Google Play URL for better accuracy.")
                else:
                    st.success(f"✅ Selected: **{selected_row['title']}** ({selected_row['confidence_level']})")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — FETCH & ANALYZE
# ══════════════════════════════════════════════════════════════════════════════

if selected_app_id:
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Step 2 — Fetch & Analyze Reviews</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        review_count = st.slider("Number of reviews to fetch:", 50, 1000, 200, step=50)
    with col2:
        st.write("")
        st.write("")
        fetch_button = st.button("🚀 Fetch & Analyze", use_container_width=True)

    if fetch_button:
        progress_bar = st.progress(0, text="⏳ Fetching reviews from Google Play…")
        try:
            reviews_df = fetch_reviews_for_app(
                st.session_state.selected_app_id,
                max_reviews=review_count
            )
            progress_bar.progress(30, text="✅ Reviews fetched! Filtering…")

            if reviews_df.empty:
                st.error("❌ Could not fetch reviews. App ID may be invalid.")
                progress_bar.empty()
            else:
                before = len(reviews_df)
                reviews_df = reviews_df[
                    reviews_df["content"].notna() &
                    (reviews_df["content"].astype(str).str.strip() != "") &
                    (reviews_df["content"].astype(str).str.strip().str.lower() != "none")
                ].copy().reset_index(drop=True)
                filtered = before - len(reviews_df)
                if filtered > 0:
                    st.info(f"ℹ️ Skipped {filtered} empty/null review(s).")

                progress_bar.progress(50, text="🤖 Running MuRIL sentiment analysis…")

                model, tokenizer = load_model_cached()
                from inference import predict_batch

                # Run with per-review progress updates
                texts = reviews_df["content"].tolist()
                labels, scores = [], []
                chunk = max(1, len(texts) // 20)  # update progress every 5%
                for i, text in enumerate(texts):
                    from inference import predict_sentiment
                    label, score = predict_sentiment(text)
                    labels.append(label)
                    scores.append(score)
                    if i % chunk == 0:
                        pct = 50 + int((i / len(texts)) * 45)
                        progress_bar.progress(pct, text=f"🤖 Analysing review {i+1}/{len(texts)}…")

                reviews_df["predicted_sentiment"] = labels
                reviews_df["confidence"] = scores

                progress_bar.progress(98, text="📊 Computing analytics…")

                sentiment_dist = calculate_sentiment_distribution(reviews_df)
                lang_dist      = calculate_language_distribution(reviews_df)
                complaints     = extract_keywords(reviews_df[reviews_df["predicted_sentiment"] == "negative"], "negative")
                praises        = extract_keywords(reviews_df[reviews_df["predicted_sentiment"] == "positive"], "positive")

                st.session_state.reviews_df     = reviews_df
                st.session_state.sentiment_dist = sentiment_dist
                st.session_state.lang_dist      = lang_dist
                st.session_state.complaints     = complaints
                st.session_state.praises        = praises
                st.session_state.analysis_done  = True

                progress_bar.progress(100, text="✅ Analysis complete!")
                st.success(f"✅ Analyzed {len(reviews_df)} reviews successfully!")

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            progress_bar.empty()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — RESULTS & INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

if "analysis_done" in st.session_state and st.session_state.analysis_done:
    reviews_df    = st.session_state.reviews_df
    sentiment_dist = st.session_state.sentiment_dist
    lang_dist     = st.session_state.lang_dist
    complaints    = st.session_state.complaints
    praises       = st.session_state.praises

    st.markdown("---")
    st.markdown('<div class="hero-title" style="font-size:1.6rem; margin-bottom:1.2rem;">📈 Results & Insights</div>', unsafe_allow_html=True)

    # ── Metric Cards ─────────────────────────────────────────────────────────
    pos_pct  = sentiment_dist.get("positive", 0)
    neg_pct  = sentiment_dist.get("negative", 0)
    neu_pct  = sentiment_dist.get("neutral",  0)
    avg_conf = reviews_df["confidence"].mean()
    neu_count = len(reviews_df[reviews_df["predicted_sentiment"] == "neutral"])

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">📝 Total Reviews</div>
            <div class="metric-value">{len(reviews_df):,}</div>
            <div class="metric-sub">Analyzed</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">😊 Positive</div>
            <div class="metric-value positive">{pos_pct:.1f}%</div>
            <div class="metric-sub">{int(len(reviews_df)*pos_pct/100):,} reviews</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">😠 Negative</div>
            <div class="metric-value negative">{neg_pct:.1f}%</div>
            <div class="metric-sub">{int(len(reviews_df)*neg_pct/100):,} reviews</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🎯 Avg Confidence</div>
            <div class="metric-value">{avg_conf:.1%}</div>
            <div class="metric-sub">Model certainty</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Sentiment Pie + Language Bar ───────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Sentiment Distribution")
        fig = go.Figure(data=[go.Pie(
            labels=["Positive", "Negative", "Neutral"],
            values=[pos_pct, neg_pct, neu_pct],
            marker=dict(
                colors=["#22c55e", "#ef4444", "#facc15"],
                line=dict(color="#0f0f1a", width=2)
            ),
            textposition="auto",
            textfont=dict(size=13, color="white"),
            hole=0.35,
        )])
        fig.update_layout(
            height=320,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            legend=dict(font=dict(color="#94a3b8")),
            margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🌍 Language Distribution")
        lang_data = pd.DataFrame(
            list(lang_dist.items()), columns=["Language", "Count"]
        ).sort_values("Count", ascending=True).head(10)

        fig = px.bar(
            lang_data, x="Count", y="Language", orientation="h",
            color="Count", color_continuous_scale=["#1e3a5f", "#3b82f6", "#818cf8"],
            text="Count",
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            height=300, showlegend=False, coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis=dict(title="Reviews", gridcolor="rgba(255,255,255,0.05)", color="#64748b"),
            yaxis=dict(title="", color="#94a3b8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Rating vs Sentiment (NEW) ─────────────────────────────────────
    st.subheader("⭐ Rating vs Sentiment Breakdown")

    if "rating" in reviews_df.columns:
        rating_sentiment = (
            reviews_df.groupby(["rating", "predicted_sentiment"])
            .size()
            .reset_index(name="count")
        )
        color_map = {"positive": "#22c55e", "negative": "#ef4444", "neutral": "#facc15"}

        fig = px.bar(
            rating_sentiment, x="rating", y="count", color="predicted_sentiment",
            color_discrete_map=color_map, barmode="group",
            labels={"rating": "Star Rating", "count": "Number of Reviews", "predicted_sentiment": "Sentiment"},
        )
        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            legend=dict(font=dict(color="#94a3b8"), title_font=dict(color="#94a3b8")),
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(title="Star Rating (1–5)", gridcolor="rgba(255,255,255,0.05)", color="#64748b", tickmode="linear"),
            yaxis=dict(title="Reviews", gridcolor="rgba(255,255,255,0.05)", color="#64748b"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Rating column not available in this dataset.")

    # ── Row 3: Top Complaints + Top Praises ──────────────────────────────────
    col1, col2 = st.columns(2)

    max_complaint = complaints[0][1] if complaints else 1
    max_praise    = praises[0][1]    if praises    else 1

    with col1:
        st.subheader("🚨 Top Complaints")
        if complaints:
            for word, count in complaints[:10]:
                pct = int((count / max_complaint) * 100)
                st.markdown(
                    f'<div class="complaint-card">'
                    f'<span class="complaint-word">🔴 {word.capitalize()}</span>'
                    f'<div class="complaint-bar"><div class="complaint-bar-fill" style="width:{pct}%"></div></div>'
                    f'<span class="kw-count">{count}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No complaint keywords found")

    with col2:
        st.subheader("👍 Top Praises")
        if praises:
            for word, count in praises[:10]:
                pct = int((count / max_praise) * 100)
                st.markdown(
                    f'<div class="praise-card">'
                    f'<span class="praise-word">🟢 {word.capitalize()}</span>'
                    f'<div class="praise-bar"><div class="praise-bar-fill" style="width:{pct}%"></div></div>'
                    f'<span class="kw-count">{count}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No praise keywords found")

    # ── Neutral Reviews Section (NEW) ─────────────────────────────────────────
    neutral_df = reviews_df[reviews_df["predicted_sentiment"] == "neutral"]
    if len(neutral_df) > 0:
        st.markdown("---")
        with st.expander(f"😐 Neutral Reviews ({len(neutral_df)} found) — click to expand"):
            st.caption("These reviews don't lean clearly positive or negative — often mixed feedback or suggestions.")
            for _, row in neutral_df.head(8).iterrows():
                conf = row.get("confidence", 0)
                rating = row.get("rating", "?")
                st.markdown(
                    f'<div class="neutral-card">'
                    f'<span style="color:#64748b; font-size:0.75rem;">⭐ {rating} · Confidence: {conf:.0%}</span><br>'
                    f'{str(row["content"])[:300]}{"…" if len(str(row["content"])) > 300 else ""}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ── Review Length Distribution (NEW) ──────────────────────────────────────
    st.markdown("---")
    st.subheader("📏 Review Length Distribution")

    reviews_df["review_length"] = reviews_df["content"].astype(str).str.len()
    bins = [0, 50, 100, 200, 350, 500, 5000]
    labels_bin = ["< 50", "50–100", "100–200", "200–350", "350–500", "500+"]
    reviews_df["length_bucket"] = pd.cut(reviews_df["review_length"], bins=bins, labels=labels_bin)

    length_dist = reviews_df.groupby(["length_bucket", "predicted_sentiment"]).size().reset_index(name="count")
    color_map = {"positive": "#22c55e", "negative": "#ef4444", "neutral": "#facc15"}

    fig = px.bar(
        length_dist, x="length_bucket", y="count", color="predicted_sentiment",
        color_discrete_map=color_map, barmode="stack",
        labels={"length_bucket": "Review Length (characters)", "count": "Number of Reviews", "predicted_sentiment": "Sentiment"},
        category_orders={"length_bucket": labels_bin},
    )
    fig.update_layout(
        height=280,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        legend=dict(font=dict(color="#94a3b8")),
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#64748b"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#64748b"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Sample Reviews Table ──────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 Sample Reviews with Predictions")

    sample_n = st.select_slider("Show reviews:", options=[10, 25, 50], value=10)
    sample_reviews = reviews_df[["content", "predicted_sentiment", "confidence", "rating"]].head(sample_n).copy()
    sample_reviews.columns = ["Review", "Sentiment", "Confidence", "Rating"]
    sample_reviews["Confidence"] = sample_reviews["Confidence"].map("{:.1%}".format)
    st.dataframe(sample_reviews, use_container_width=True, hide_index=True)

    # ── Download Button ───────────────────────────────────────────────────────
    csv = reviews_df.drop(columns=["review_length", "length_bucket"], errors="ignore").to_csv(index=False)
    col1, col2 = st.columns([3, 1])
    with col2:
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"bharatreview_{st.session_state.selected_app_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem 0; color: #475569; font-size: 0.8rem;">
    <b style="color:#818cf8;">BharatReview</b> — Built with ❤️ using 
    <b style="color:#94a3b8;">MuRIL</b> · <b style="color:#94a3b8;">Streamlit</b> · <b style="color:#94a3b8;">Plotly</b><br>
    Multilingual sentiment analysis across English, Hindi, Tamil, Telugu, Kannada, Bengali & Romanized text
</div>
""", unsafe_allow_html=True)
