import asyncio
from playwright.async_api import async_playwright

# ✅ 5 browsers parallel
semaphore = asyncio.Semaphore(5)


# -------------------------
# FULL PAGE SCROLL
# -------------------------
async def auto_scroll(page):

    previous_height = 0
    stable_count = 0
    max_scrolls = 30

    for _ in range(max_scrolls):

        # scroll down
        await page.mouse.wheel(0, 1200)

        # faster wait
        await page.wait_for_timeout(700)

        current_height = await page.evaluate(
            "() => document.body.scrollHeight"
        )

        print(f"[SCROLL HEIGHT] {current_height}px")

        # allow tiny fluctuations
        difference = abs(
            current_height - previous_height
        )

        if difference < 50:
            stable_count += 1
        else:
            stable_count = 0

        # stop if stable enough
        if stable_count >= 3:
            break

        previous_height = current_height

    print("[SCROLL FINISHED]")


# -------------------------
# EXTRACT ONLY VISIBLE UI TEXT
# -------------------------
async def extract_visible_text(page):

    text = await page.evaluate(
        """
        () => {

            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                {
                    acceptNode(node) {

                        const value = node.nodeValue.trim();

                        if (!value)
                            return NodeFilter.FILTER_REJECT;

                        const parent = node.parentElement;

                        if (!parent)
                            return NodeFilter.FILTER_REJECT;

                        const style =
                            window.getComputedStyle(parent);

                        if (
                            style.display === 'none' ||
                            style.visibility === 'hidden' ||
                            style.opacity === '0'
                        ) {
                            return NodeFilter.FILTER_REJECT;
                        }

                        const rect =
                            parent.getBoundingClientRect();

                        if (
                            rect.width === 0 ||
                            rect.height === 0
                        ) {
                            return NodeFilter.FILTER_REJECT;
                        }

                        return NodeFilter.FILTER_ACCEPT;
                    }
                }
            );

            const parts = [];

            while (walker.nextNode()) {

                parts.push(
                    walker.currentNode.nodeValue.trim()
                );
            }

            return parts.join(' ');
        }
        """
    )

    return " ".join(text.split())


# -------------------------
# TECH DETECTION
# -------------------------
async def detect_tech_playwright(page, requests):

    tech = {
        "frontend": set(),
        "backend": set(),
        "cms": set()
    }

    content = (await page.content()).lower()

    # Frontend
    if (
        "react" in content or
        "_reactroot" in content or
        "data-reactroot" in content
    ):
        tech["frontend"].add("React")

    if (
        "angular" in content or
        "ng-version" in content or
        "ng-app" in content
    ):
        tech["frontend"].add("Angular")

    if (
        "vue" in content or
        "__vue__" in content or
        "vue-router" in content
    ):
        tech["frontend"].add("Vue")

    # CMS
    if (
        "wp-content" in content or
        "wordpress" in content or
        "wp-json" in content
    ):
        tech["cms"].add("WordPress")

    if (
        "cdn.shopify.com" in content or
        "myshopify" in content
    ):
        tech["cms"].add("Shopify")

    # Script sources
    scripts = await page.eval_on_selector_all(
        "script",
        "els => els.map(e => e.src || '').filter(Boolean)"
    )

    for src in scripts:

        src = src.lower()

        if "react" in src:
            tech["frontend"].add("React")

        if "angular" in src:
            tech["frontend"].add("Angular")

        if "vue" in src:
            tech["frontend"].add("Vue")

        if "cdn.shopify.com" in src:
            tech["cms"].add("Shopify")

    # Network requests
    for url in requests:

        if (
            "api." in url or
            "/api/" in url or
            "/graphql" in url or
            "wp-json" in url
        ):
            tech["backend"].add("API Detected")

        if "amazonaws" in url:
            tech["backend"].add("AWS")

        if "firebase" in url:
            tech["backend"].add("Firebase")

    for key in tech:
        tech[key] = sorted(tech[key])

    return tech


# -------------------------
# MAIN SCRAPER
# -------------------------
async def scrape_website(url: str):

    async with semaphore:

        try:

            async with async_playwright() as p:

                browser = await p.chromium.launch(
                    headless=False,
                    slow_mo=100
                )

                context = await browser.new_context(
                    viewport={
                        "width": 1400,
                        "height": 900
                    }
                )

                page = await context.new_page()

                requests = []

                page.on(
                    "request",
                    lambda req:
                    requests.append(req.url.lower())
                )

                print("\n================================")
                print(f"[OPENING] {url}")
                print("================================\n")

                # ✅ FIXED LOAD
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                print("[PAGE LOADED]")

                await page.wait_for_selector(
                    "body",
                    timeout=15000
                )

                # allow React/Vue rendering
                await page.wait_for_timeout(3000)

                print("[STARTING FULL PAGE SCROLL]\n")

                # full homepage scroll
                await auto_scroll(page)

                # small wait after scroll
                await page.wait_for_timeout(1500)

                print("\n[EXTRACTING VISIBLE UI TEXT]\n")

                # visible UI text only
                text = await extract_visible_text(page)

                # word count
                word_count = len(text.split())

                print(f"[WORD COUNT] {word_count}")

                # tech detection
                tech = await detect_tech_playwright(
                    page,
                    requests
                )

                print(f"[TECH DETECTED] {tech}")

                await browser.close()

                return {
                    "text": text,
                    "tech": tech
                }

        except Exception as e:

            print("\nSCRAPE ERROR:", url)
            print(e)

            return {
                "text": "",
                "tech": {
                    "frontend": [],
                    "backend": [],
                    "cms": []
                }
            }


# -------------------------
# PROCESS ONE COMPANY
# -------------------------
async def process_company(company_data):

    company = (
        company_data.get("company")
        or company_data.get("Company Name")
    )

    website = (
        company_data.get("website")
        or company_data.get("Company Website")
    )

    if not website:

        return {
            "company": company,
            "website": None,
            "text": "",
            "tech": {
                "frontend": [],
                "backend": [],
                "cms": []
            }
        }

    result = await scrape_website(website)

    return {
        "company": company,
        "website": website,
        "text": result.get("text", ""),
        "tech": result.get("tech", {
            "frontend": [],
            "backend": [],
            "cms": []
        })
    }


# -------------------------
# SCRAPE ALL
# -------------------------
async def scrape_all(data: list):

    tasks = [
        process_company(item)
        for item in data
    ]

    results = await asyncio.gather(*tasks)

    return results