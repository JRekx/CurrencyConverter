import unittest
from app import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_access(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_form_submission_valid(self):
        data = {
            'amount': '100',
            'from_currency': 'USD',
            'to_currency': 'EUR'
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertIn(b'is equal to', response.data)

    def test_form_submission_invalid(self):
        data = {
            'amount': '100',
            'from_currency': 'INVALID',
            'to_currency': 'EUR'
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertIn(b'Invalid currency codes', response.data)

if __name__ == '__main__':
    unittest.main()
