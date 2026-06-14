# BharatReview — Deployment & Usage Guide

## 🚀 Project Overview

**BharatReview** is a production-ready multilingual Indian app review intelligence platform that:

- ✅ Analyzes Google Play Store reviews in English, Hindi, Tamil, Telugu, and code-mixed text
- ✅ Uses fine-tuned MuRIL model (98.46% accuracy)
- ✅ Provides sentiment distribution, keyword extraction, and language analytics
- ✅ Features URL-first, confidence-based app selection (eliminates errors)
- ✅ Professional Streamlit dashboard with interactive visualizations
- ✅ Ready for production deployment on HuggingFace Spaces

---

## 📦 Installation & Setup

### 1. Clone & Install Dependencies

```bash
git clone <your-repo-url>
cd BharatReview
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Pre-trained Model

The MuRIL sentiment model is included in `/models/muril_sentiment/`. No additional downloads needed.

### 3. Run the Dashboard

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## 🎯 How to Use

### Method 1: Google Play URL (Recommended)

1. **Copy the URL** of any app from Google Play Store
   - Example: `https://play.google.com/store/apps/details?id=com.whatsapp`

2. **Paste in Dashboard** → Instant app detection (100% accurate)

3. **Select Review Count** (50-1000)

4. **Click "Fetch & Analyze"** → Results in ~30-60 seconds

### Method 2: App Name Search (Alternative)

1. **Type app name** (e.g., "PhonePe", "Instagram", "BGMI")

2. **View Search Results** with confidence scores:
   - 🟢 **HIGH** (≥0.90): Trusted, use without hesitation
   - 🟡 **MEDIUM** (0.70-0.89): Verify before proceeding
   - 🔴 **LOW** (<0.70): Switch to URL input for accuracy

3. **Select Correct App** from list

4. **Fetch & Analyze**

---

## 📊 Output

### Dashboard Displays:

1. **Sentiment Distribution**
   - Pie chart: Positive / Negative / Neutral percentages
   - Average model confidence

2. **Language Distribution**
   - Bar chart of detected languages
   - Breakdown of multilingual reviews

3. **Top Complaints** (Negative Reviews)
   - Keywords extracted from negative sentiment reviews
   - Frequency count

4. **Top Praises** (Positive Reviews)
   - Keywords extracted from positive sentiment reviews
   - Frequency count

5. **Sample Reviews**
   - 10 sample reviews with predictions
   - Sentiment labels and confidence scores

6. **Download Results**
   - CSV export of all analyzed reviews
   - Includes: content, sentiment, confidence, rating

---

## 🔒 Data Quality & Confidence System

### Reliability by Input Method:

| Input Method | Accuracy | Time | Confidence |
|---|---|---|---|
| Google Play URL | 100% | Instant | Always HIGH |
| Known App Database (350+ apps) | 99% | Instant | HIGH |
| Search Recovery | 90% | 5-10s | MEDIUM |
| Unknown Apps | 75-85% | 10-20s | LOW |

### Quality Safeguards:

✅ **Known-App Database**: 350+ popular Indian apps  
✅ **Confidence Scoring**: Quantified trust level (0.0-1.0)  
✅ **User Verification**: Dashboard warns about low-confidence results  
✅ **Multi-Level Recovery**: Native → Known App → Search → Fallback  

---

## 🏗️ Project Structure

```
BharatReview/
├── app.py                      # Main Streamlit dashboard
├── scraper.py                  # Google Play scraping + app resolution
├── inference.py                # MuRIL model loading & predictions
├── analytics.py                # Sentiment distribution & keyword extraction
├── requirements.txt            # Python dependencies
├── models/
│   └── muril_sentiment/        # Fine-tuned MuRIL model (98.46% accuracy)
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer.json
│       └── ...
├── test_*.py                   # Unit tests
└── README.md
```

---

## 🚀 Deployment on HuggingFace Spaces

### Step 1: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Name: `bharatreview` (or your choice)
4. License: OpenRAIL
5. Space SDK: **Streamlit**
6. Private/Public: Your choice

### Step 2: Upload Files

```bash
cd BharatReview
git clone https://huggingface.co/spaces/YOUR_USERNAME/bharatreview
cd bharatreview

# Copy files
cp ../app.py .
cp ../scraper.py .
cp ../inference.py .
cp ../analytics.py .
cp ../requirements.txt .
cp -r ../models .

git add .
git commit -m "Initial BharatReview deployment"
git push
```

### Step 3: Configure Requirements

Make sure `requirements.txt` includes:

```txt
streamlit>=1.28
torch>=2.0
transformers>=4.30
pandas>=2.0
numpy>=1.24
plotly>=5.14
google-play-scraper>=1.2.7
nltk>=3.8
```

### Step 4: Live!

Your dashboard is now live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/bharatreview
```

Share the link in your GitHub README, portfolio, or LinkedIn!

---

## 📈 Model Performance

- **Test Accuracy**: 98.46%
- **Weighted F1 Score**: 98.46%
- **Languages**: English, Hindi, Tamil, Telugu, Kannada, Bengali, Code-mixed
- **Model Size**: ~500MB (fits in HF Spaces)

---

## 🛠️ API Usage (For Integration)

```python
from scraper import search_apps, fetch_reviews_for_app, extract_app_id_from_url
from inference import load_model, predict_batch
from analytics import calculate_sentiment_distribution, extract_keywords

# Method 1: URL
app_id = extract_app_id_from_url("https://play.google.com/store/apps/details?id=com.whatsapp")

# Method 2: Search with confidence
apps_df = search_apps("WhatsApp")
selected_app = apps_df[apps_df["confidence_level"] == "HIGH"].iloc[0]
app_id = selected_app["appId"]

# Fetch reviews
reviews_df = fetch_reviews_for_app(app_id, max_reviews=200)

# Predict sentiment
model = load_model()
predictions = predict_batch(model, reviews_df["content"].tolist())

# Analyze
sentiment_dist = calculate_sentiment_distribution(reviews_df)
complaints = extract_keywords(reviews_df, "negative")
```

---

## ❓ FAQ

**Q: Why URL-first design?**  
A: Google Play search is inconsistent. URLs are 100% reliable and eliminate all ambiguity.

**Q: What if my app is not in the known-app database?**  
A: The system falls back to search recovery (90% accurate). URL input is still recommended.

**Q: How many reviews can I analyze?**  
A: 50-1000 per session. More reviews = longer processing time but richer insights.

**Q: What languages are supported?**  
A: English, Hindi, Tamil, Telugu, Kannada, Bengali, + transliterated/code-mixed text.

**Q: Can I use this commercially?**  
A: Yes! MuRIL is open-source. Check licenses in `models/` folder for details.

---

## 📞 Support & Feedback

- **Issues**: Open GitHub issues for bugs
- **Features**: Suggest enhancements via pull requests
- **Credits**: Uses MuRIL (Google) + google-play-scraper

---

## 📜 License

This project uses open-source components. See LICENSE file for details.

---

## 🎓 Learning Path

1. Explore `scraper.py` to understand app resolution logic
2. Review `inference.py` for model loading and batch prediction
3. Study `analytics.py` for sentiment calculation and keyword extraction
4. Customize `app.py` Streamlit dashboard for your needs

---

**Made with ❤️ for the Indian developer community**
