# Incident Management System

Automated incident creation, prioritisation, and routing for Pi-7 helpline.

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```

## Tech Stack
- Flask, SQLAlchemy, Flask-Login
- SQLite database
- PyTest for testing