import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_valid_campus_email(email):
    """Validate that email belongs to an institutional @college.edu domain."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False
    # Enforce @college.edu or institutional .edu domain
    domain = email.split('@')[-1].lower()
    return domain == 'college.edu' or domain.endswith('.college.edu') or domain.endswith('.edu')

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

        # Validation checks
        if not college_email or not student_id or not department or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if not is_valid_campus_email(college_email):
            flash('Registration is strictly restricted to valid campus email domains (@college.edu).', 'error')
            return render_template('auth/register.html', college_email=college_email, student_id=student_id, department=department)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
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

        # Log user into session
        session['user_id'] = new_user.id
        session['user_email'] = new_user.college_email

        flash('Registration successful! Welcome to SearchIt.', 'success')
        return redirect(url_for('index'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login authentication."""
    if request.method == 'GET' and 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        college_email = request.form.get('college_email', '').strip().lower()
        password = request.form.get('password', '')

        if not college_email or not password:
            flash('Please enter both email address and password.', 'error')
            return render_template('auth/login.html', college_email=college_email)

        user = User.query.filter_by(college_email=college_email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email address or password.', 'error')
            return render_template('auth/login.html', college_email=college_email)

        session['user_id'] = user.id
        session['user_email'] = user.college_email

        flash(f'Welcome back, {user.college_email}!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
