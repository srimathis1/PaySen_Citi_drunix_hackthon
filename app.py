import streamlit as st
from services.risk_engine import calculate_risk
from services.fx_engine import estimate_remittance

st.set_page_config(page_title="PaySathi", page_icon="🛡️", layout="wide")

st.title("🛡️ PaySathi")
st.subheader("Context-aware payment safety for India's real-time payments")
st.caption("Hackathon MVP • Mock payment layer • Designed for future NPCI API integration")

with st.sidebar:
    st.header("Demo User")
    user_name = st.text_input("Name", "Srimathi")
    st.success("Trusted Circle: 4 contacts")
    st.info("PaySathi does not replace a bank or NPCI. This prototype demonstrates the decision layer that can sit before a payment request.")

tab1, tab2, tab3 = st.tabs(["💸 Payment Safety", "🌍 Cross-Border", "🧠 How It Works"])

with tab1:
    st.markdown("### Check a payment before it is sent")

    c1, c2 = st.columns(2)
    with c1:
        recipient = st.text_input("Recipient", "newshop@upi")
        amount = st.number_input("Amount (₹)", min_value=1, value=8500, step=500)
        purpose = st.selectbox(
            "Payment purpose",
            ["Shopping", "Rent", "Education", "Medical", "Family", "Investment", "Other"]
        )
        new_recipient = st.checkbox("This is a new recipient", value=True)

    with c2:
        recent_count = st.slider("Payments to this recipient in the last 24h", 0, 10, 0)
        unusual_time = st.checkbox("Payment is being made at an unusual time", value=False)
        user_stated = st.text_input(
            "What are you paying for?",
            "Buying a laptop"
        )
        expected_recipient_type = st.selectbox(
            "Expected recipient type",
            ["Merchant", "Person", "Landlord", "College", "Hospital", "Investment platform"]
        )

    if st.button("🔍 Analyze Payment", type="primary"):
        result = calculate_risk(
            amount=amount,
            new_recipient=new_recipient,
            recent_count=recent_count,
            unusual_time=unusual_time,
            purpose=purpose,
            stated_intent=user_stated,
            recipient_type=expected_recipient_type,
        )

        st.divider()
        a, b, c = st.columns(3)
        a.metric("Risk Score", f"{result['score']}/100")
        b.metric("Decision", result["decision"])
        c.metric("Trust Level", result["trust"])

        if result["decision"] == "ALLOW":
            st.success("✅ Payment can proceed.")
        elif result["decision"] == "VERIFY":
            st.warning("⚠️ Verify the recipient before continuing.")
        else:
            st.error("🛑 High-risk payment. PaySathi recommends a safety pause.")

        st.markdown("### Why?")
        for reason in result["reasons"]:
            st.write("•", reason)

        st.markdown("### Human-readable confirmation")
        st.info(
            f"You are about to send ₹{amount:,.0f} to **{recipient}**. "
            f"Purpose: **{purpose}**. "
            f"PaySathi classified this payment as **{result['decision']}**."
        )

        st.caption(
            "Prototype behavior: a real deployment would pass the final transaction "
            "through the bank/UPI payment flow after user authorization."
        )

with tab2:
    st.markdown("### 🌍 Transparent cross-border remittance estimate")
    st.write("A companion module shows how the same safety layer can explain cross-border costs.")

    c1, c2 = st.columns(2)
    with c1:
        inr = st.number_input("Amount in INR", min_value=100, value=50000, step=1000)
        corridor = st.selectbox("Destination", ["USD — United States", "AED — UAE", "SGD — Singapore", "GBP — United Kingdom"])
    with c2:
        fx_rate = st.number_input("Reference FX rate", min_value=0.01, value=0.0119, format="%.4f")
        fee_pct = st.slider("Estimated total fee (%)", 0.0, 5.0, 1.2, 0.1)

    if st.button("Calculate transparent quote"):
        quote = estimate_remittance(inr, fx_rate, fee_pct)
        st.metric("Recipient receives (reference estimate)", f"{quote['received']:,.2f}")
        st.write(f"**Fee:** ₹{quote['fee']:,.2f}")
        st.write(f"**Effective rate after fee:** {quote['effective_rate']:.6f}")
        st.caption("For demonstration only. Live FX, compliance checks and settlement rails would be supplied by regulated partners.")

with tab3:
    st.markdown("### 🧠 PaySathi architecture")
    st.code("""
User
  │
  ▼
Payment Intent
  │
  ├── Recipient Trust Graph
  ├── Amount / Velocity Signals
  ├── Time & Behaviour Signals
  └── Stated Payment Intent
          │
          ▼
   Explainable Risk Engine
          │
     ┌────┼─────┐
     ▼    ▼     ▼
   ALLOW VERIFY PAUSE
          │
          ▼
 Bank / UPI / NPCI Payment Rail
    (integration point)
    """, language="text")

    st.markdown("### What makes the MVP different?")
    points = [
        "It evaluates the payment context, not only a transaction amount.",
        "It explains the reason for a warning in plain language.",
        "It treats a new recipient as a context signal instead of automatically blocking the user.",
        "The same decision layer can be adapted to UPI, remittance and other payment rails.",
        "The prototype is API-ready: the mock transaction object can later be replaced by an authorized NPCI/bank API response."
    ]
    for p in points:
        st.write("•", p)

st.divider()
st.caption("PaySathi — prototype for DRUNIX Hackathon 2026 | Not a banking service")
