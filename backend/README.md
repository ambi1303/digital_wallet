# Digital Wallet Backend

This is the backend API for the Digital Wallet application, built with FastAPI.

## Features

- User authentication with JWT tokens
- Wallet management
- Transaction processing
- Admin dashboard
- Email notifications
- Fraud detection

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration.

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── security.py
│   ├── schemas/
│   ├── services/
│   └── utils/
├── main.py
├── requirements.txt
└── .env
```

### Running Tests

```bash
pytest
```

### Code Style

This project uses Black for code formatting:

```bash
black .
``` 