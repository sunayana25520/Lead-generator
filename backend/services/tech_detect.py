# def detect_tech_stack(text):
#     text = text.lower()
#     stack = []

#     tech_map = {
#         "React": ["react"],
#         "Angular": ["angular"],
#         "Vue": ["vue"],
#         "Node.js": ["node", "nodejs"],
#         "Python": ["python", "django", "flask"],
#         "AWS": ["aws", "amazon web services"],
#         "Shopify": ["shopify"],
#         "WordPress": ["wordpress"]
#     }

#     for tech, keywords in tech_map.items():
#         if any(k in text for k in keywords):
#             stack.append(tech)

#     return list(set(stack))




async def detect_tech_playwright(page):
    tech = {
        "frontend": set(),
        "backend": set(),
        "cms": set(),
        "infra": set()   # CDN / hosting hints
    }

    # -------------------------
    # 1. HTML CONTENT
    # -------------------------
    content = (await page.content()).lower()

    # Frontend frameworks
    if "react" in content or "_reactroot" in content:
        tech["frontend"].add("React")

    if "ng-version" in content or "angular" in content:
        tech["frontend"].add("Angular")

    if "__vue__" in content or "vue" in content:
        tech["frontend"].add("Vue")

    if "__next" in content:
        tech["frontend"].add("Next.js")

    # CMS
    if "wp-content" in content:
        tech["cms"].add("WordPress")

    if "shopify" in content:
        tech["cms"].add("Shopify")

    # -------------------------
    # 2. SCRIPT SOURCES
    # -------------------------
    scripts = await page.eval_on_selector_all(
        "script",
        "els => els.map(e => e.src)"
    )

    for src in scripts:
        src = src.lower()

        # Frontend
        if "react" in src:
            tech["frontend"].add("React")

        if "vue" in src:
            tech["frontend"].add("Vue")

        if "angular" in src:
            tech["frontend"].add("Angular")

        # SaaS / tools (important for scoring)
        if "stripe" in src:
            tech["backend"].add("Stripe")

        if "intercom" in src:
            tech["backend"].add("Intercom")

        if "hubspot" in src:
            tech["backend"].add("HubSpot")

        if "segment" in src:
            tech["backend"].add("Segment")

        # CMS
        if "cdn.shopify.com" in src:
            tech["cms"].add("Shopify")

    # -------------------------
    # 3. GLOBAL JS VARIABLES
    # -------------------------
    try:
        if await page.evaluate("() => !!window.React"):
            tech["frontend"].add("React")
    except:
        pass

    try:
        if await page.evaluate("() => !!window.Vue"):
            tech["frontend"].add("Vue")
    except:
        pass

    # -------------------------
    # 4. NETWORK REQUESTS
    # -------------------------
    requests = []
    page.on("request", lambda req: requests.append(req.url.lower()))

    await page.reload()
    await page.wait_for_load_state("networkidle")

    for url in requests:

        # Backend / APIs
        if "api" in url:
            tech["backend"].add("API")

        if "amazonaws" in url:
            tech["backend"].add("AWS")

        if "firebase" in url:
            tech["backend"].add("Firebase")

        if "supabase" in url:
            tech["backend"].add("Supabase")

        # Infra / CDN
        if "cloudflare" in url:
            tech["infra"].add("Cloudflare")

        if "vercel" in url:
            tech["infra"].add("Vercel")

        if "netlify" in url:
            tech["infra"].add("Netlify")

    # -------------------------
    # FINAL CLEANUP
    # -------------------------
    return {k: list(v) for k, v in tech.items()}