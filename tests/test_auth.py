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

    def test_register_invalid_domain_rejected(self):
        """Verify non-institutional domain (@gmail.com) is rejected."""
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
