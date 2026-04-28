# Full-Stack Billing & Analytics Platform (Django + REST)

## Features
- User authentication (login/logout)
- Create and manage invoices
- Product inventory tracking
- PDF invoice generation
- REST API for products and invoices
- Real-time total calculation

## Tech Stack
- Django
- Django REST Framework
- Bootstrap
- SQLite

## API Endpoints
- /billing/api/products/
- /billing/api/invoices/
- /billing/api/invoice/<id>/

## How to Run
```bash
git clone <repo>
cd project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
