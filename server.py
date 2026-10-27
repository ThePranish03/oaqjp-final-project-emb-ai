"""Flask web interface for the Emotion Detector project."""
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html", result=None, error=None, text="")


@app.post("/emotionDetector")
def detect_emotion():
    text_to_analyze = request.form.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return render_template(
            "index.html", result=None,
            error="Please enter a sentence before analyzing.", text=text_to_analyze
        ), 400
    try:
        result = emotion_detector(text_to_analyze)
    except RuntimeError as exc:
        app.logger.exception("Emotion detection failed")
        return render_template(
            "index.html", result=None, error=str(exc), text=text_to_analyze
        ), 502
    if result.get("dominant_emotion") is None:
        return render_template(
            "index.html", result=None,
            error="The service could not analyze this input. Please try another sentence.",
            text=text_to_analyze
        ), 400
    return render_template("index.html", result=result, error=None, text=text_to_analyze)


if __name__ == "__main__":
    # Run locally with: flask --app server run --debug
    app.run(host="127.0.0.1", port=5000, debug=False)
