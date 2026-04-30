def build_output(company, website, signals, score, category):

    # ✅ YES / NO (instead of empty)
    hiring = "Yes" if signals.get("hiring") else "No"
    qa = "Yes" if signals.get("qa") else "No"

    # ✅ PRODUCT
    product = "SaaS" if signals.get("saas") else "Other"

    # ✅ PAIN + MESSAGE (ALWAYS FILLED)
    if signals.get("qa") and signals.get("hiring"):
        pain = "Scaling QA & testing team"
        line = "Saw you're hiring QA engineers—are you scaling testing efforts?"
    elif signals.get("hiring"):
        pain = "Hiring and team expansion"
        line = "Saw you're hiring—are you expanding your engineering team?"
    elif signals.get("qa"):
        pain = "Improving QA automation"
        line = "Noticed QA efforts—can help improve testing efficiency."
    else:
        pain = "General engineering improvements"
        line = "Would love to help improve your engineering workflows."

    # ✅ TECH STACK SAFE
    tech_stack = ", ".join(signals["tech"]["stack"]) if signals.get("tech") else "other"

    return {
        "Company Name": company,
        "Website": website,
        "Tech Stack": tech_stack,
        "Hiring Detected": hiring,
        "QA Signals": qa,
        "Product Type": product,
        "Pain Point": pain,
        "Personalization Line": line,
        "Lead Score": score,
        "Category": category
    }