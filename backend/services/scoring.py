def calculate_score(signals):
    score = 0

    qa = signals.get("qa")
    if qa and qa.get("value"):
        score += 2
        score += min(len(qa.get("keywords", [])), 2)

    hiring = signals.get("hiring")
    if hiring and hiring.get("value"):
        if hiring.get("count", 0) > 5:
            score += 3
        else:
            score += 2

    saas = signals.get("saas")
    if saas and saas.get("value"):
        score += 1
        if saas.get("strength", 0) > 3:
            score += 1

    tech = signals.get("tech")
    if tech and tech.get("count", 0) > 0:
        score += 1

    negative = signals.get("negative")
    if negative and negative.get("value"):
        score -= 2

    if signals.get("website_health"):
        score += signals["website_health"]

    if score >= 9:
        category = "Hot"
    elif score >= 6:
        category = "Good"
    elif score >= 3:
        category = "Average"
    else:
        category = "Bad"

    return score, category