def estimate_remittance(inr, fx_rate, fee_pct):
    fee = inr * fee_pct / 100
    net_inr = inr - fee
    received = net_inr * fx_rate
    effective_rate = received / inr
    return {
        "fee": fee,
        "net_inr": net_inr,
        "received": received,
        "effective_rate": effective_rate,
    }
