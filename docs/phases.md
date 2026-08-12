# Granular Implementation Roadmap

---

### Phase 1: Environment Setup & Flask Application Factory
- **Tasks:**
  - Create `.gitignore`, `.env`, `.env.example`, `requirements.txt`, and `LICENSE`.
  - Build `config.py` using `python-dotenv`.
  - Build `database.py` with Flask-SQLAlchemy `db` initialization.
  - Create `app.py` as the Flask Application Factory (`create_app()`).
  - Create `templates/base.html` with Tailwind CSS CDN.
  - Create `templates/index.html` landing page.
- **Verification:** Run `python app.py` and verify HTTP 200 at `http://127.0.0.1:5000`.

---

### Phase 2: Database Schema & Models Implementation
- **Tasks:**
  - Build `models.py` defining `User`, `Item`, and `ChatMessage` models.
  - Create automatic database table creation setup (`db.create_all()`) within app context in `app.py`.
- **Verification:** Run app and verify SQLite file `campus_data.db` is generated with all 3 tables.

---

### Phase 3: Domain-Restricted Authentication System
- **Tasks:**
  - Build `routes/auth.py` Blueprint with `/register`, `/login`, and `/logout` routes.
  - Implement password hashing using `werkzeug.security`.
  - Enforce `@college.edu` domain validation regex and Student ID validation.
  - Build `templates/auth/register.html` and `templates/auth/login.html`.
- **Verification:** Registering `@gmail.com` fails; registering `@college.edu` succeeds and logs user into session.

---

### Phase 4: Central Dashboard Feed & Filter System
- **Tasks:**
  - Build `routes/dashboard.py` Blueprint handling `/dashboard`.
  - Build `templates/dashboard.html` rendering item cards with filter tabs (`ALL`, `LOST`, `FOUND`).
  - Add search bar filtering by keyword or building name.
- **Verification:** Reported items render dynamically on dashboard with working filter buttons.

---

### Phase 5: Structured Item Reporting Module
- **Tasks:**
  - Build `routes/items.py` Blueprint handling `/report-item`.
  - Build `templates/report_item.html` containing:
    - Category chip selector.
    - 3-tier location selector (*Building ➔ Floor ➔ Spot*).
    - Mock image uploader preview UI.
    - Secret verification detail input.
  - Save submitted item to SQLite database via `db.session`.
- **Verification:** Submitting the form writes item to DB and redirects to dashboard displaying the new item.

---

### Phase 6: Item Detail Page & Secret Verification Claim
- **Tasks:**
  - Add `/items/<int:item_id>` route in `routes/items.py`.
  - Build `templates/item_detail.html` rendering metadata, location description, and poster info.
  - Implement secret detail verification prompt for items marked as `FOUND`.
- **Verification:** Item metadata renders completely; non-owners are prompted for secret detail before contact.

---

### Phase 7: Privacy Consent System & In-App Chat
- **Tasks:**
  - Create `templates/components/consent_modal.html` with explicit safety and risk disclaimer.
  - Build `routes/chat.py` Blueprint handling anonymous user-to-user messaging per item.
  - Build `templates/chat.html` rendering message history and send form.
- **Verification:** User must check "I Agree" on consent modal before chat room unlocks.

---

### Phase 8: Profile Page, Karma Score & Resolution
- **Tasks:**
  - Build `routes/profile.py` Blueprint handling `/profile`.
  - Build `templates/profile.html` showing user's posts, claimed items, and Karma Score.
  - Implement "Mark as Resolved & Returned" route that grants +100 Karma points to the finder.
- **Verification:** Resolving an item updates status to `RESOLVED` and increments finder's Karma score by 100.

---

### Phase 9: Automated Tests & Validation Suite
- **Tasks:**
  - Build `tests/test_auth.py` testing domain validation, login, and session persistence using Flask test client.
  - Build `tests/test_items.py` testing item creation and resolution logic.
- **Verification:** Run `pytest` and confirm all tests pass cleanly.

---

### Phase 10: Final Audit & Documentation Wrap-up
- **Tasks:**
  - Perform UI responsiveness, link validity, and session security audit.
  - Finalize `README.md` with execution commands.
  - Update `docs/memory.md` marking project complete.
- **Verification:** Complete end-to-end user workflow functions smoothly without errors.
