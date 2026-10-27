# Emotion Detector — Watson NLP + Flask

A small Python web application for analyzing a sentence's emotional tone. This project is organized to support the Coursera **Final Project: Emotion Detector** rubric: reusable package, normalized output, unit tests, Flask interface, input/error handling, and static analysis.

> **Before running:** configure `EMOTION_API_URL` with the exact Watson NLP emotion endpoint supplied in your Coursera lab. This repository does not include a credential or assume a particular lab endpoint. The wrapper expects a Watson-style response with `emotionPredictions[0].emotion` or a simplified `emotion`/`emotions` object. Adjust the request body or parser if the actual lab response differs.

## Features

- `EmotionDetection` Python package with `emotion_detector(text)`.
- Five scores: anger, disgust, fear, joy, sadness; plus `dominant_emotion`.
- HTTP 400 and blank-input handling.
- Flask user interface with a responsive results view.
- Unit tests with a mocked service response (no API credentials required for tests).
- Pylint configuration and commands for static analysis.

## Project layout

```text
Emotion-Detector-WatsonNLP/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/index.html
├── static/style.css
├── screenshots/                 # Save your actual lab screenshots here
├── server.py
├── test_emotion_detection.py
├── requirements.txt
├── .env.example
├── .pylintrc
└── README.md
```

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:EMOTION_API_URL = "PASTE_THE_EXACT_ENDPOINT_FROM_YOUR_LAB"
# If your endpoint requires a key, set it according to your lab instructions:
# $env:EMOTION_API_KEY = "YOUR_LAB_KEY"
```

On macOS/Linux, activate with `source .venv/bin/activate` and export `EMOTION_API_URL` instead.

## Run the unit tests

```bash
python -m unittest -v
```

Tests use mocks to validate the return shape, dominant emotion, HTTP 400 handling, and blank input without depending on a live API.

## Run Flask

```bash
flask --app server run
```

Open <http://127.0.0.1:5000>. Enter a non-empty sentence to test the form. Try submitting a blank field to validate the input error.

## Static analysis

```bash
python -m pip install pylint
pylint server.py EmotionDetection test_emotion_detection.py
```

The `.pylintrc` file contains a modest, explicit configuration. A score depends on the installed Pylint version and findings; fix reported warnings rather than claiming a score that was not produced locally.

## Coursera rubric mapping

| Rubric task | Files / evidence |
|---|---|
| 1. Repository URL | This public GitHub repository and this README |
| 2. Emotion function | `EmotionDetection/emotion_detection.py`; run an import and API test locally |
| 3. Output format | `emotion_detector` returns five scores and `dominant_emotion` |
| 4. Package validation | `EmotionDetection/__init__.py`; test `from EmotionDetection import emotion_detector` |
| 5. Unit tests | `test_emotion_detection.py`; run `python -m unittest -v` |
| 6. Flask deployment | `server.py`; capture `screenshots/6b_deployment_test.png` after running the app |
| 7. Error handling | HTTP 400 handling in package and blank-input handling in `server.py`; capture `screenshots/7c_error_handling_interface.png` |
| 8. Static analysis | Run Pylint and submit the actual terminal output |

## Screenshot checklist

Capture the screenshots from your own running lab environment and save them in `screenshots/`:

- `6b_deployment_test.png` — working Flask page with an actual analysis result.
- `7c_error_handling_interface.png` — UI showing the blank-input error.

Do not submit sample or fabricated terminal output as proof of a test run.

## Important note on the lab API

Watson NLP endpoint URLs, authentication, request fields, and response shape can differ between lab setups. This starter implementation is configurable and robust to a couple of common response shapes, but the final call must be verified using the endpoint and sample response from your own Coursera lab. Keep credentials out of GitHub.
