import re
import time
from functools import wraps
from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

auth_bp = Blueprint('auth', __name__)

# Simple in-memory rate limiter for login brute-force defense
# Key: IP address, Value: list of timestamps of failed login attempts
FAILED_LOGIN_ATTEMPTS = {}

def is_rate_limited(ip_address, max_attempts=5, window_seconds=300):
    """Check if an IP address has exceeded failed login attempt threshold within window."""
    now = time.time()
    attempts = FAILED_LOGIN_ATTEMPTS.get(ip_address, [])
    # Filter attempts within current window
    valid_attempts = [t for t in attempts if now - t < window_seconds]
    FAILED_LOGIN_ATTEMPTS[ip_address] = valid_attempts
    return len(valid_attempts) >= max_attempts

def record_failed_attempt(ip_address):
    """Record a failed login attempt timestamp for the given IP address."""
    now = time.time()
    attempts = FAILED_LOGIN_ATTEMPTS.get(ip_address, [])
    attempts.append(now)
    FAILED_LOGIN_ATTEMPTS[ip_address] = attempts

def clear_failed_attempts(ip_address):
    """Clear failed login attempts record upon successful authentication."""
    FAILED_LOGIN_ATTEMPTS.pop(ip_address, None)

def is_safe_url(target):
    """Validate that redirect target is a safe relative path on the same host."""
    if not target or not isinstance(target, str):
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def login_required(f):
    """Decorator to require authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            target_next = request.url if is_safe_url(request.url) else url_for('index')
            return redirect(url_for('auth.login', next=target_next))
        return f(*args, **kwargs)
    return decorated_function

def is_valid_campus_email(email):
    """Validate that email belongs strictly to an official campus @college.edu domain."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False
    domain = email.split('@')[-1].lower()
    return domain == 'college.edu' or domain.endswith('.college.edu')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle institutional user registration with domain & student ID validation."""
    if request.method == 'GET' and 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        college_email = request.form.get('college_email', '').strip().lower()
        student_id = request.form.get('student_id', '').strip()
        department = request.form.get('department', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Input length caps & presence checks
        if not college_email or not student_id or not department or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if len(college_email) > 120 or len(student_id) > 50 or len(department) > 100 or len(password) > 128:
            flash('Field length exceeds maximum limit.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if not is_valid_campus_email(college_email):
            flash('Registration is strictly restricted to valid campus email domains (@college.edu).', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        # Check existing user
        if User.query.filter_by(college_email=college_email).first():
            flash('An account with this email address already exists.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if User.query.filter_by(student_id=student_id).first():
            flash('An account with this Student ID already exists.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            college_email=college_email,
            student_id=student_id,
            department=department,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        # Prevent Session Fixation: clear prior session data & regenerate
        csrf_tok = session.get('_csrf_token')
        session.clear()
        if csrf_tok:
            session['_csrf_token'] = csrf_tok

        session['user_id'] = new_user.id
        session['user_email'] = new_user.college_email

        flash('Registration successful! Welcome to SearchIt.', 'success')
        return redirect(url_for('index'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login authentication with rate limiting protection."""
    if request.method == 'GET' and 'user_id' in session:
        return redirect(url_for('index'))

    next_param = request.args.get('next')
    safe_next = next_param if is_safe_url(next_param) else None
    ip_addr = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        # Check rate limit before processing authentication
        if is_rate_limited(ip_addr):
            flash('Too many failed login attempts. Please wait 5 minutes before trying again.', 'error')
            return render_template('auth/login.html', college_email=request.form.get('college_email', '').strip().lower()), 429

        college_email = request.form.get('college_email', '').strip().lower()
        password = request.form.get('password', '')

        if not college_email or not password:
            flash('Please enter both email address and password.', 'error')
            return render_template('auth/login.html', college_email=college_email)

        user = User.query.filter_by(college_email=college_email).first()

        if not user or not check_password_hash(user.password_hash, password):
            record_failed_attempt(ip_addr)
            flash('Invalid email address or password.', 'error')
            return render_template('auth/login.html', college_email=college_email)

        # Successful login: clear failed attempts tracker
        clear_failed_attempts(ip_addr)

        # Prevent Session Fixation: clear prior session & regenerate
        csrf_tok = session.get('_csrf_token')
        session.clear()
        if csrf_tok:
            session['_csrf_token'] = csrf_tok

        session['user_id'] = user.id
        session['user_email'] = user.college_email

        flash(f'Welcome back, {user.college_email}!', 'success')
        return redirect(safe_next if safe_next else url_for('index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle user logout safely."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


