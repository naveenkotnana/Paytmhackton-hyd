"""Merchant-growth opportunity scoring from live synthetic payments telemetry."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.payments import PaymentTransaction


def _money(value: Any) -> float:
    return float(Decimal(str(value or 0)).quantize(Decimal("0.01")))


def _hours_bucket(created_at: Optional[datetime]) -> str:
    if created_at is None:
        return "unknown"
    return created_at.strftime("%Y-%m-%d %H:00")


def calculate_opportunity_pulse(
    db: Session,
    *,
    merchant_id: Optional[str] = None,
    days_back: int = 7,
) -> Dict[str, Any]:
    """Return a merchant opportunity summary derived from stored payment data.

    The result stays grounded in the current DB state and intentionally labels the
    values as synthetic demo data for the prototype experience.
    """
    cutoff = datetime.utcnow() - timedelta(days=days_back)
    query = db.query(PaymentTransaction).filter(PaymentTransaction.created_at >= cutoff)
    if merchant_id:
        query = query.filter(PaymentTransaction.merchant_id == merchant_id)

    txns = query.all()
    if not txns:
        return {
            "top_method": "UPI",
            "top_bank": "ICICI",
            "failure_rate_pct": 0.0,
            "affected_txns": 0,
            "peak_window": "No recent failures",
            "recommended_action": "No merchant recovery action needed for the selected window.",
            "recoverable_amount_inr": 0.0,
            "synthetic_demo_data": True,
        }

    failure_groups: Dict[Tuple[str, str], Dict[str, Any]] = defaultdict(
        lambda: {"method": "", "bank": "", "attempts": 0, "failed": 0, "amount": Decimal("0.00")}
    )
    hourly_groups: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "failed": 0})

    for txn in txns:
        method = txn.method or "UNKNOWN"
        bank = txn.bank or "UNKNOWN"
        key = (method, bank)
        failure_groups[key]["method"] = method
        failure_groups[key]["bank"] = bank
        failure_groups[key]["attempts"] += 1
        if txn.status == "FAILED":
            failure_groups[key]["failed"] += 1
            failure_groups[key]["amount"] += Decimal(str(txn.amount or 0))

        hour_key = _hours_bucket(txn.created_at)
        hourly_groups[hour_key]["total"] += 1
        if txn.status == "FAILED":
            hourly_groups[hour_key]["failed"] += 1

    if failure_groups:
        top_group = max(
            failure_groups.values(),
            key=lambda item: (item["failed"] / item["attempts"], item["failed"], item["amount"]),
        )
        top_method = top_group["method"]
        top_bank = top_group["bank"]
        failed_count = int(top_group["failed"])
        attempts = int(top_group["attempts"])
        failure_rate = (failed_count / attempts * 100.0) if attempts else 0.0
        recoverable = _money(top_group["amount"])
        peak_window = "No recent failures"
        if hourly_groups:
            peak_hour = max(hourly_groups.items(), key=lambda item: item[1]["failed"] or item[1]["total"])
            peak_window = peak_hour[0]

        recommended_action = (
            f"Route {top_method} retries through a healthy {top_bank} or alternate gateway, "
            f"and notify the merchant to retry affected orders before the next settlement window."
        )
        return {
            "top_method": top_method,
            "top_bank": top_bank,
            "failure_rate_pct": round(failure_rate, 2),
            "affected_txns": failed_count,
            "peak_window": peak_window,
            "recommended_action": recommended_action,
            "recoverable_amount_inr": recoverable,
            "synthetic_demo_data": True,
        }

    peak_window = max(hourly_groups.items(), key=lambda item: item[1]["total"], default=("No recent activity", {"total": 0}))[0]
    return {
        "top_method": "UPI",
        "top_bank": "ICICI",
        "failure_rate_pct": 0.0,
        "affected_txns": 0,
        "peak_window": peak_window,
        "recommended_action": "No action needed in the selected payment window.",
        "recoverable_amount_inr": 0.0,
        "synthetic_demo_data": True,
    }
