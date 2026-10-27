# Screenshot capture guide

1. Start Flask from this project directory with `flask --app server run`.
2. Open `http://127.0.0.1:5000` in the browser and submit a sentence. Capture the page including the result panel as `screenshots/6b_deployment_test.png`.
3. Submit the form with an empty text box. Capture the visible error message as `screenshots/7c_error_handling_interface.png`.
4. Run `python -m unittest -v` and `pylint server.py EmotionDetection test_emotion_detection.py`; capture real terminal output for the matching questions.

Use your operating system's screenshot tool. Screenshots should show the actual local application and should not be edited to imply a test succeeded when it did not.
