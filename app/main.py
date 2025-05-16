from fastapi import FastAPI
from app.api import auth, wallet, admin
from app.utils.scheduler import start_scheduler

app = FastAPI(
    title="Digital Wallet API",
    description="Backend system for wallet operations and fraud detection",
    version="1.0.0"
)

# Start the scheduler after app creation
start_scheduler(app)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "Digital Wallet API is running 🚀"}
