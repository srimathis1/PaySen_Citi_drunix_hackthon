# 🛡️ PaySathi

**Context-aware payment safety for India's real-time payment ecosystem.**

PaySathi is a hackathon MVP for the DRUNIX fintech challenge. It adds an explainable decision layer before a payment is authorized.

## Problem

Real-time payments are fast, but speed can also reduce the time a user has to notice:
- a first-time recipient
- an unusually large payment
- repeated transfers
- a suspicious payment time
- a mismatch between the stated purpose and recipient type

## Solution

PaySathi calculates an explainable risk score and returns:

- 🟢 ALLOW
- 🟡 VERIFY
- 🔴 PAUSE

The prototype also contains a cross-border remittance transparency module.

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit.

## Demo flow

1. Enter a new recipient.
2. Enter a large amount.
3. Select a payment purpose.
4. Increase recent payment count.
5. Click **Analyze Payment**.
6. Show how the decision changes from ALLOW → VERIFY → PAUSE.

## Production integration

The current payment layer is intentionally mocked.

Potential production architecture:

User App → PaySathi Risk API → authorized bank/UPI/NPCI integration → payment authorization.

Actual NPCI APIs, credentials, sandbox rules, KYC/AML controls and regulated payment partners would be required for a live deployment.

## Tech stack

- Python
- Streamlit
- Explainable rule-based risk engine
- Cross-border FX estimation module

## Team pitch

**Tagline:** "Don't slow every payment. Slow the risky ones."

**Track:** Real-Time Payments + Financial Inclusion / AI & Fraud Detection

## Disclaimer

This is a hackathon prototype, not a banking or payment service.
