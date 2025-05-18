# Digital Wallet Application

A full-stack digital wallet application built with Angular (frontend) and FastAPI (backend).

## Project Structure

```
digital_wallet/
├── frontend/           # Angular application
└── backend/           # FastAPI application
```

## Backend (FastAPI)

The backend is built with FastAPI and provides a robust API for the digital wallet application.

### Features
- User authentication and authorization
- Wallet management
- Transaction processing
- Admin dashboard
- Fraud detection
- Automated reporting

### Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python create_db.py
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Frontend (Angular)

The frontend is built with Angular and provides a modern, responsive user interface.

### Features
- User authentication
- Wallet dashboard
- Transaction management
- Real-time balance updates
- Admin interface
- Responsive design

### Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
ng serve
```

The application will be available at `http://localhost:4200`

## Development

### Backend Development
- API documentation is available at `/docs` when running the backend
- Run tests: `pytest`
- Database migrations: `alembic upgrade head`

### Frontend Development
- Run tests: `ng test`
- Build for production: `ng build --prod`
- Lint code: `ng lint`

## Docker Support

Both frontend and backend can be run using Docker:

```bash
# Build and run backend
docker build -t digital-wallet-backend ./backend
docker run -p 8000:8000 digital-wallet-backend

# Build and run frontend
docker build -t digital-wallet-frontend ./frontend
docker run -p 4200:80 digital-wallet-frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

