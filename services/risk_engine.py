def calculate_risk(
    amount,
    new_recipient,
    recent_count,
    unusual_time,
    purpose,
    stated_intent,
    recipient_type,
):
    score = 0
    reasons = []

    if new_recipient:
        score += 25
        reasons.append("Recipient is new, so identity/trust confidence is lower.")

    if amount >= 25000:
        score += 25
        reasons.append("Large-value transaction increases the impact of an incorrect payment.")
    elif amount >= 10000:
        score += 12
        reasons.append("Amount is above the normal low-value payment range.")

    if recent_count >= 5:
        score += 25
        reasons.append("Multiple recent payments to the same recipient indicate unusual velocity.")
    elif recent_count >= 2:
        score += 10
        reasons.append("There have been multiple recent payments to this recipient.")

    if unusual_time:
        score += 10
        reasons.append("The transaction is being made at an unusual time.")

    # Simple intent mismatch demonstration.
    intent = stated_intent.lower()
    if purpose == "Investment" and any(x in intent for x in ["refund", "delivery", "shopping", "purchase"]):
        score += 20
        reasons.append("The selected purpose and stated payment intent appear inconsistent.")
    elif purpose == "Shopping" and recipient_type == "Investment platform":
        score += 25
        reasons.append("Recipient type does not match the selected shopping purpose.")

    score = min(score, 100)

    if score >= 65:
        decision = "PAUSE"
    elif score >= 35:
        decision = "VERIFY"
    else:
        decision = "ALLOW"

    if score < 25:
        trust = "High"
    elif score < 55:
        trust = "Medium"
    else:
        trust = "Low"

    if not reasons:
        reasons.append("No strong risk signals were detected in this demo.")

    return {
        "score": score,
        "decision": decision,
        "trust": trust,
        "reasons": reasons,
    }
