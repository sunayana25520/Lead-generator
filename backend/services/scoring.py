def calculate_score(signals, tech=None):

    score = 0

    if signals.get("qa"):
        score += 2

    if signals.get("hiring"):
        score += 2

    if signals.get("saas"):
        score += 1

    score += signals.get("website_health", 0)

    # ✅ YOUR CATEGORY RULE
    if score >= 5:
        category = "High"
    elif score >= 2:
        category = "Medium"
    else:
        category = "Low"

    return score, category