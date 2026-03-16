from app import app
from flask import session
import unittest

class TestPredictions(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_predictions_with_chart(self):
        with self.app.session_transaction() as sess:
            sess['user_chart'] = {
                "rasi": {"englishName": "Mesham", "tamilName": "மேஷம்"},
                "nakshatra": {"name": "Ashwini", "index": 0}
            }
            sess['language'] = 'en'
        
        response = self.app.get('/predictions')
        self.assertEqual(response.status_code, 200)
        # Check if "MONTHLY OVERVIEW" is in the response (case insensitive or partial match)
        self.assertIn(b"MONTHLY OVERVIEW", response.data)
        self.assertIn(b"A month of significant breakthroughs", response.data)

    def test_predictions_tamil(self):
        with self.app.session_transaction() as sess:
            sess['user_chart'] = {
                "rasi": {"englishName": "Mesham", "tamilName": "மேஷம்"},
                "nakshatra": {"name": "Ashwini", "index": 0}
            }
            sess['language'] = 'ta'
        
        response = self.app.get('/predictions')
        self.assertEqual(response.status_code, 200)
        self.assertIn("மாதாந்திர கணிப்பு".encode('utf-8'), response.data)
        self.assertIn("குறிப்பிடத்தக்க முன்னேற்றங்களைக் கொண்ட மாதம்".encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()
