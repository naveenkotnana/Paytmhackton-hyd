"""Unit tests for the opportunity pulse helper."""

from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.payments import Merchant, PaymentOrder, PaymentTransaction
from app.services.opportunity_pulse import calculate_opportunity_pulse


def _seed_demo_data(session):
    merchant = Merchant(
        merchant_id="mid_demo_pulse_01",
        name="Demo Pulse Merchant",
        email="demo@example.com",
        business_category="FOOD_DELIVERY",
        pricing_plan="STANDARD_MDR",
        risk_tier="MEDIUM",
        status="ACTIVE",
    )
    session.add(merchant)
    session.flush()

    for idx in range(8):
        order_id = f"order_op_{idx:02d}"
        amount = Decimal("250") + Decimal(idx * 15)
        session.add(
            PaymentOrder(
                order_id=order_id,
                merchant_id=merchant.merchant_id,
                customer_id="cust_demo_01",
                amount=amount,
                currency="INR",
                receipt=f"r{idx}",
                status="CREATED",
            )
        )
        status = "FAILED" if idx < 5 else "CAPTURED"
        method = "UPI" if idx % 2 == 0 else "CARD"
        bank = "ICICI" if idx in (0, 2, 4, 6) else "HDFC"
        session.add(
            PaymentTransaction(
                payment_id=f"pay_op_{idx:02d}",
                order_id=order_id,
                merchant_id=merchant.merchant_id,
                customer_id="cust_demo_01",
                amount=amount,
                currency="INR",
                method=method,
                bank=bank,
                gateway="PAYTM_DIRECT",
                status=status,
                net_amount=amount,
            )
        )
    session.commit()
    return merchant


def test_calculate_opportunity_pulse_uses_live_telemetry():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        merchant = _seed_demo_data(session)
        pulse = calculate_opportunity_pulse(session, merchant_id=merchant.merchant_id, days_back=30)

        assert pulse["synthetic_demo_data"] is True
        assert pulse["top_method"] in {"UPI", "CARD"}
        assert pulse["top_bank"] in {"ICICI", "HDFC"}
        assert pulse["affected_txns"] >= 2
        assert pulse["recoverable_amount_inr"] >= 0.0
        assert "Route" in pulse["recommended_action"]
    finally:
        session.close()
