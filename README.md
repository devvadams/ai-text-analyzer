# AI Text Analyzer API 🚀

A lightweight AI-powered REST API for **sentiment analysis, text summarization, and classification**, built with Flask and integrated with HuggingFace (with fallback support).

---

## 🔥 Features

* ✅ Sentiment Analysis (HuggingFace + fallback)
* ✅ Text Summarization (lightweight fallback)
* ✅ Text Classification (keyword-based fallback)
* ✅ Clean API structure (Flask Blueprint)
* ✅ Production-ready (Render deployment)

---

## 🛠️ Tech Stack

* Python
* Flask
* Requests
* HuggingFace API

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/ai-text-analyzer.git
cd ai-text-analyzer
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
python run.py
```

---

## 🌐 API Endpoints

### 🔹 Health

```
GET /health
```

---

### 🔹 Sentiment

```
POST /sentiment
```

```json
{
  "text": "I love this product"
}
```

---

### 🔹 Summarize

```
POST /summarize
```

```json
{
  "text": "Long text..."
}
```

---

### 🔹 Classify

```
POST /classify
```

```json
{
  "text": "We are hiring a developer",
  "labels": ["job", "spam", "education"]
}
```

---

## ⚠️ Notes

* Uses HuggingFace API when available
* Falls back to lightweight local logic if API fails
* Designed to be fast and resource-efficient

---

## 📄 License

MIT License
