import os
import re
import requests

# ============================
# CONFIG
# ============================
HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ============================
# SENTIMENT (API + FALLBACK)
# ============================
def analyze_sentiment(text):
    if not text:
        raise ValueError("Text is required")

    url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

    # 🔥 TRY HUGGINGFACE FIRST
    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json={"inputs": text},
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()[0]
            return {
                "label": result["label"],
                "score": float(result["score"]),
                "source": "huggingface"
            }

    except Exception as e:
        print("🔥 HF API FAILED:", e)

    # ============================
    # 🔥 FALLBACK (LOCAL LOGIC)
    # ============================
    text_lower = text.lower()

    # remove punctuation
    clean_text = re.sub(r"[^\w\s]", "", text_lower)
    words = clean_text.split()

    positive_words = [
        "love", "great", "amazing", "good", "happy",
        "excellent", "best", "fantastic", "nice"
    ]

    negative_words = [
        "bad", "terrible", "hate", "worst",
        "awful", "poor", "horrible"
    ]

    total_words = len(words)

    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)

    score = pos_count - neg_count

    if total_words > 0:
        confidence = min(abs(score) / total_words, 1.0)
    else:
        confidence = 0.0

    label = "POSITIVE" if score >= 0 else "NEGATIVE"

    return {
        "label": label,
        "score": round(confidence, 4),
        "source": "fallback"
    }


# ============================
# SUMMARIZATION (FALLBACK)
# ============================
def summarize_text(text):
    if not text:
        raise ValueError("Text is required")

    words = text.split()

    if len(words) <= 30:
        return {
            "summary": text,
            "source": "fallback"
        }

    # summary = " ".join(words[:30]) + "..."
    sentences = text.split(".")
    summary = ".".join(sentences[:2]).strip() + "..."

    return {
        "summary": summary,
        "source": "fallback"
    }


# ============================
# CLASSIFICATION (FALLBACK)
# ============================
def classify_text(text, labels):
    if not text:
        raise ValueError("Text is required")

    if not labels:
        raise ValueError("Labels are required")

    text_lower = text.lower()

    # 🔥 KEYWORD MAP (SMART LOGIC)
    keyword_map = {
        "job": ["job", "hiring", "career", "vacancy", "recruit", "developer"],
        "spam": ["win", "free", "prize", "urgent", "claim"],
        "education": ["learn", "study", "course", "school", "training"]
    }

    scores = []

    for label in labels:
        keywords = keyword_map.get(label.lower(), [])

        match_count = sum(1 for word in keywords if word in text_lower)

        if match_count > 0:
            score = min(0.5 + (match_count * 0.1), 0.9)
        else:
            score = 0.1

        scores.append(round(score, 2))

    return {
        "labels": labels,
        "scores": scores,
        "source": "fallback"
    }