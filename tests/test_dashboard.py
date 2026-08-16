import unittest
from app import create_app
from database import db
from models import Item, User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'testsecretkey'

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_renders_successfully(self):
        """Verify dashboard endpoint returns HTTP 200 and triggers seed data."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Central Campus Feed', response.data)
        self.assertIn(b'Black AirPods Pro Case', response.data)

    def test_dashboard_filter_by_type(self):
        """Verify filtering by item type (LOST vs FOUND)."""
        lost_resp = self.client.get('/dashboard?type=LOST')
        self.assertEqual(lost_resp.status_code, 200)
        self.assertIn(b'Student ID Card', lost_resp.data)
        self.assertNotIn(b'Black AirPods Pro Case', lost_resp.data)

        found_resp = self.client.get('/dashboard?type=FOUND')
        self.assertEqual(found_resp.status_code, 200)
        self.assertIn(b'Black AirPods Pro Case', found_resp.data)
        self.assertNotIn(b'Student ID Card', found_resp.data)

    def test_dashboard_search_keyword(self):
        """Verify keyword search filtering."""
        search_resp = self.client.get('/dashboard?q=AirPods')
        self.assertEqual(search_resp.status_code, 200)
        self.assertIn(b'Black AirPods Pro Case', search_resp.data)
        self.assertNotIn(b'Hydro Flask', search_resp.data)

if __name__ == '__main__':
    unittest.main()
