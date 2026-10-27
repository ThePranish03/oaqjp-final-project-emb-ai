"""Unit tests for the EmotionDetection package (external API is mocked)."""
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import EMOTIONS, emotion_detector


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    @patch("EmotionDetection.emotion_detection.EMOTION_API_URL", "https://example.test/emotion")
    def test_output_format_and_dominant_emotion(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.02, "fear": 0.03,
                "joy": 0.90, "sadness": 0.04
            }}]
        }
        mock_post.return_value = mock_response
        result = emotion_detector("I am very happy")
        self.assertEqual(set(result), set(EMOTIONS) | {"dominant_emotion"})
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.90)

    @patch("EmotionDetection.emotion_detection.EMOTION_API_URL", "https://example.test/emotion")
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_null_values(self, mock_post):
        response = Mock(status_code=400, ok=False)
        mock_post.return_value = response
        result = emotion_detector("some text")
        self.assertTrue(all(result[key] is None for key in (*EMOTIONS, "dominant_emotion")))

    def test_blank_input_returns_null_values(self):
        result = emotion_detector("   ")
        self.assertTrue(all(result[key] is None for key in (*EMOTIONS, "dominant_emotion")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
