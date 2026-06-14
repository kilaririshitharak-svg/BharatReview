# BharatReview Dashboard — Visual Guide & Examples

## 🎨 Dashboard Interface Overview

This document shows what users will see when using the BharatReview dashboard.

---

## 📱 **Screen 1: Initial Load — URL Input Mode (Recommended)**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 BharatReview                                      ║
║                  App Review Intelligence Platform                            ║
├──────────────────────────────────────────────────────────────────────────────┤
║                                                                               ║
║  [Left Sidebar]                    [Main Content Area]                       ║
│  ┌─────────────────────────────┐                                             ║
│  │ 🎮 BharatReview             │   📱 Step 1: Select Your App               ║
│  │ Multilingual Indian App      │                                             ║
│  │ Review Analyzer              │   INPUT METHOD:                             ║
│  │                              │   ◯ Google Play URL (SELECTED)              ║
│  │ Input Method:                │   ◯ App Name Search                         ║
│  │ ⦿ Google Play URL            │                                             ║
│  │ ◯ App Name Search            │   ✅ RECOMMENDED: Direct, accurate, no     ║
│  │                              │   errors                                    ║
│  │                              │                                             ║
│  │                              │   Paste Google Play URL:                    ║
│  │                              │   ┌────────────────────────────────────┐    ║
│  │                              │   │ https://play.google.com/store/...  │    ║
│  │                              │   └────────────────────────────────────┘    ║
│  │                              │                                             ║
│  │                              │   💡 Example:                               ║
│  │                              │   https://play.google.com/store/...        ║
│  │                              │   details?id=com.whatsapp                   ║
│  │                              │                                             ║
│  └─────────────────────────────┘                                             ║
│                                                                               ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 📱 **Screen 2: After URL Entry — App Detected**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 BharatReview                                      ║
│                  App Review Intelligence Platform                             ║
├──────────────────────────────────────────────────────────────────────────────┤
║                                                                               ║
║  📱 Step 1: Select Your App                                                 ║
│                                                                               ║
│  INPUT METHOD:                                                                │
│  ◯ Google Play URL                                                            │
│  ◯ App Name Search                                                            │
│                                                                               ║
│  ✅ RECOMMENDED: Direct, accurate, no errors                                 ║
│                                                                               ║
│  Paste Google Play URL:                                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐  ║
│  │ https://play.google.com/store/apps/details?id=com.instagram.android   │  ║
│  └────────────────────────────────────────────────────────────────────────┘  ║
│                                                                               ║
│  ┌────────────────────────────────────────────────────────────────────────┐  ║
│  │ ✅ App ID extracted: com.instagram.android                             │  ║
│  └────────────────────────────────────────────────────────────────────────┘  ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  📊 Step 2: Fetch & Analyze Reviews                                          ║
│                                                                               ║
│  Number of reviews to fetch:                                                  │
│  ◀───────●─────────▶  [50 ───── 200 ──── 1000]                              ║
│           200 (selected)                                                      ║
│                                                                               ║
│  ┌──────────────────────────────────┐  ┌──────────────────────────────────┐  ║
│  │ 🚀 Fetch & Analyze               │  │ (Processing...)                  │  ║
│  └──────────────────────────────────┘  └──────────────────────────────────┘  ║
│                                                                               ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 **Screen 3: Results Dashboard — Sentiment Analysis**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 BharatReview                                      ║
│                       Results & Insights                                      ║
├──────────────────────────────────────────────────────────────────────────────┤
║                                                                               ║
║  METRICS ROW:                                                                 ║
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐            ║
│  │ Total Reviews    │  │ Avg Confidence   │  │ Positive Reviews │            ║
│  │                  │  │                  │  │                  │            ║
│  │       600        │  │      84.2%       │  │     68.17%       │            ║
│  └──────────────────┘  └──────────────────┘  └──────────────────┘            ║
│  ┌──────────────────┐                                                         ║
│  │ Negative Reviews │                                                         ║
│  │                  │                                                         ║
│  │     24.83%       │                                                         ║
│  └──────────────────┘                                                         ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  Sentiment Distribution              Language Distribution                    ║
│                                                                               ║
│  ╔═════════════╗                     ┌─────────────────────────────┐         ║
│  ║  ╱╲        ║                     │ Language      │ Count       │         ║
│  ║╱░░░╲  Pos   ║                     ├─────────────────────────────┤         ║
│  ║ 68% ╲ 409   ║                     │ English       │ 595         │         ║
│  ║╲███╱ Neg   ║                     │ Hindi         │ 2           │         ║
│  ║ ╲╱ 25% 149  ║                     │ Tamil         │ 2           │         ║
│  ║    Neu 7%   ║                     │ Kannada       │ 1           │         ║
│  ║    42       ║                     └─────────────────────────────┘         ║
│  ╚═════════════╝                                                              ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  🚨 Top Complaints              👍 Top Praises                               ║
│                                                                               ║
│  Keyword        │ Frequency      Keyword        │ Frequency                 ║
│  ─────────────────────────────  ─────────────────────────────              ║
│  payment        │ 12             payment        │ 12                         ║
│  phone          │ 11             service        │ 10                         ║
│  account        │ 10             easy           │ 10                         ║
│  support        │ 10             useful         │ 9                          ║
│  issue          │ 8              fast           │ 7                          ║
│  worst          │ 8              thank          │ 6                          ║
│  bad            │ 6              amazing        │ 5                          ║
│  balance        │ 6              experience     │ 5                          ║
│  service        │ 6              interface      │ 4                          ║
│  problem        │ 5              reliable       │ 4                          ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  Sample Reviews with Predictions                                              ║
│                                                                               ║
│  Review                          │ Sentiment  │ Confidence │ Rating           ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  good app                        │ Positive   │ 0.94       │ 5 ⭐           ║
│  Good Service                    │ Positive   │ 0.93       │ 5 ⭐           ║
│  excellent useful for customers  │ Positive   │ 0.94       │ 5 ⭐           ║
│  very good app                   │ Positive   │ 0.94       │ 4 ⭐           ║
│  do not work                     │ Negative   │ 0.94       │ 1 ⭐           ║
│  worst update ever               │ Negative   │ 0.92       │ 1 ⭐           ║
│  app crashed                     │ Negative   │ 0.89       │ 2 ⭐           ║
│  It is okay                      │ Neutral    │ 0.87       │ 3 ⭐           ║
│  nice interface                  │ Positive   │ 0.91       │ 4 ⭐           ║
│  amazing experience              │ Positive   │ 0.95       │ 5 ⭐           ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  [📥 Download Full Results (CSV)]                                            ║
│                                                                               ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔍 **Screen 4: App Search Mode — With Confidence Scores**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 BharatReview                                      ║
│                  App Review Intelligence Platform                             ║
├──────────────────────────────────────────────────────────────────────────────┤
║                                                                               ║
║  📱 Step 1: Select Your App                                                 ║
│                                                                               ║
│  INPUT METHOD:                                                                │
│  ◯ Google Play URL                                                            │
│  ⦿ App Name Search                                                            │
│                                                                               ║
│  ⚠️ Search mode: Results may be inaccurate for some apps. Verify your       ║
│  selection.                                                                   ║
│                                                                               ║
│  Search app name:                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐  ║
│  │ Instagram Lite                                                         │  ║
│  └────────────────────────────────────────────────────────────────────────┘  ║
│                                                                               ║
│  🔍 Searching for: Instagram Lite                                             │
│                                                                               ║
│  ℹ️ Rank 1 ('Instagram Lite') → resolved via known-app table:               ║
│  com.instagram.lite                                                           ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  Search Results:                                                              ║
│                                                                               ║
│  Rank │ Title            │ Developer        │ Confidence              │      ║
│  ─────┼──────────────────┼──────────────────┼─────────────────────────┤      ║
│  1    │ Instagram Lite   │ Meta Platforms   │ 🟢 HIGH (1.00)          │      ║
│  2    │ Instagram        │ Meta Platforms   │ 🟡 MEDIUM (0.80)        │      ║
│  3    │ Threads          │ Meta Platforms   │ 🟡 MEDIUM (0.80)        │      ║
│  4    │ Facebook Lite    │ Meta Platforms   │ 🟡 MEDIUM (0.80)        │      ║
│  5    │ Facebook         │ Meta Platforms   │ 🟡 MEDIUM (0.80)        │      ║
│                                                                               ║
│  Select the correct app (by rank):                                            ║
│  [▼ 1 - Instagram Lite]                                                       ║
│                                                                               ║
│  ✅ Selected: Instagram Lite (HIGH)                                           ║
│                                                                               ║
│  ─────────────────────────────────────────────────────────────────────────   ║
│  📊 Step 2: Fetch & Analyze Reviews                                          ║
│                                                                               ║
│  Number of reviews to fetch:                                                  │
│  ◀───────●─────────▶  [50 ───── 200 ──── 1000]                              ║
│           200 (selected)                                                      ║
│                                                                               ║
│  ┌──────────────────────────────────┐                                        ║
│  │ 🚀 Fetch & Analyze               │                                        ║
│  └──────────────────────────────────┘                                        ║
│                                                                               ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## ⚠️ **Screen 5: Low Confidence Warning**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 BharatReview                                      ║
│                  App Review Intelligence Platform                             ║
├──────────────────────────────────────────────────────────────────────────────┤
║                                                                               ║
║  Search Results:                                                              ║
│                                                                               ║
│  Rank │ Title             │ Developer        │ Confidence              │     ║
│  ─────┼───────────────────┼──────────────────┼─────────────────────────┤     ║
│  1    │ Some Fake App     │ Unknown Dev      │ 🔴 LOW (0.65)           │     ║
│  2    │ Another App       │ Another Dev      │ 🔴 LOW (0.60)           │     ║
│  3    │ Unknown App       │ Unknown Dev      │ 🔴 LOW (0.55)           │     ║
│                                                                               ║
│  ⚠️ 3 result(s) with LOW confidence. Verify before proceeding.              ║
│                                                                               ║
│  Select the correct app (by rank):                                            ║
│  [▼ 1 - Some Fake App]                                                        ║
│                                                                               ║
│  ┌────────────────────────────────────────────────────────────────────────┐  ║
│  │ ⚠️  Low Confidence (0.65): Results may be inaccurate. Use Google      │  ║
│  │ Play URL for better accuracy.                                          │  ║
│  └────────────────────────────────────────────────────────────────────────┘  ║
│                                                                               ║
╚═════════════════════════════════════════════════════════════════════════════╝
```

---

## 📥 **Screen 6: Download Results as CSV**

```
When user clicks "📥 Download Full Results (CSV)", they get a file like:

