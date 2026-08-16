from flask import Flask, render_template, session, g
from config import Config
from database import db
import models
from models import User
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

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

    @app.context_processor
    def inject_user():
        return dict(current_user=g.get('user', None))

    # Root landing route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
