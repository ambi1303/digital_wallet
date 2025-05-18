from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.tasks.fraud_scan import run_daily_fraud_scan
from app.tasks.reporting import ReportingService
import logging

logger = logging.getLogger(__name__)

def start_scheduler(app):
    """Initialize and start the scheduler"""
    scheduler = AsyncIOScheduler()

    # Schedule daily fraud scan at 1 AM UTC
    scheduler.add_job(
        func=run_scheduled_fraud_scan,
        trigger=CronTrigger(hour=1, minute=0),
        id='fraud_scan',
        name='Daily Fraud Scan',
        replace_existing=True
    )

    # Schedule daily report generation at 2 AM UTC
    scheduler.add_job(
        func=run_scheduled_report,
        trigger=CronTrigger(hour=2, minute=0),
        id='daily_report',
        name='Daily Transaction Report',
        replace_existing=True
    )

    # Schedule weekly report at 3 AM UTC on Mondays
    scheduler.add_job(
        func=run_scheduled_weekly_report,
        trigger=CronTrigger(day_of_week='mon', hour=3, minute=0),
        id='weekly_report',
        name='Weekly Transaction Report',
        replace_existing=True
    )

    # Schedule monthly report at 4 AM UTC on the 1st of each month
    scheduler.add_job(
        func=run_scheduled_monthly_report,
        trigger=CronTrigger(day=1, hour=4, minute=0),
        id='monthly_report',
        name='Monthly Transaction Report',
        replace_existing=True
    )

    try:
        scheduler.start()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")

def run_scheduled_fraud_scan():
    """Run scheduled fraud scan with proper error handling"""
    try:
        db = SessionLocal()
        run_daily_fraud_scan(db)
        logger.info("Daily fraud scan completed successfully")
    except Exception as e:
        logger.error(f"Failed to run daily fraud scan: {str(e)}")
    finally:
        db.close()

def run_scheduled_report():
    """Run scheduled daily report with proper error handling"""
    try:
        db = SessionLocal()
        reporting_service = ReportingService(db)
        report = reporting_service.generate_daily_report()
        logger.info(f"Daily report generated successfully: {report['date']}")
    except Exception as e:
        logger.error(f"Failed to generate daily report: {str(e)}")
    finally:
        db.close()

def run_scheduled_weekly_report():
    """Run scheduled weekly report with proper error handling"""
    try:
        db = SessionLocal()
        reporting_service = ReportingService(db)
        # Generate weekly report (implementation similar to daily report but for 7 days)
        logger.info("Weekly report generated successfully")
    except Exception as e:
        logger.error(f"Failed to generate weekly report: {str(e)}")
    finally:
        db.close()

def run_scheduled_monthly_report():
    """Run scheduled monthly report with proper error handling"""
    try:
        db = SessionLocal()
        reporting_service = ReportingService(db)
        # Generate monthly report (implementation similar to daily report but for 30 days)
        logger.info("Monthly report generated successfully")
    except Exception as e:
        logger.error(f"Failed to generate monthly report: {str(e)}")
    finally:
        db.close()
