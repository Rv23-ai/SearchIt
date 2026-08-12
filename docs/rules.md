# Database Schema & AI Developer Rules

## 1. Database Schema Specifications

### `users` Table
- `id`: Integer (Primary Key, Auto-increment)
- `college_email`: String(120) (Unique, Indexed, Not Null)
- `student_id`: String(50) (Unique, Indexed, Not Null)
- `department`: String(100) (Not Null)
- `password_hash`: String(255) (Not Null)
- `karma_score`: Integer (Default: 0)
- `created_at`: DateTime (Default: UTC Now)

### `items` Table
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String(150) (Not Null)
- `category`: String(50) (Not Null) -- Phone, Keys, Earbuds, ID Card, Bag, Accessories, Documents
- `item_type`: String(10) (Not Null) -- LOST or FOUND
- `status`: String(20) (Default: 'ACTIVE') -- ACTIVE, CLAIMED, RESOLVED
- `building`: String(100) (Not Null)
- `floor`: String(50) (Not Null)
- `spot_description`: Text (Not Null)
- `secret_question`: String(255) (Nullable) -- For FOUND items
- `image_url`: String(255) (Nullable)
- `user_id`: Integer (Foreign Key -> users.id)
- `created_at`: DateTime (Default: UTC Now)

### `chat_messages` Table
- `id`: Integer (Primary Key, Auto-increment)
- `item_id`: Integer (Foreign Key -> items.id)
- `sender_id`: Integer (Foreign Key -> users.id)
- `receiver_id`: Integer (Foreign Key -> users.id)
- `message_text`: Text (Not Null)
- `timestamp`: DateTime (Default: UTC Now)

---

## 2. AI Developer Rules & Anti-Hallucination Directives

### Absolute Code Quality Imperatives
1. **NO INCOMPLETE CODE:** Never write `// TODO`, `...`, or truncated code blocks. Provide full, working, copy-pasteable files.
2. **STRICT DEPENDENCY LOCK:** Use ONLY packages explicitly defined in `requirements.txt`:
   - `Flask`
   - `Flask-SQLAlchemy`
   - `python-dotenv`
   - `Werkzeug`
3. **NO EXTRA JS FRAMEWORKS:** Do NOT introduce React, Vue, Svelte, or npm dependencies. All interactivity must use vanilla JavaScript or Tailwind CSS.
4. **NO HARDCODED SECRETS:** All configurations (DB paths, secret keys, session configuration) must be imported from `config.py`.

---

### Flask Architecture Best Practices
- **Blueprints Pattern:** Organize routes cleanly into Flask Blueprints under `routes/`.
- **ORMs Exclusively:** Use Flask-SQLAlchemy `db.session` for all queries. Raw SQL concatenation is strictly forbidden.
- **Security:** Use Werkzeug `generate_password_hash` and `check_password_hash` for password storage.
- **Session Auth:** Secure routes using a custom `@login_required` decorator checking Flask `session['user_id']`.
- **Flash Feedback:** Use Flask `flash()` messages for user feedback (e.g., success banners, error warnings).

---

### UI & Template Guidelines
- Style ALL templates using Tailwind CSS v3 utility classes loaded via CDN in `base.html`.
- Maintain unified color tokens defined in `docs/design.md`.
- Ensure forms render responsive labels, input focus rings, and clear error messages.

---

### State & Memory Update Protocol
- Immediately after executing ANY phase task, update `docs/memory.md`.
- Record: Completed tasks, files created/modified, active blockers, and current phase status.
