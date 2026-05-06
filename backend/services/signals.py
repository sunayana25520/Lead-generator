import re


def detect_signals(text: str):

    if not text or len(text) < 50:
        return {
            "qa": False,
            "hiring": False,
            "saas": False,
            "website_health": 0
        }

    text = text.lower()

    # -------------------------
    # QA (STRICT)
    # -------------------------
    qa_patterns = [

        r"\bqa engineer\b",
        r"\bquality assurance\b",
        r"\bquality engineering\b",

        r"\btest automation\b",
        r"\bautomation testing\b",
        r"\bsoftware testing\b",

        r"\bend[- ]to[- ]end testing\b",

        r"\bsdet\b"
    ]

    # -------------------------
    # HIRING
    # -------------------------
    hiring_patterns = [

        r"\bwe are hiring\b",
        r"\bwe're hiring\b",

        r"\bjoin our team\b",

        r"\bopen positions\b",
        r"\bopen roles\b",

        r"\bapply now\b",

        r"\bcareers\b"
    ]

    # -------------------------
    # SAAS
    # -------------------------
    saas_patterns = [

        r"\bplatform\b",
        r"\bsoftware\b",
        r"\bsaas\b",

        r"\bapi\b",

        r"\bdashboard\b",

        r"\banalytics\b",

        r"\bcloud\b",

        r"\bautomation\b",

        r"\bintegration\b",

        r"\bworkflow\b"
    ]

    # -------------------------
    # APPLY DETECTION
    # -------------------------
    qa = any(
        re.search(p, text)
        for p in qa_patterns
    )

    hiring = any(
        re.search(p, text)
        for p in hiring_patterns
    )

    saas_hits = sum(
        len(re.findall(p, text))
        for p in saas_patterns
    )

    saas = saas_hits >= 1

    # -------------------------
    # HEALTH
    # -------------------------
    word_count = len(text.split())

    if word_count > 4000:
        health = 2

    elif word_count > 1000:
        health = 1

    else:
        health = 0

    return {
        "qa": qa,
        "hiring": hiring,
        "saas": saas,
        "website_health": health
    }