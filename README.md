<div align="center">

# 🚀 BharatReview

### Multilingual Indian App Review Intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/MuRIL-HuggingFace-ffd21e?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/google/muril-base-cased)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Accuracy](https://img.shields.io/badge/Test%20Accuracy-98.46%25-22c55e?style=for-the-badge)](#model)
[![License](https://img.shields.io/badge/License-MIT-6366f1?style=for-the-badge)](LICENSE)

**BharatReview** analyzes Google Play Store reviews written in English, Hindi, Tamil, Telugu, Kannada, Bengali, and Romanized Indian text — and converts them into actionable sentiment insights using a fine-tuned MuRIL transformer model.

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [Usage](#-usage) · [Model](#-model) · [Architecture](#-architecture) · [Deploy](#-deployment)

</div>

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🌐 **Multilingual** | English, Hindi, Tamil, Telugu, Kannada, Bengali + Romanized text |
| 🤖 **MuRIL-Powered** | Fine-tuned Google MuRIL model — 98.46% test accuracy |
| 🔍 **Smart App Search** | 350+ known Indian apps + Google Play URL input |
| 📊 **5 Analytics Charts** | Sentiment, language distribution, rating vs sentiment, review length, keywords |
| 🚨 **Top Complaints** | Meaningful complaint keywords with inline frequency bars |
| 👍 **Top Praises** | Meaningful praise keywords filtered from filler words |
| 😐 **Neutral Reviews** | Dedicated expandable section for mixed-feedback reviews |
| 📥 **CSV Export** | Download full results with predicted sentiments |
| 🎨 **Dark UI** | Glassmorphism dark theme with gradient hero, styled cards |

---

## 🎬 Demo

> **Input modes:**
> - Paste a Google Play URL (recommended — most accurate)
> - Search by app name (e.g., "PhonePe", "Zomato", "Swiggy")

**Supported apps include:** PhonePe · Google Pay · Paytm · WhatsApp · Swiggy · Zomato · Ola · Uber · IRCTC · MakeMyTrip · Meesho · Flipkart · Amazon · Hotstar · Netflix · Spotify · and 300+ more.

---

## 💻 Installation

### Prerequisites
- Python 3.10+
- 4 GB RAM minimum (8 GB recommended for smooth inference)
- CUDA GPU optional (runs on CPU — slower but functional)

### Clone & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/BharatReview.git
cd BharatReview

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### Model Setup

The MuRIL sentiment model (~950 MB) must be placed at `models/muril_sentiment/`.

**Required files inside `models/muril_sentiment/`:**
```
config.json
model.safetensors
tokenizer.json
tokenizer_config.json
special_tokens_map.json
vocab.txt
training_args.bin
```

> If you're using the pre-trained weights from HuggingFace, download them with:
> ```python
> from huggingface_hub import snapshot_download
> snapshot_download(repo_id="your-username/muril-sentiment", local_dir="models/muril_sentiment")
> ```

---

## 🚀 Usage

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`

### Step 1 — Select Your App

**Option A: Google Play URL** *(Recommended)*
```
https://play.google.com/store/apps/details?id=com.whatsapp
```

**Option B: App Name Search**
- Type the app name (e.g., `PhonePe`)
- Press **Enter** or click **🔍 Search**
- Select the correct app from results
- Check the confidence score before proceeding

### Step 2 — Fetch & Analyze
- Set the number of reviews (50–1,000)
- Click **🚀 Fetch & Analyze**
- Watch the real-time progress bar as MuRIL processes each review

### Step 3 — Explore Results
- **Sentiment Distribution** — donut chart (Positive / Negative / Neutral)
- **Language Distribution** — horizontal bar chart by detected script
- **Rating vs Sentiment** — grouped bars comparing star ratings to predicted sentiment
- **Top Complaints** — most frequent negative-review keywords
- **Top Praises** — most frequent positive-review keywords
- **Neutral Reviews** — expandable section with mixed-feedback reviews
- **Review Length Chart** — stacked bar showing length vs sentiment patterns
- **Download CSV** — full results with predictions and confidence scores

---

## 🤖 Model

### Architecture

| Property | Value |
|---|---|
| Base Model | `google/muril-base-cased` |
| Task | Sequence Classification (3 classes) |
| Classes | `positive` · `negative` · `neutral` |
| Max Length | 128 tokens |
| Framework | PyTorch + HuggingFace Transformers |

### Training

| Metric | Value |
|---|---|
| Training Set | Indian Play Store reviews (English + 5 Indian languages) |
| Test Accuracy | **98.46%** |
| Languages | English, Hindi, Tamil, Telugu, Kannada, Bengali, Romanized |

### Why MuRIL?

Most sentiment models are trained on English only. MuRIL (Multilingual Representations for Indian Languages) was developed by Google Research specifically for Indian languages and handles:

- **Script-based text**: Devanagari (Hindi), Tamil script, Telugu script, etc.
- **Romanized text**: `achha hai yaar`, `bahut badhiya app hai`
- **Code-mixed text**: `This app is bahut accha, love it!`

---

## 🏗️ Architecture

```
BharatReview/
│
├── app.py              # Streamlit dashboard (UI + orchestration)
├── inference.py        # MuRIL model loader + sentiment prediction
├── scraper.py          # Google Play review scraper + app search
├── analytics.py        # Sentiment distribution, language detection, keywords
├── requirements.txt    # Pinned Python dependencies
│
└── models/
    └── muril_sentiment/
        ├── config.json
        ├── model.safetensors   # 950 MB — fine-tuned weights
        ├── tokenizer.json
        ├── tokenizer_config.json
        ├── special_tokens_map.json
        ├── vocab.txt
        └── training_args.bin
```

### Data Flow

```
User Input (URL or App Name)
         │
         ▼
    scraper.py
    ┌─────────────────────────────┐
    │  Resolve App ID             │
    │  Fetch Reviews (up to 1000) │
    │  Filter None/empty reviews  │
    └─────────────────────────────┘
         │
         ▼
    inference.py
    ┌─────────────────────────────┐
    │  MuRIL Tokenizer            │
    │  Forward Pass               │
    │  Softmax → label + score    │
    └─────────────────────────────┘
         │
         ▼
    analytics.py
    ┌─────────────────────────────┐
    │  Sentiment Distribution     │
    │  Language Detection         │
    │  Keyword Extraction         │
    └─────────────────────────────┘
         │
         ▼
    app.py (Streamlit)
    5 Charts + Keyword Cards + Tables
```

---

## 📦 Dependencies

```
streamlit>=1.32.0        # Dashboard framework
torch>=2.0.0             # PyTorch for MuRIL inference
transformers>=4.44.0     # HuggingFace model loading
pandas>=2.0.0            # Data handling
numpy>=1.24.0            # Numerical operations
plotly>=5.18.0           # Interactive charts
google-play-scraper>=1.2.7  # Play Store review fetcher
nltk>=3.8.0              # Stopwords for keyword extraction
sentencepiece>=0.1.99    # MuRIL tokenizer dependency
```

---

## ☁️ Deployment

### HuggingFace Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select **Streamlit** as the SDK
3. Upload the model to a separate HuggingFace **Model Repository**
4. Update `MODEL_PATH` in `inference.py` to load from the Hub:
   ```python
   MODEL_PATH = "your-username/muril-sentiment"
   ```
5. Push the code (without model weights) to the Space repo

### Local Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🗺️ Roadmap

- [ ] HuggingFace Spaces live deployment
- [ ] Batch CSV upload (analyze your own review files)
- [ ] Trend analysis over time (monthly sentiment shifts)
- [ ] Word cloud visualization
- [ ] Multi-app comparison mode
- [ ] REST API endpoint for programmatic access

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ for Indian developers and product teams**

*BharatReview — because every review deserves to be understood*

</div>
