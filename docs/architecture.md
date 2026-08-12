# System Architecture & Technical Specifications

## 1. Tech Stack Matrix

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Clean syntax, robust ecosystem, fast prototyping. |
| **Web Framework** | Flask 3.0+ | Lightweight, explicit, highly flexible WSGI monolithic framework. |
| **ORM / Database** | Flask-SQLAlchemy + SQLite | Simple, file-based database for prototype, modular ORM mapping. |
| **Password Security**| Werkzeug Security | Built-in secure PBKDF2 / Bcrypt password hashing. |
| **Templating** | Jinja2 | Server-Side Rendering (SSR) for multi-page simplicity. |
| **Styling** | Tailwind CSS (v3 CDN) | Responsive, utility-first styling without node/npm build dependencies. |

---

## 2. Directory Layout (Flask Blueprints Pattern)
```text
CampusApp/
├── .gitignore
├── .env
├── .env.example
├── README.md
├── requirements.txt
├── LICENSE
├── app.py                      # Flask Application Factory & Entrypoint
├── config.py                   # Flask Configuration Class
├── database.py                 # db = SQLAlchemy() setup instance
├── models.py                   # ORM Database Models
├── routes/                     # Modular Flask Blueprints
│   ├── __init__.py
│   ├── auth.py                 # auth_bp (/login, /register, /logout)
│   ├── dashboard.py            # dashboard_bp (/dashboard, /feed)
│   ├── items.py                # items_bp (/report-item, /items/<id>)
│   ├── chat.py                 # chat_bp (/chat/<item_id>)
│   └── profile.py              # profile_bp (/profile, /resolve/<id>)
├── static/
│   ├── css/
│   │   └── custom.css          # Custom overrides
│   ├── js/
│   │   └── app.js              # Client-side form helpers & modal JS
│   └── uploads/                # Static storage for item photos
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Master layout (Navbar, Footer, Flash Messages)
│   ├── components/             # Reusable UI Partials
│   │   ├── navbar.html
│   │   └── consent_modal.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard.html          # Central Feed Page
│   ├── report_item.html        # Add Item Form
│   ├── item_detail.html        # Detailed Item View
│   ├── chat.html               # Anonymous Chat Interface
│   └── profile.html            # User Activity & Karma Points
├── tests/                      # Pytest Suite
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_items.py
└── docs/                       # Permanent Documentation
    ├── PRD.md
    ├── architecture.md
    ├── rules.md
    ├── phases.md
    ├── design.md
    └── memory.md
```
