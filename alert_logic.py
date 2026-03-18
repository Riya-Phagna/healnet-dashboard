# =====================================================
# ALERT + RISK ENGINE (FINAL VERSION)
# =====================================================

def calculate_risk(heart_rate, spo2, sleep_hours, steps):
    """
    Returns:
        alert_level (str)
        alert_message (str)
    """

    # ---------- CRITICAL ----------
    if heart_rate > 120 or spo2 < 90 or sleep_hours < 4:
        return "CRITICAL", "🚨 Critical health risk detected."

    # ---------- WARNING ----------
    elif heart_rate > 95 or spo2 < 94 or sleep_hours < 5 or steps < 2000:
        return "WARNING", "⚠️ Moderate health risk detected."

    # ---------- NORMAL ----------
    else:
        return "NORMAL", "✅ Patient vitals stable."


# =====================================================
# TREND BASED ALERTS
# =====================================================

def trend_based_alert(df):

    alerts = []

    if len(df) < 5:
        return alerts

    last = df.tail(5)

    if "risk_score" in last.columns:
        if last["risk_score"].mean() > 70:
            alerts.append(("CRITICAL", "Risk increasing continuously"))

    if "spo2" in last.columns:
        if last["spo2"].mean() < 92:
            alerts.append(("WARNING", "Oxygen level dropping trend"))

    if "heart_rate" in last.columns:
        if last["heart_rate"].mean() > 110:
            alerts.append(("WARNING", "Heart rate continuously high"))

    return alerts