# ModelBench

**A Django-based LLM Evaluation Platform with OAuth2 authentication, multi-model benchmarking, and automated review workflows.**

[![Django](https://img.shields.io/badge/Django-5.2-092E20.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Core Concepts](#core-concepts)
- [Review Workflow](#review-workflow)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

ModelBench is a full-featured backend platform for evaluating, comparing, and managing Large Language Models (LLMs). It provides:

- **Benchmark Management**: Create and manage benchmarks to evaluate model performance across diverse tasks.
- **Dataset Versioning**: Track datasets through multiple versions with metadata.
- **Experiment Tracking**: Run experiments against benchmarks, capturing inputs, outputs, and metrics.
- **Evaluation Pipeline**: Automated scoring using custom evaluators or LLM-as-a-judge methodologies.
- **Multi-Agent Review System**: Submit evaluations for human review with configurable workflows (pending → reviewing → approved/rejected).
- **OpenAPI/Swagger Docs**: Auto-generated API documentation via drf-spectacular.

Designed for ML teams that need structured, auditable evaluation pipelines with both automated and human oversight.

---

## Features

### Core Capabilities
- **RESTful API** — Full CRUD operations with pagination, filtering, search, and ordering
- **OAuth2 Authentication** — Token-based auth with `django-oauth-toolkit`
- **Social Login** — Google, GitHub, and Apple sign-in via `django-allauth`
- **Role-Based Access Control** — Custom `IsAdminOrReadOnly` permissions; admins can modify, others are read-only
- **Automated Logging** — Rotating file handlers capture all API activity
- **CSV Export** — Download any list resource (experiments, evaluations, etc.) as CSV
- **Data Import** — Bulk import datasets from CSV or JSON files

### Benchmark & Experiment Flow
1. Upload or define a dataset (with versions)
2. Create a benchmark tied to a dataset
3. Run an experiment: specify model + config, get generated runs
4. Evaluate runs automatically or submit for manual review
5. Track results and export reports

### Review Workflow
- Evaluations enter `PENDING` state after creation
- Admins assign reviewers; status moves to `REVIEWING`
- Reviewers approve or reject with comments
- Final status: `APPROVED` or `REJECTED`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.2.19 + Django REST Framework 3.18.3 |
| Auth | django-oauth-toolkit 3.4.1, django-allauth 65.22.1 |
| API Docs | drf-spectacular 0.30.0 (OpenAPI 3.x / Swagger UI) |
| Filtering | django-filter 26.2 |
| CORS | django-cors-headers 4.9.0 |
| Env Config | django-environ 0.14.0 |
| Database | SQLite 3 (dev), PostgreSQL recommended for production |
| OAuth Providers | Google, GitHub, Apple (via allauth) |

---

## Project Structure

```
modelbench/
├── modelbench/               # Django project config
│   ├── settings.py           # All app settings, middleware, OAuth providers
│   ├── urls.py               # Root URL dispatcher
│   ├── wsgi.py / asgi.py     # Deployment entry points
│   └── __init__.py
│
├── core/                     # Shared utilities
│   ├── permissions.py        # IsAdminOrReadOnly permission class
│   ├── mixins.py             # CSV export/mixin base classes
│   └── middleware.py         # APILoggingMiddleware
│
├── datasets/                 # Dataset management
│   ├── models.py             # Dataset, DatasetVersion
│   ├── serializers.py
│   ├── views.py              # DatasetViewSet, DatasetVersionViewSet
│   └── imports.py            # CSV/JSON import logic
│
├── benchmarks/               # Benchmark definitions
│   ├── models.py             # Benchmark model
│   ├── serializers.py
│   └── views.py              # BenchmarkViewSet
│
├── experiments/              # Experiment lifecycle
│   ├── models.py             # Experiment, ExperimentRun
│   ├── serializers.py
│   └── views.py              # ExperimentViewSet, RunViewSet
│
├── evaluations/              # Scoring & reviews
│   ├── models.py             # Evaluation, Review, ReviewComment
│   ├── serializers.py
│   └── views.py              # EvaluationViewSet, ReviewViewSet
│
├── review_workflow/          # Workflow state machine
│   ├── models.py
│   ├── services.py           # Review workflow service layer
│   └── admin.py
│
├── .env                      # Local secrets (gitignored)
├── .env.example              # Template for environment variables
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- pip
- A PostgreSQL database (recommended for production; SQLite works for development)

### Quick Start (Development)

```bash
# 1. Clone the repository
git clone https://github.com/yashanand110606/modelbench.git
cd modelbench

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment template and configure
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux

# Edit .env and set your values, at minimum:
#   DEBUG=True
#   SECRET_KEY=<generate-a-strong-key>
#   DATABASE_URL=sqlite:///db.sqlite3   (or postgresql://...)

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for admin access)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

---

## API Documentation

Once the server is running, interactive API documentation is available at:

| Endpoint | Description |
|----------|-------------|
| `/api/docs/` | Swagger UI — browse and test all endpoints |
| `/api/redoc/` | ReDoc alternative view |
| `/api/schema/` | Raw OpenAPI 3 specification (JSON) |

### Key API Endpoints

All API routes are prefixed with `/api/`.

#### Authentication
- `POST /api/auth/login/` — Session login (username/password)
- `POST /api/auth/register/` — Register a new account
- `POST /api/oauth/token/` — OAuth2 token exchange
- `GET/POST /api/socialaccount/providers/` — List/configure social providers

#### Datasets
- `GET/POST /api/datasets/` — List/create datasets
- `GET /api/datasets/{id}/versions/` — List versions of a dataset
- `POST /api/datasets/{id}/import/` — Bulk import from CSV/JSON

#### Benchmarks
- `GET/POST /api/benchmarks/` — List/create benchmarks
- Filter by `name`, `description`, `dataset`
- Search on `name`, `description`

#### Experiments
- `GET/POST /api/experiments/` — List/create experiments
- `GET/POST /api/experiments/{id}/runs/` — Manage experiment runs
- Each run captures: prompt, expected output, actual output, timestamp

#### Evaluations
- `GET/POST /api/evaluations/` — List/create evaluations
- Filter by `experiment`, `run`, `status`
- Scored automatically or submitted for human review

#### Reviews
- `GET/POST /api/reviews/` — Create and manage review assignments
- `PATCH /api/reviews/{id}/` — Update review status (approve/reject) with comments
- Status flow: `PENDING` → `REVIEWING` → `APPROVED` / `REJECTED`

### Pagination, Filtering & Search

All list endpoints support:
- **Pagination**: `?page=1&page_size=20` (default page size: 20)
- **Filtering**: `?field=value` (see individual endpoint docs)
- **Search**: `?search=query` (full-text on name/description fields)
- **Ordering**: `?ordering=-created_at` (prefix `-` for descending)

### CSV Export

Every list endpoint supports CSV download:
```
GET /api/experiments/?export=csv
```

---

## Authentication

ModelBench supports three authentication methods:

### 1. Session Authentication (Cookie-based)
Useful for browser-based clients. Log in via the DRF login endpoint or the Django admin panel.

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### 2. OAuth2 Bearer Tokens
For programmatic/API access. Obtain a token first:

```bash
curl -X POST http://localhost:8000/api/oauth/token/ \
  -d "grant_type=password&username=admin&password=your-password&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
```

Then include the token in requests:
```
Authorization: Bearer <access_token>
```

### 3. Social Authentication (allauth)
Sign up/sign in using Google, GitHub, or Apple. Configure provider credentials in `.env`:

```env
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GITHUB_CLIENT_ID=your-github-client-id-here
GITHUB_CLIENT_SECRET=your-github-client-secret-here
APPLE_CLIENT_ID=your-apple-client-id-here
APPLE_CLIENT_SECRET=your-apple-client-secret-here
APPLE_KEY_ID=your-apple-key-id-here
APPLE_CERTIFICATE_KEY=your-apple-certificate-key-here
```

---

## Core Concepts

### Dataset → Benchmark → Experiment → Evaluation

The data model flows logically:

1. **Dataset** — The raw input/output pairs used for evaluation (e.g., a CSV of questions and answers). Can have multiple **Versions** to track iterations.
2. **Benchmark** — Defines *how* a dataset is evaluated (scoring criteria, model configs, parameters). Tied to one dataset.
3. **Experiment** — A specific execution instance: run a benchmark with concrete model settings. Contains multiple **Runs**.
4. **Run** — A single model inference result: input prompt, expected output, actual output, raw response.
5. **Evaluation** — The scored result of a run (automatically computed or manually assigned).
6. **Review** — Human approval process for evaluations. Ensures quality control before finalizing results.

### Permission Model

- **Authenticated users** can `GET` (read) all resources.
- **Staff/admin users** can `POST`, `PUT`, `PATCH`, `DELETE` (write) resources.
- Unauthenticated requests receive `401 Unauthorized`.

---

## Review Workflow

The `review_workflow` app implements a state machine for evaluation quality control:

```
                  ┌──────────────┐
                  │   PENDING    │  ← New evaluations land here
                  └──────┬───────┘
                         │ assign_reviewer()
                  ┌──────▼───────┐
                  │  REVIEWING   │  ← Reviewer has been notified
                  └──────┬───────┘
                         │
                ┌────────┴────────┐
                ▼                 ▼
       ┌──────────────┐   ┌──────────────┐
       │   APPROVED   │   │   REJECTED   │
       └──────────────┘   └──────────────┘
```

Reviews include:
- Assigned reviewer (`ForeignKey` to User)
- Status transitions tracked automatically
- Optional comment field for justification
- Timestamped audit trail

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test datasets
python manage.py test evaluations
python manage.py test review_workflow

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report -m
```

---

## Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Use a proper `SECRET_KEY` (never the default)
3. Configure PostgreSQL: `DATABASE_URL=postgresql://user:pass@host:port/dbname`
4. Set `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
5. Set up a reverse proxy (Nginx) or use Gunicorn:
   ```bash
   gunicorn modelbench.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```
6. Configure email backend for allauth (required for password reset, even with optional email verification)
7. Set up static file collection:
   ```bash
   python manage.py collectstatic
   ```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEBUG` | No | `False` | Enable debug mode |
| `SECRET_KEY` | **Yes** | — | Django secret key |
| `DATABASE_URL` | No | `sqlite:///db.sqlite3` | Database connection string |
| `ALLOWED_HOSTS` | No | `[]` | Comma-separated allowed hosts |
| `CORS_ALLOW_ALL_ORIGINS` | No | `False` | Allow all CORS origins (dev only) |
| `CORS_ALLOWED_ORIGINS` | No | localhost:3000,8000 | Specific allowed origins |
| `GOOGLE_CLIENT_ID` | No | — | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | — | Google OAuth client secret |
| `GITHUB_CLIENT_ID` | No | — | GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | No | — | GitHub OAuth client secret |

See [.env.example](.env.example) for the full reference.

---

## Security

This project follows several security best practices:

- **Secrets in environment variables** — `.env` is gitignored; never commit credentials
- **SQL injection prevention** — Django ORM handles query parameterization automatically
- **CSRF protection** — Enabled by default via `CsrfViewMiddleware`
- **X-Frame-Options** — Clickjacking protection enabled
- **HSTS** — HTTP Strict Transport Security when `DEBUG=False`
- **Input validation** — DRF serializers validate all incoming data
- **RBAC** — Admin-only write permissions prevent unauthorized modifications
- **Logging** — All API requests logged to rotating file handler (`logs/api.log`)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Ensure all tests pass: `python manage.py test`
6. Push to your fork and open a Pull Request

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Use descriptive variable and function names
- Keep functions focused and under 50 lines where possible
- Document non-obvious business logic with inline comments

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

Built with [Django](https://www.djangoproject.com/), [DRF](https://www.django-rest-framework.org/), and [allauth](https://docs.allauth.org/).
