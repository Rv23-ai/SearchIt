# Product Requirements Document (PRD) - Campus Lost & Found System

## 1. Executive Summary & Purpose
The **Campus Lost & Found Platform** is a monolithic web application built using Python (Flask). It provides a centralized, trustworthy, and efficient digital department for students and faculty to report, search, verify, and retrieve lost items on campus.

### 1.1 Core Objectives
- **Accelerate Item Recovery:** Provide structured metadata, visual verification, indoor floor hierarchy, and secret verification questions to reunite owners with lost items within hours.
- **Privacy & Safety First:** Protect student privacy through domain-restricted access (`@college.edu`), student ID verification, anonymous in-app messaging, and explicit safety consent modals.
- **Incentivize Honesty:** Reward users with Goodwill / Karma points when they return found items.

---

## 2. Target Audience & Roles

| Role | Access Level | Responsibilities |
| :--- | :--- | :--- |
| **Student / Faculty** | Verified User | Report lost/found items, view feed, initiate claim chats, mark items as resolved. |
| **Campus Admin** | Superuser / Admin | Moderate flagged posts, oversee unresolved items, verify institutional access. |

---

## 3. Detailed Feature Specifications

### 3.1 Authentication & Onboarding
- **Institutional Domain Restrictor:** Registration strictly enforced for campus email domains (`*@college.edu` or institutional equivalent).
- **Student ID Verification:** Requires Admission / Roll Number during registration alongside email to prevent spoofing.
- **Session Management:** Secure cookie-based sessions managed via Flask `session` (`HTTPOnly`, `SameSite=Lax`).

### 3.2 Quick-Action Item Reporting
- **Category Chips:** One-click item tags (`Phone`, `Keys`, `Earbuds`, `ID Card`, `Bag`, `Accessories`, `Documents`).
- **3-Tier Indoor Location Selector:**
  1. *Building / Block:* Admin Block, Central Library, Science Block A, Main Canteen, Sports Complex.
  2. *Floor Level:* Ground Floor, 1st Floor, 2nd Floor, 3rd Floor, Outdoor Grounds.
  3. *Spot Detail:* Specific landmark description (e.g., "Desk #12, Row 3 near reading hall window").
- **Mock Image Upload:** Drag-and-drop zone showing instant client-side image preview and upload progress indicator.
- **Secret Claim Detail (Anti-Fraud):** Finder specifies a hidden verification detail (e.g., "What sticker is on the phone case?"). Claimant must answer this in chat to prove ownership.

### 3.3 Central Campus Feed & Filter System
- **Unified Feed:** Stream of items displaying photo preview, category badge, indoor location, and status.
- **Filters:** Quick toggle tabs (`ALL ITEMS`, `LOST ITEMS`, `FOUND ITEMS`) and search by keyword or building.

### 3.4 Anonymous In-App Chat & Consent Modal
- **Peer-to-Peer Messaging:** Enables finder and claimant to communicate without revealing personal phone numbers or social handles.
- **Mandatory Risk Consent Modal:** Intercepts the user before opening a chat room, requiring explicit agreement to a safety disclaimer regarding voluntary phone number exchange.

### 3.5 Student Profile & Karma Score
- **Personal Activity Hub:** Displays active lost posts, found uploads, and resolved claims.
- **Karma / Goodwill Points:** Awards +100 Goodwill Points upon successfully marking an item as "Resolved & Returned".

---

## 4. Edge Cases & Safety Rules
1. **False Claims:** Secret Verification Question prevents unauthorized users from claiming items.
2. **Domain Rejection:** Generic email domains (`@gmail.com`, `@yahoo.com`) are explicitly rejected during registration with clear UI feedback.
3. **Inappropriate Content:** Users can report or flag suspicious item listings.
