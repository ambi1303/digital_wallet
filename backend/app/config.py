import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wallet.db")

# Application Settings
APP_NAME = "Digital Wallet API"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Transaction Limits
MAX_TRANSACTION_AMOUNT = float(os.getenv("MAX_TRANSACTION_AMOUNT", "10000"))
MIN_TRANSACTION_AMOUNT = float(os.getenv("MIN_TRANSACTION_AMOUNT", "0.01"))
DAILY_TRANSACTION_LIMIT = float(os.getenv("DAILY_TRANSACTION_LIMIT", "50000"))

# Fraud Detection Settings
SUSPICIOUS_TRANSACTION_THRESHOLD = float(os.getenv("SUSPICIOUS_TRANSACTION_THRESHOLD", "5000"))
RAPID_TRANSACTION_WINDOW = int(os.getenv("RAPID_TRANSACTION_WINDOW", "300"))  # 5 minutes in seconds
MAX_RAPID_TRANSACTIONS = int(os.getenv("MAX_RAPID_TRANSACTIONS", "5"))

# Email Settings (for notifications)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# JWT Token Generation
def create_access_token(data: dict):
    from jose import jwt
    from datetime import datetime
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
