def detect_tech_stack(text):
    text = text.lower()
    stack = []

    tech_map = {
        "React": ["react"],
        "Angular": ["angular"],
        "Vue": ["vue"],
        "Node.js": ["node", "nodejs"],
        "Python": ["python", "django", "flask"],
        "AWS": ["aws", "amazon web services"],
        "Shopify": ["shopify"],
        "WordPress": ["wordpress"]
    }

    for tech, keywords in tech_map.items():
        if any(k in text for k in keywords):
            stack.append(tech)

    return list(set(stack))