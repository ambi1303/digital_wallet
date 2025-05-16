# Digital Wallet System with Fraud Detection

A secure digital wallet backend built with FastAPI, featuring cash management, multi-currency support, and fraud detection.

## Features

### Core Features
- **User Authentication:** Registration and login with bcrypt hashed passwords and JWT token-based authentication.
- **Wallet Operations:** Deposit, withdraw, and transfer virtual cash between users.
- **Multi-Currency Support:** Transactions and balances support multiple currencies (USD, INR, EUR, etc.).
- **Transaction History:** Maintains detailed history of all wallet transactions per user.
- **Transaction Validation:** Prevents overdrafts, negative amounts, invalid transfers.
- **Fraud Detection:** Rule-based checks for rapid transfers and large withdrawals with flagged transactions.
- **Admin APIs:** View flagged transactions, aggregate balances, and top users by transaction volume.

### Bonus Features
- **Scheduled Fraud Scanning:** Daily automated fraud scans using APScheduler.
- **Soft Delete:** Users and transactions are soft deleted (marked inactive, not physically removed).
- **Email Alerts:** Mock email notifications sent to users upon suspicious transactions.
- **Swagger Documentation:** Fully documented RESTful API available at `/docs`.

## Tech Stack
- **Backend Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Authentication:** JWT, bcrypt
- **Scheduler:** APScheduler for periodic fraud detection
- **Database:** SQLite (default), easily replaceable with PostgreSQL/MySQL
- **Python Version:** 3.12+

## API Overview

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Wallet
- `POST /wallet/` - Perform deposit, withdraw, or transfer
- `GET /wallet/history` - Get transaction history (filtered for user)
- `GET /wallet/balance` - Get current balance(s) per currency

### Admin
- `GET /admin/flagged-transactions` - View flagged suspicious transactions
- `GET /admin/total-balances` - Aggregate user balances across currencies
- `GET /admin/top-users` - List top users by transaction volume

### Fraud Detection
- Scheduled daily fraud scan flags suspicious activity automatically
- Mock email alerts on suspicious transactions

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ambi1303/digital_wallet.git
   cd digital_wallet
2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Initialize the Database 
python create_db.py

5. Run the FastApi Server 
uvicorn app.main:app --reload

6. Access API docs at http://localhost:8000/docs

