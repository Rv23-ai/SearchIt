import os
import hmac
import secrets
from flask import Flask, render_template, session, g, request, abort
from config import Config
from database import db
import models
from models import User
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

def generate_csrf_token():
    """Generate or retrieve unique CSRF token for the active session."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def create_app(config_class=Config):
    """Application factory for the Campus Lost & Found Platform."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    # Create database tables automatically within app context
    with app.app_context():
        db.create_all()

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.session.get(User, user_id)

    @app.before_request
    def csrf_protect():
        """Enforce CSRF token verification on state-changing HTTP methods."""
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            # In automated test mode, validate token if provided or skip if testing flag set
            if app.config.get('TESTING') and not app.config.get('WTF_CSRF_ENABLED', False):
                return
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            session_token = session.get('_csrf_token')
            if not token or not session_token or not hmac.compare_digest(token, session_token):
                abort(403, description="Security Error: Invalid or missing CSRF token.")

    @app.context_processor
    def inject_security_context():
        return dict(
            current_user=g.get('user', None),
            csrf_token=generate_csrf_token
        )

    @app.after_request
    def set_security_headers(response):
        """Inject security headers to protect against Clickjacking, MIME sniffing, and XSS."""
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:;"
        )
        return response

    # Root landing route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)

