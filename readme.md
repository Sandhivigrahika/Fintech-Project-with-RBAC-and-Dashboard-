# Fintech Financial Records API 🚀



[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Framework-blue?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Reliable%20DB-brightgreen)](https://www.postgresql.org/)
[![Railway](https://img.shields.io/badge/Hosted-Railway-orange?logo=railway)](https://railway.app/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-teal)](https://pydantic.dev/)
[![JWT](https://img.shields.io/badge/JWT-Auth-purple)](https://jwt.io/)

**Secure financial records management API** with **Role-Based Access Control (RBAC)**, full CRUD, advanced filtering, dashboard analytics, and CSV export.

**Live API:** [https://fintect-api-production.up.railway.app/docs](https://fintect-api-production.up.railway.app/docs)

## 🎯 Quick Start

### Test Credentials

| Role     | Username                      | Password   |
|----------|-------------------------------|------------|
| **Admin** | `neel.hans97@gmail.com`       | `admin123` |
| **Analyst** | `analyst1@example.com`     | `analyst123` |
| **Viewer** | `viewer1@example.com`       | `viewer123` |

**Click "Authorize"** in `/docs` and login to test protected endpoints.

## 🛡️ Role-Based Access Control (RBAC)

| Role    | Permissions |
|---------|-------------|
| **Admin** | Full CRUD + User management + Promotion |
| **Analyst** | Read records + Dashboard + CSV export |
| **Viewer** | Dashboard read-only |

**RBAC enforced via Enums** for type safety.

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/auth/register` | Public | Create new user |
| `POST` | `/auth/token` | Public | Login (returns JWT) | Default role ->Viewer

### User Management (Admin Only)
| Method | Endpoint | Description | Privilege
|--------|------------------|-------------|
| `GET` | `/admin/users/` | List all users | Admin
| `PATCH` | `/admin/users/{user_id}/role` | Update user role | Admin
| `PATCH` | `/admin/users/{user_id}/status` | Activate/deactivate user | Admin

### Financial Records
| Method | Endpoint | Access | Description |
|--------|---------------------|--------|-------------|
| `POST` | `/records/management/create` | Admin | Create record |
| `GET` | `/records/management/` | All | List with filters |
| `PATCH` | `/records/management/{record_id}` | Admin | Update record |
| `DELETE` | `/records/management/{record_id}/delete` | Admin | Delete record |

**Filters:** `page`, `page_size`, `customer_name`, `mobile_number`, `category`, `type`, `date_from`, `date_to`

### Dashboard Analytics
| Method | Endpoint | Access | Description |
|--------|--------------------------------|--------|-------------|
| `GET` | `/dashboard/financial_summary/` | Analyst + Admin | Overall totals |
| `GET` | `/dashboard/financial_summary/customer/summary/{mobile_number}` | Analyst + Admin  | Customer summary |
| `GET` | `/dashboard/financial_summary/category/{category}` | Analyst + Admin  | Category breakdown |
| `GET` | `/dashboard/financial_summary/customer/recent_activity/{mobile_number}` |Analyst + Admin  | Recent customer activity |
| `GET` | `/dashboard/financial_summary/trends/monthly` | Analyst + Admin  | Monthly income/expense trends |
| `GET` | `/dashboard/financial_summary/export/csv` | Analyst + Admin  | Export all records as CSV |

### Health Check



## 🛠 Tech Stack
- Framework: FastAPI 
- Database: PostgreSQL (Railway hosted)
- ORM: SQLAlchemy
- Auth: JWT (OAuth2PasswordBearer)
- Validation: Pydantic v2 + field_validator
- Deployment: Railway (auto-deploy from GitHub)


## 🎨 Key Features

### ✅ Input Validation
- Pydantic schemas with `field_validator`
- Automatic type conversion
- Input normalization (whitespace trimming)
- Clear validation error messages

### ✅ Error Handling
- 400: Bad Request (validation/duplicates)
- 401: Unauthorized (auth failures)
- 422: Pydantic validation details


### ✅ Data Persistence
- PostgreSQL + SQLAlchemy ORM
- DATABASE_URL env var (works local + production)
- Auto table creation + seed data on startup


### ✅ Security
- JWT token authentication
- RBAC enforced via dependency injection
- Password hashing (bcrypt)
- SQL injection protection (ORM)


## 📁 Project Structure
fintech_project/
├── app/
│ ├── core/ # Config, security, dependencies
│ ├── db/ # Database session, models
│ ├── enums/ # RecordType, RecordCategory, UserRole
│ ├── models/ # User, FinancialRecord
│ ├── routes/ # API routers
│ ├── schemas/ # Pydantic models
│ └── scripts/ # Seed data, table creation
├── main.py # FastAPI app + lifespan
├── requirements.txt
├── .env.example
└── Procfile # Railway deployment


## Tradeoffs
- The admin credential is currently hardcoded in the seed_admins.py however for production it may be shifted to .env file
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


## 🚀 Local Setup

```bash
git clone <repo>
cd fintech_project

# Virtual env
python -m venv venv
venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```


## 🌐 Production

**Hosted:** [https://fintect-api-production.up.railway.app/docs](https://fintect-api-production.up.railway.app/docs)

Auto-deploys on GitHub push
PostgreSQL (Railway managed)
DATABASE_URL configured
