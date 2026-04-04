# Fintech Dashboard API

A backend API for a finance dashboard system built with FastAPI, SQLAlchemy, and SQLite/PgSql.

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (local), PostgreSQL (production)
- **ORM:** SQLAlchemy
- **Authentication:** JWT via python-jose
- **Password Hashing:** bcrypt via passlib
- **Validation:** Pydantic v2

---

## Setup

1. **Clone the repo**
   git clone <repo-url>
   cd fintech_project

2. **Create and activate virtual environment**
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux

3. **Install dependencies**
   pip install -r requirements.txt

4. **Create `.env` file**
   cp .env.example .env

   Fill in the values:
   DATABASE_URL=sqlite:///./fintech.db
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=60

5. **Run the server**
   uvicorn main:app --reload

Tables and seed data are created automatically on startup.

---

## Default Admin Credentials

email: neel.hans97@gmail.com
password: admin123

---

## API Documentation

Once the server is running, visit:
http://127.0.0.1:8000/docs

Click **Authorize** and login with the admin credentials to test protected endpoints.

---

## Roles

| Role | Permissions |
|---|---|
| Admin | Full access — manage users, records, dashboard |
| Analyst | View records and dashboard summaries |
| Viewer | View dashboard data only |

---

## Endpoints

### Auth
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /auth/register | Register a new user | Public |
| POST | /auth/token | Login and get JWT token | Public |


### Admin - User Management
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /admin/users/ | Get all users | Admin |
| PATCH | /admin/users/{id}/role | Update user role | Admin |
| PATCH | /admin/users/{id}/status | Activate or deactivate user | Admin |

### Financial Records
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /records/ | Get all records with filters | Analyst, Admin |
| POST | /records/ | Create a new record | Admin |
| PATCH | /records/{id} | Update a record | Admin |
| DELETE | /records/{id} | Soft delete a record | Admin |

### Dashboard
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /dashboard/summary | Total income, expenses, net balance | Analyst, Admin |
| GET | /dashboard/category | Category wise totals | Analyst, Admin |
| GET | /dashboard/trends | Monthly trends | Analyst, Admin |

---

## Project Structure

fintech_project/
├── main.py
├── requirements.txt
├── .env.example
├── Procfile
└── app/
    ├── core/
    │   ├── dependencies.py
    │   ├── rbac.py
    │   └── security.py
    ├── db/
    │   ├── base.py
    │   └── session.py
    ├── enums/
    │   └── enums.py
    ├── models/
    │   ├── user.py
    │   └── financial_record.py
    ├── routes/
    │   ├── auth_router.py
    │   ├── admin_routes.py
    │   ├── financial_routes.py
    │   └── dashboard_routes.py
    ├── schemas/
    │   ├── register_login_schema.py
    │   ├── user_response.py
    │   └── financial_record_schema.py
    ├── scripts/
    │   ├── data/
    │   │   └── financial_records.json
    │   ├── create_tables.py
    │   ├── seed_admin.py
    │   └── seed_financial.py
    └── services/
        ├── auth_service.py
        ├── user_service.py
        ├── financial_service.py
        └── dashboard_service.py

---

## Assumptions

- Financial records represent company customer data, not tied to individual users
- Users represent internal company staff with different access levels
- Soft delete is used for financial records — deleted records are hidden but not removed from the database
- Admin credentials are seeded automatically on first startup

---

## Tradeoffs
- The admin credential is currently hardcoded in the  seed_admins.py however for production it may be shifted to .env file
- Used os.getenv() for environment variables directly. In production this would be replaced with pydantic BaseSettings for typed config management and validation
- Sync vs Async: Used synchronous SQLAlchemy Session with def routes for simplicity. A production system would benefit from AsyncSession with asyncpg for true async I/O, but that added complexity was out of scope for this assignment.

### Database
- Used **SQLite** locally for simplicity. Switched to **PostgreSQL** on Railway via `DATABASE_URL` environment variable with no code changes needed.
- In production, **Alembic** would be used for schema migrations instead of `create_all` on startup.

### Authentication
- Used `OAuth2PasswordRequestForm` for the login endpoint as it follows FastAPI's standard auth pattern and works seamlessly with Swagger UI for testing.
- `SECRET_KEY` is stored in `.env`. In production this should be a long random string stored in a secrets manager.

### Async vs Sync
- Used synchronous SQLAlchemy `Session` with `def` routes for simplicity. A production system would benefit from `AsyncSession` with `asyncpg` for true async I/O.

### Configuration
- Used `os.getenv()` for environment variables directly. In production this would be replaced with Pydantic `BaseSettings` for typed config management and validation.

### Pagination
- Pagination is not implemented on list endpoints. In production, limit/offset or cursor based pagination would be added.

### Seed Data
- Tables and seed data are created automatically on startup via FastAPI lifespan. In production, Alembic migrations and a separate deployment step would handle this.

---

## Deployment

Deployed on Railway. Live API:
<your-railway-url>

API Docs:
<your-railway-url>/docs