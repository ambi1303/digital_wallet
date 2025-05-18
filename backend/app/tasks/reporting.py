from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction, TransactionStatus
from app.models.wallet import Wallet
from app.models.user import User
from app.utils.email import send_email_alert
import logging

logger = logging.getLogger(__name__)

class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    def generate_daily_report(self) -> dict:
        """Generate daily transaction report"""
        yesterday = datetime.utcnow() - timedelta(days=1)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Get transaction statistics
        transaction_stats = self._get_transaction_stats(yesterday_start, yesterday_end)
        
        # Get flagged transactions
        flagged_transactions = self._get_flagged_transactions(yesterday_start, yesterday_end)
        
        # Get top users by transaction volume
        top_users = self._get_top_users(yesterday_start, yesterday_end)
        
        # Get currency distribution
        currency_stats = self._get_currency_stats(yesterday_start, yesterday_end)

        report = {
            "date": yesterday.date().isoformat(),
            "transaction_stats": transaction_stats,
            "flagged_transactions": flagged_transactions,
            "top_users": top_users,
            "currency_stats": currency_stats
        }

        # Send report to admin
        self._send_admin_report(report)

        return report

    def _get_transaction_stats(self, start_date: datetime, end_date: datetime) -> dict:
        """Get transaction statistics for the period"""
        transactions = self.db.query(Transaction).filter(
            Transaction.created_at.between(start_date, end_date)
        ).all()

        total_amount = sum(t.amount for t in transactions)
        total_count = len(transactions)
        avg_amount = total_amount / total_count if total_count > 0 else 0

        return {
            "total_transactions": total_count,
            "total_amount": total_amount,
            "average_amount": avg_amount,
            "transaction_types": {
                "deposit": len([t for t in transactions if t.transaction_type == "DEPOSIT"]),
                "withdrawal": len([t for t in transactions if t.transaction_type == "WITHDRAWAL"]),
                "transfer": len([t for t in transactions if t.transaction_type == "TRANSFER"])
            }
        }

    def _get_flagged_transactions(self, start_date: datetime, end_date: datetime) -> list:
        """Get flagged transactions for the period"""
        return self.db.query(Transaction).filter(
            Transaction.created_at.between(start_date, end_date),
            Transaction.is_flagged == True
        ).all()

    def _get_top_users(self, start_date: datetime, end_date: datetime, limit: int = 10) -> list:
        """Get top users by transaction volume"""
        return self.db.query(
            User,
            func.sum(Transaction.amount).label('total_volume')
        ).join(Transaction).filter(
            Transaction.created_at.between(start_date, end_date)
        ).group_by(User.id).order_by(
            func.sum(Transaction.amount).desc()
        ).limit(limit).all()

    def _get_currency_stats(self, start_date: datetime, end_date: datetime) -> dict:
        """Get currency distribution statistics"""
        currency_stats = {}
        transactions = self.db.query(Transaction).filter(
            Transaction.created_at.between(start_date, end_date)
        ).all()

        for transaction in transactions:
            currency = transaction.currency
            if currency not in currency_stats:
                currency_stats[currency] = {
                    "count": 0,
                    "total_amount": 0
                }
            currency_stats[currency]["count"] += 1
            currency_stats[currency]["total_amount"] += transaction.amount

        return currency_stats

    def _send_admin_report(self, report: dict) -> None:
        """Send daily report to admin"""
        try:
            # Format report for email
            email_body = self._format_report_email(report)
            
            # Get admin email
            admin = self.db.query(User).filter(User.is_admin == True).first()
            if admin:
                send_email_alert(
                    to_email=admin.email,
                    subject=f"Daily Transaction Report - {report['date']}",
                    body=email_body
                )
        except Exception as e:
            logger.error(f"Failed to send admin report: {str(e)}")

    def _format_report_email(self, report: dict) -> str:
        """Format report data for email"""
        return f"""
Daily Transaction Report - {report['date']}

Transaction Statistics:
- Total Transactions: {report['transaction_stats']['total_transactions']}
- Total Amount: {report['transaction_stats']['total_amount']}
- Average Amount: {report['transaction_stats']['average_amount']}

Transaction Types:
- Deposits: {report['transaction_stats']['transaction_types']['deposit']}
- Withdrawals: {report['transaction_stats']['transaction_types']['withdrawal']}
- Transfers: {report['transaction_stats']['transaction_types']['transfer']}

Flagged Transactions: {len(report['flagged_transactions'])}

Top Users by Volume:
{self._format_top_users(report['top_users'])}

Currency Distribution:
{self._format_currency_stats(report['currency_stats'])}
"""

    def _format_top_users(self, top_users: list) -> str:
        """Format top users for email"""
        return "\n".join([
            f"- {user.username}: {volume} {user.wallet.currency.value}"
            for user, volume in top_users
        ])

    def _format_currency_stats(self, currency_stats: dict) -> str:
        """Format currency statistics for email"""
        return "\n".join([
            f"- {currency}: {stats['count']} transactions, {stats['total_amount']} total"
            for currency, stats in currency_stats.items()
        ]) 