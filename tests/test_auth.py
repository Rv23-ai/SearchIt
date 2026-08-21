import unittest
import sys
import os
from app import create_app
from database import db
from models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'testsecretkey'

class AuthTestCase(unittest.TestCase):
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

    def test_security_headers_present(self):
        """Verify HTTP security response headers (X-Frame-Options, CSP, etc.) are injected."""
        response = self.client.get('/')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertIn("default-src 'self'", response.headers.get('Content-Security-Policy', ''))

    def test_register_short_password_rejected(self):
        """Verify password under 8 characters is rejected."""
        response = self.client.post('/register', data={
            'college_email': 'shortpass@college.edu',
            'student_id': 'CS2026-101',
            'department': 'CS',
            'password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)
        self.assertIn(b'Password must be at least 8 characters long', response.data)

    def test_rate_limiting_on_login(self):
        """Verify 5 failed login attempts trigger rate limiting HTTP 429 response."""
        # 5 consecutive failed login attempts
        for _ in range(5):
            self.client.post('/login', data={
                'college_email': 'nonexistent@college.edu',
                'password': 'wrongpassword'
            })
        
        # 6th attempt should be throttled with HTTP 429
        blocked_resp = self.client.post('/login', data={
            'college_email': 'nonexistent@college.edu',
            'password': 'wrongpassword'
        })
        self.assertEqual(blocked_resp.status_code, 429)
        self.assertIn(b'Too many failed login attempts', blocked_resp.data)

    def test_register_invalid_domain_rejected(self):
        """Verify non-institutional domains (@gmail.com and arbitrary @other.edu) are rejected."""
        response = self.client.post('/register', data={
            'college_email': 'student@gmail.com',
            'student_id': 'CS2026-001',
            'department': 'Computer Science',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Registration is strictly restricted to valid campus email domains', response.data)
        user = User.query.filter_by(college_email='student@gmail.com').first()
        self.assertIsNone(user)

        # Test arbitrary .edu domain rejection (e.g., hacker@fake.edu)
        response_edu = self.client.post('/register', data={
            'college_email': 'hacker@fake.edu',
            'student_id': 'CS2026-999',
            'department': 'Computer Science',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Registration is strictly restricted to valid campus email domains', response_edu.data)
        user_edu = User.query.filter_by(college_email='hacker@fake.edu').first()
        self.assertIsNone(user_edu)

    def test_register_valid_campus_email_success(self):
        """Verify valid @college.edu email succeeds and creates user."""
        response = self.client.post('/register', data={
            'college_email': 'student@college.edu',
            'student_id': 'CS2026-001',
            'department': 'Computer Science',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful!', response.data)
        user = User.query.filter_by(college_email='student@college.edu').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.student_id, 'CS2026-001')

    def test_open_redirect_rejected_on_login(self):
        """Verify open redirect payload (?next=https://attacker.com) is safely ignored."""
        # Register user
        self.client.post('/register', data={
            'college_email': 'victim@college.edu',
            'student_id': 'CS2026-777',
            'department': 'Security',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        })
        self.client.get('/logout')

        # Login with malicious next redirect parameter
        resp = self.client.post('/login?next=https://attacker.com/phishing', data={
            'college_email': 'victim@college.edu',
            'password': 'securepassword'
        }, follow_redirects=False)

        # Must redirect to root ('/') and NOT external URL
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(resp.location.startswith('https://attacker.com'))
        self.assertTrue(resp.location.startswith('/') or resp.location.endswith('/'))

    def test_csrf_token_enforcement(self):
        """Verify CSRF token validation blocks unauthorized POST requests when CSRF testing enabled."""
        self.app.config['WTF_CSRF_ENABLED'] = True
        resp = self.client.post('/register', data={
            'college_email': 'unauthorized@college.edu',
            'student_id': 'CS2026-888',
            'department': 'IT',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(resp.status_code, 403)
        self.assertIn(b'CSRF token', resp.data)

    def test_duplicate_email_rejected(self):
        """Verify registering with duplicate email is blocked."""
        self.client.post('/register', data={
            'college_email': 'alex@college.edu',
            'student_id': 'CS2026-002',
            'department': 'ECE',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.get('/logout')
        response = self.client.post('/register', data={
            'college_email': 'alex@college.edu',
            'student_id': 'CS2026-003',
            'department': 'ECE',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'An account with this email address already exists', response.data)

    def test_login_logout_flow(self):
        """Verify successful login and logout."""
        # 1. Register user
        self.client.post('/register', data={
            'college_email': 'login_test@college.edu',
            'student_id': 'CS2026-010',
            'department': 'IT',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        })
        # Logout first
        self.client.get('/logout')

        # 2. Invalid password login attempt
        bad_login = self.client.post('/login', data={
            'college_email': 'login_test@college.edu',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email address or password', bad_login.data)

        # 3. Valid login attempt
        good_login = self.client.post('/login', data={
            'college_email': 'login_test@college.edu',
            'password': 'securepassword'
        }, follow_redirects=True)
        self.assertIn(b'Welcome back, login_test@college.edu', good_login.data)

        # 4. Logout
        logout_resp = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out successfully', logout_resp.data)

if __name__ == '__main__':
    unittest.main()
