from datetime import datetime, timezone
from database import db

class User(db.Model):
    """User ORM model representing campus students and faculty."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    college_email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    karma_score = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    items = db.relationship('Item', backref='user', lazy=True, cascade='all, delete-orphan')
    sent_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.sender_id',
        backref='sender',
        lazy=True,
        cascade='all, delete-orphan'
    )
    received_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.receiver_id',
        backref='receiver',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.college_email}>'


class Item(db.Model):
    """Item ORM model for lost and found reports."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    item_type = db.Column(db.String(10), nullable=False)  # 'LOST' or 'FOUND'
    status = db.Column(db.String(20), default='ACTIVE', nullable=False)  # 'ACTIVE', 'CLAIMED', 'RESOLVED'
    building = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    spot_description = db.Column(db.Text, nullable=False)
    secret_question = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    chat_messages = db.relationship('ChatMessage', backref='item', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Item {self.id}: {self.title} ({self.item_type})>'


class ChatMessage(db.Model):
    """ChatMessage ORM model for anonymous peer-to-peer messaging."""
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<ChatMessage {self.id} for Item {self.item_id}>'
