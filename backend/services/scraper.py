import asyncio
from playwright.async_api import async_playwright

from services.signals import detect_signals
from services.validator import normalize_signals
from services.scoring import calculate_score
from services.personalize import build_output


async def scrape_website(url):
    text = ""

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # browser = await p.chromium.launch(headless=False, slow_mo=500)
            page = await browser.new_page()

            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)

            text += await page.inner_text("body")

            for path in ["/careers", "/jobs", "/about"]:
                try:
                    await page.goto(url.rstrip("/") + path, timeout=20000)
                    await page.wait_for_timeout(2000)
                    text += "\n" + await page.inner_text("body")
                except:
                    pass

            await browser.close()

    except Exception as e:
        print("ERROR:", e)

    return text


async def process_company(company_data):
    company = company_data["company"]
    website = company_data["website"]

    text = await scrape_website(website)

    signals = normalize_signals(detect_signals(text))
    score, category = calculate_score(signals)

    return build_output(company, website, signals, score, category)


async def scrape_all(data):
    tasks = [process_company(d) for d in data]
    return await asyncio.gather(*tasks)