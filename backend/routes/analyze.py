# from fastapi import APIRouter, UploadFile, File
# import csv
# import io

# from services.scraper import scrape_all
# from services.signals import detect_signals
# from services.scoring import calculate_score
# from services.personalize import build_output

# router = APIRouter()


# @router.post("/analyze")
# async def analyze(file: UploadFile = File(...)):

#     content = await file.read()
#     csv_text = content.decode("utf-8")
#     reader = csv.DictReader(io.StringIO(csv_text))

#     data = list(reader)

#     scraped_data = await scrape_all(data)

#     results = []

#     for item in scraped_data:
#         company = item.get("company")
#         website = item.get("website")
#         text = item.get("text", "")
#         tech = item.get("tech", {
#             "frontend": [],
#             "backend": [],
#             "cms": []
#         })

#         signals = detect_signals(text)
#         score, category = calculate_score(signals)

#         output = build_output(company, website, signals, score, category, tech)
#         results.append(output)

#     return {"results": results, "total": len(results)}


from fastapi import APIRouter, UploadFile, File
import csv
import io

from services.scraper import scrape_all
from services.signals import detect_signals
from services.scoring import calculate_score
from services.personalize import build_output

# ✅ GOOGLE SHEETS
from db.sheets import clear_sheet, save_bulk_to_sheet

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # READ CSV
    content = await file.read()

    csv_text = content.decode("utf-8")

    reader = csv.DictReader(
        io.StringIO(csv_text)
    )

    data = list(reader)

    print("\n========================")
    print("STARTING SCRAPING")
    print("========================\n")

    # SCRAPE
    scraped_data = await scrape_all(data)

    results = []

    # ANALYZE
    for item in scraped_data:

        company = item.get("company")

        website = item.get("website")

        text = item.get("text", "")

        tech = item.get(
            "tech",
            {
                "frontend": [],
                "backend": [],
                "cms": []
            }
        )

        signals = detect_signals(text)

        score, category = calculate_score(
            signals
        )

        output = build_output(
            company,
            website,
            signals,
            score,
            category,
            tech
        )

        results.append(output)

    print("\n========================")
    print("UPDATING GOOGLE SHEET")
    print("========================\n")

    # CLEAR OLD DATA
    clear_sheet()

    # SAVE NEW DATA
    save_bulk_to_sheet(results)

    print("\n========================")
    print("ANALYSIS COMPLETE")
    print("========================\n")

    # RETURN SAME DATA TO UI
    return {
        "results": results,
        "total": len(results)
    }