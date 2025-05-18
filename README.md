# Digital Wallet System

A secure and feature-rich digital wallet system with cash management and fraud detection capabilities.

## Features

- User Authentication & Session Management
- Wallet Operations (Deposit, Withdraw, Transfer)
- Multi-currency Support
- Transaction Processing & Validation
- Fraud Detection System
- Admin & Reporting APIs
- Email Alerts for Suspicious Activities
- Scheduled Fraud Scans

## Tech Stack

- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT (Authentication)
- APScheduler (Task Scheduling)
- Pydantic (Data Validation)

## Prerequisites

- Python 3.8+
- PostgreSQL
- SMTP Server (for email alerts)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd digital_wallet
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```
Edit .env with your configuration

5. Initialize database:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
digital_wallet/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API endpoints
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   ├── tasks/           # Scheduled tasks
│   ├── utils/           # Utilities
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # Application entry
├── tests/               # Test files
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Rate limiting
- Transaction validation
- Fraud detection rules
- Email alerts for suspicious activities

## Development

1. Run tests:
```bash
pytest
```

2. Run linting:
```bash
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

