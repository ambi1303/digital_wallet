from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

scheduler = BackgroundScheduler()

def start_scheduler(app: FastAPI):
    from app.services import fraud  

    # Schedule daily fraud scan every 24 hours
    scheduler.add_job(fraud.daily_fraud_scan, "interval", days=1)
    scheduler.start()

    # Shut down scheduler on app shutdown
    @app.on_event("shutdown")
    def shutdown_event():
        scheduler.shutdown()
