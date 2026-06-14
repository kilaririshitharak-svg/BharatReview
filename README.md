<div align="center">

# 🚀 BharatReview

### Multilingual Indian App Review Intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/MuRIL-HuggingFace-ffd21e?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/BharatReview/muril-sentiment)
[![Accuracy](https://img.shields.io/badge/Accuracy-98.46%25-22c55e?style=for-the-badge)](#)

**Analyze Google Play Store reviews in English, Hindi, Tamil, Telugu, Kannada & Bengali using a fine-tuned MuRIL transformer model.**

🔗 **[Live Demo](https://huggingface.co/spaces/BharatReview/BharatReview)** · 🤖 **[Model on HuggingFace](https://huggingface.co/BharatReview/muril-sentiment)**

</div>

---

## ✨ Features

- 🌐 **Multilingual** — English, Hindi, Tamil, Telugu, Kannada, Bengali + Romanized text
- 🤖 **MuRIL-Powered** — Fine-tuned Google MuRIL model with 98.46% test accuracy
- 🔍 **Smart Search** — 350+ known Indian apps + Google Play URL input
- 📊 **5 Charts** — Sentiment, language, rating vs sentiment, review length, keywords
- 🚨 **Top Complaints & Praises** — Keyword extraction from negative/positive reviews
- 📥 **CSV Export** — Download full results with predictions and confidence scores
- 🎨 **Dark UI** — Glassmorphism theme with interactive Plotly charts

---

## 🚀 Quick Start

```bash
git clone https://github.com/kilaririshitharak-svg/BharatReview.git
cd BharatReview
pip install -r requirements.txt
streamlit run app.py
```

> **Model:** Download from [HuggingFace Hub](https://huggingface.co/BharatReview/muril-sentiment) and place in `models/muril_sentiment/`
>
> ```python
> from huggingface_hub import snapshot_download
> snapshot_download(repo_id="BharatReview/muril-sentiment", local_dir="models/muril_sentiment")
> ```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit + Plotly |
| Model | Google MuRIL (PyTorch + HuggingFace Transformers) |
| Scraper | google-play-scraper |
| Analytics | Pandas, NLTK |
| Deployment | HuggingFace Spaces |

---

## 📄 License

MIT License — feel free to use and build on this project.

<div align="center">

**Made with ❤️ for Indian developers and product teams**

</div>
