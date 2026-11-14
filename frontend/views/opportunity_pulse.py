"""Opportunity Pulse Streamlit view."""
from __future__ import annotations

import streamlit as st

from app.db.base import SessionLocal
from app.services.opportunity_pulse import calculate_opportunity_pulse


def render_opportunity_pulse(role: str = "ADMIN", merchant_id: str | None = None, page: str = "Opportunity Pulse") -> None:
    """Render a 3-card growth opportunity dashboard from actual stored telemetry."""
    del page
    target_merchant = merchant_id or st.session_state.get("merchant_id") or "mid_rameshwaram_01"
    with SessionLocal() as db:
        pulse = calculate_opportunity_pulse(
            db,
            merchant_id=target_merchant if role == "MERCHANT" else None,
            days_back=7,
        )

    st.header("Opportunity Pulse")
    st.caption("Synthetic demo data • live database-backed merchant-recovery insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1rem; min-height:220px;">
              <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; font-weight:800; color:#64748B;">Top failing flow</div>
              <div style="font-size:2rem; font-weight:800; margin-top:0.6rem; color:#0F172A;">{pulse['top_method']}</div>
              <div style="font-size:1rem; color:#475569; margin-top:0.2rem;">{pulse['top_bank']} bank</div>
              <div style="margin-top:1rem; font-size:0.88rem; color:#0F172A;">Failure rate: <strong>{pulse['failure_rate_pct']:.2f}%</strong></div>
              <div style="font-size:0.88rem; color:#475569;">Affected transactions: <strong>{pulse['affected_txns']}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1rem; min-height:220px;">
              <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; font-weight:800; color:#64748B;">Peak impacted window</div>
              <div style="font-size:1.8rem; font-weight:800; margin-top:0.6rem; color:#0F172A;">{pulse['peak_window']}</div>
              <div style="margin-top:1rem; font-size:0.88rem; color:#475569;">The highest concentration of failed traffic sits in this time band and needs intervention.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1rem; min-height:220px;">
              <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; font-weight:800; color:#64748B;">Recommended action</div>
              <div style="font-size:1rem; font-weight:700; margin-top:0.65rem; color:#0F172A;">Recoverable ₹ volume</div>
              <div style="font-size:2rem; font-weight:800; margin-top:0.2rem; color:#059669;">₹{pulse['recoverable_amount_inr']:,.2f}</div>
              <div style="margin-top:0.8rem; font-size:0.82rem; color:#334155;">{pulse['recommended_action']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin-top:1.25rem; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:0.85rem 1rem; color:#475569;">
          <strong>Demo label:</strong> This view is intentionally synthetic and uses the live payment database to estimate probable merchant recovery opportunities.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        [{
            "Payment method": pulse['top_method'],
            "Bank": pulse['top_bank'],
            "Failure rate %": pulse['failure_rate_pct'],
            "Affected txns": pulse['affected_txns'],
            "Peak window": pulse['peak_window'],
            "Recoverable ₹": pulse['recoverable_amount_inr'],
        }],
        use_container_width=True,
        hide_index=True,
    )
