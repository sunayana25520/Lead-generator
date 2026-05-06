import asyncio

from services.scraper import scrape_website
from services.signals import detect_signals
from services.scoring import calculate_score


WEBSITE = "https://trykintsugi.com"


async def main():

    print("\n========================")
    print("START DEBUG")
    print("========================\n")

    result = await scrape_website(WEBSITE)

    text = result.get("text", "")
    tech = result.get("tech", {})

    print("\n========================")
    print("VISIBLE TEXT")
    print("========================\n")

    print(text[:3000])

    print("\n========================")
    print("TECH")
    print("========================\n")

    print(tech)

    signals = detect_signals(text)

    print("\n========================")
    print("SIGNALS")
    print("========================\n")

    print(signals)

    score, category = calculate_score(signals)

    print("\n========================")
    print("SCORE")
    print("========================\n")

    print("Score:", score)
    print("Category:", category)

    print("\n========================")
    print("END DEBUG")
    print("========================\n")


asyncio.run(main())