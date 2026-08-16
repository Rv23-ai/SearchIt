from flask import Blueprint, render_template, request
from database import db
from models import Item, User
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

CATEGORIES = ['Phone', 'Keys', 'Earbuds', 'ID Card', 'Bag', 'Accessories', 'Documents']

def seed_sample_items_if_empty():
    """Seed sample campus lost & found items if database is empty for rich preview."""
    if Item.query.count() == 0:
        # Check or create seed user
        seed_user = User.query.filter_by(college_email='campus.admin@college.edu').first()
        if not seed_user:
            seed_user = User(
                college_email='campus.admin@college.edu',
                student_id='ADM2026-001',
                department='Campus Safety & Admin',
                password_hash=generate_password_hash('adminpass123'),
                karma_score=300
            )
            db.session.add(seed_user)
            db.session.commit()

        sample_items = [
            Item(
                title='Black AirPods Pro Case',
                category='Earbuds',
                item_type='FOUND',
                status='ACTIVE',
                building='Central Library',
                floor='1st Floor',
                spot_description='Found near Desk #14 by the reading hall window.',
                secret_question='What color is the protective silicone sleeve?',
                user_id=seed_user.id
            ),
            Item(
                title='Student ID Card (CS Department)',
                category='ID Card',
                item_type='LOST',
                status='ACTIVE',
                building='Admin Block',
                floor='Ground Floor',
                spot_description='Misplaced near the fee submission counter queue.',
                user_id=seed_user.id
            ),
            Item(
                title='Blue Hydro Flask Water Bottle',
                category='Accessories',
                item_type='FOUND',
                status='ACTIVE',
                building='Main Canteen',
                floor='Outdoor Grounds',
                spot_description='Left under umbrella table #5 after lunch hour.',
                secret_question='Are there any stickers on the bottom rim?',
                user_id=seed_user.id
            ),
            Item(
                title='Brown Leather Wallet & Keyring',
                category='Keys',
                item_type='LOST',
                status='ACTIVE',
                building='Science Block A',
                floor='2nd Floor',
                spot_description='Left inside Chemistry Lab 204 on bench row 3.',
                user_id=seed_user.id
            )
        ]
        db.session.add_all(sample_items)
        db.session.commit()

@dashboard_bp.route('/dashboard')
@dashboard_bp.route('/feed')
def feed():
    """Render central campus feed with search and filter capabilities."""
    seed_sample_items_if_empty()

    item_type = request.args.get('type', 'ALL').upper()
    category = request.args.get('category', '').strip()
    search_q = request.args.get('q', '').strip()

    query = Item.query

    if item_type in ['LOST', 'FOUND']:
        query = query.filter(Item.item_type == item_type)

    if category and category in CATEGORIES:
        query = query.filter(Item.category == category)

    if search_q:
        search_term = f"%{search_q}%"
        query = query.filter(
            (Item.title.ilike(search_term)) |
            (Item.building.ilike(search_term)) |
            (Item.spot_description.ilike(search_term)) |
            (Item.category.ilike(search_term))
        )

    items = query.order_by(Item.created_at.desc()).all()

    # Live statistics counts
    total_count = Item.query.count()
    lost_count = Item.query.filter_by(item_type='LOST').count()
    found_count = Item.query.filter_by(item_type='FOUND').count()

    return render_template(
        'dashboard.html',
        items=items,
        categories=CATEGORIES,
        active_type=item_type,
        active_category=category,
        search_q=search_q,
        total_count=total_count,
        lost_count=lost_count,
        found_count=found_count
    )