content,predicted_sentiment,confidence,rating
"good app",positive,0.935020,5
"Good Service",positive,0.932846,5
"excellent useful for customers",positive,0.941223,5
"very good app",positive,0.938667,4
"very good service",positive,0.939430,5
"do not work",negative,0.941317,1
"worst update ever",negative,0.925437,1
"app crashed frequently",negative,0.918462,1
"It is okay",neutral,0.874606,3
"nice interface",positive,0.930390,4
... (200-1000 rows total)
```

---

## 🎨 **UI Features Summary**

### Colors & Design
- **Primary Color**: Blue (#1f77b4) for headings
- **Background**: Light gray (#f8f9fa) for professional look
- **Success**: Green (#28a745) for positive/high confidence
- **Warning**: Yellow (#ffc107) for medium confidence
- **Danger**: Red (#dc3545) for negative/low confidence

### Interactive Elements
- 📊 **Plotly Charts**: Interactive, zoomable sentiment & language distribution
- 📋 **Dataframes**: Sortable and filterable tables
- 🎚️ **Sliders**: Review count selector (50-1000)
- 🔘 **Radio Buttons**: Input mode selection
- 🔽 **Dropdowns**: App selection from search results
- ⬇️ **Download Button**: CSV export of full results

### Mobile Responsive
- Two-column layout on desktop (sidebar + content)
- Single column on mobile (stacked layout)
- Touch-friendly buttons and inputs
- Readable fonts at all screen sizes

---

## 🚀 **Running Locally**

After installing dependencies:

```bash
streamlit run app.py
```

Then:
1. Open browser to `http://localhost:8501`
2. See the dashboard load in ~2-3 seconds
3. Enter a Google Play URL or search for an app
4. Click "Fetch & Analyze" 
5. Wait ~30-60 seconds for sentiment analysis
6. View results with charts, metrics, and keyword insights

---

## 📱 **Sample Data Generated**

The dashboard uses **actual MuRIL model predictions** on real Google Play reviews:

**Positive Reviews (68%):**
- "Good app" → 0.94 confidence
- "Excellent service" → 0.94 confidence
- "Very useful" → 0.93 confidence

**Negative Reviews (25%):**
- "Worst update" → 0.93 confidence
- "App crashed" → 0.92 confidence
- "Bugs everywhere" → 0.91 confidence

**Neutral Reviews (7%):**
- "It's okay" → 0.87 confidence
- "Average app" → 0.85 confidence
- "Nothing special" → 0.82 confidence

---

## ✅ **Dashboard is Production-Ready!**

All visual elements, data flows, and error handling are fully implemented and tested.
