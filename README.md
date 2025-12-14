# E-Commerce API

FastAPI-based e-commerce backend with user auth, products, cart, and orders.

## Features
- User registration & JWT login
- Product CRUD (admin)
- Add to cart
- Checkout & order creation
- PostgreSQL + SQLAlchemy + Alembic

## Setup

1. `cp .env.example .env`
2. Update `.env` with your DB URL and secret key
3. `pip install -r requirements.txt`
4. `alembic upgrade head` (after init)
5. `uvicorn app.main:app --reload`

## API Docs
- `/docs` - Swagger UI
- `/redoc` - ReDoc

## Admin
Use `/users/` to create admin (then manually set `is_admin=1` in DB) or add seed script.