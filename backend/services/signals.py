def detect_signals(text: str):
    if not text or len(text) < 100:
        return {
            "qa": None,
            "hiring": None,
            "saas": None,
            "tech": None,
            "negative": None,
            "website_health": None
        }

    text = text.lower()

    # 🔧 QA (slightly expanded)
    qa_keywords = [
        "qa engineer", "quality assurance", "test automation",
        "automation testing", "sdet", "software testing",
        "testing team", "test engineer"
    ]

    # 🚀 HIRING (IMPORTANT FIX)
    hiring_keywords = [
        "we're hiring", "we are hiring",
        "open positions", "join our team",
        "apply now", "careers", "jobs",
        "open roles", "work with us"
    ]

    # 🚀 SAAS (IMPORTANT FIX)
    saas_keywords = [
        "saas", "subscription", "api",
        "cloud", "platform", "dashboard",
        "pricing", "trial", "solutions",
        "product", "software"
    ]

    # 🔧 TECH (same, slightly safer)
    tech_keywords = [
        "react", "node", "python", "aws",
        "azure", "gcp", "docker", "kubernetes"
    ]

    # 🔍 DETECTION
    qa_found = [k for k in qa_keywords if k in text]
    hiring_found = [k for k in hiring_keywords if k in text]
    saas_found = [k for k in saas_keywords if k in text]
    tech_found = list(set([k for k in tech_keywords if k in text]))  # remove duplicates

    # 🌐 WEBSITE HEALTH
    word_count = len(text.split())

    if word_count > 4000:
        health = 2
    elif word_count > 1500:
        health = 1
    else:
        health = None

    return {
        "qa": {
            "value": True,
            "keywords": qa_found
        } if qa_found else None,

        "hiring": {
            "value": True,
            "count": len(hiring_found),
            "keywords": hiring_found
        } if hiring_found else None,

        "saas": {
            "value": True,
            "strength": len(saas_found),
            "keywords": saas_found
        } if len(saas_found) >= 2 else None,

        "tech": {
            "count": len(tech_found),
            "stack": tech_found
        } if tech_found else None,

        "negative": None,
        "website_health": health
    }