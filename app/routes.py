from flask import Blueprint, jsonify, request

from app.services.ai_service import (
    analyze_sentiment,
    summarize_text,
    classify_text,
)

api = Blueprint("api", __name__)


# =========================================================
# HELPERS (CLEAN RESPONSE FORMAT)
# =========================================================

def success_response(data, status=200):
    return jsonify({
        "success": True,
        "data": data
    }), status


def error_response(message, status=400):
    return jsonify({
        "success": False,
        "error": message
    }), status


# =========================================================
# ROUTES
# =========================================================

@api.route("/", methods=["GET"])
def home():
    return success_response({
        "message": "AI Text Analyzer API is running"
    })


@api.route("/health", methods=["GET"])
def health():
    return success_response({
        "status": "ok"
    })


# =========================================================
# SENTIMENT
# =========================================================

@api.route("/sentiment", methods=["POST"])
def sentiment():
    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return error_response("Field 'text' is required")

        result = analyze_sentiment(data["text"])

        return success_response(result)

    except ValueError as error:
        return error_response(str(error), 400)

    except Exception as error:
        print("🔥 SENTIMENT ERROR:", str(error))  # 👈 ADD THIS
        return error_response(str(error), 500)


# =========================================================
# SUMMARIZATION
# =========================================================

@api.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return error_response("Field 'text' is required")

        result = summarize_text(data["text"])

        return success_response(result)

    except ValueError as error:
        return error_response(str(error), 400)

    except Exception as error:
        print("SUMMARY ERROR:", str(error))
        return error_response(str(error), 500)


# =========================================================
# CLASSIFICATION
# =========================================================

@api.route("/classify", methods=["POST"])
def classify():
    try:
        data = request.get_json(silent=True)

        if not data:
            return error_response("JSON body is required")

        if "text" not in data:
            return error_response("Field 'text' is required")

        if "labels" not in data:
            return error_response("Field 'labels' is required")

        result = classify_text(
            data["text"],
            data["labels"]
        )

        return success_response(result)

    except ValueError as error:
        return error_response(str(error), 400)

    except Exception as error:
        print("🔥 CLASSIFY ERROR:", str(error))
        return error_response(str(error), 500)