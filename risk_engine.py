import random

def calculate_risk(heart_rate, spo2, sleep):

    score = 0

    if heart_rate > 110 or heart_rate < 50:
        score += 30

    if spo2 < 94:
        score += 40

    if sleep < 5:
        score += 30

    if score < 30:
        status = "Normal"
    elif score < 70:
        status = "Mild Risk"
    else:
        status = "High Risk"

    return score, status