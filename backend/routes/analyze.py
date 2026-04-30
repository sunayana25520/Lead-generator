from fastapi import APIRouter, UploadFile, File
import csv
import io

from services.scraper import scrape_all
from db.sheets import clear_sheet, save_bulk_to_sheet

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    content = await file.read()

    # ✅ FIX encoding error
    decoded = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(decoded))

    data = []
    for row in reader:
        data.append({
            "company": row["company"],
            "website": row["website"]
        })

    # ✅ CLEAR FIRST
    clear_sheet()

    # PROCESS
    results = await scrape_all(data)

    # SAVE
    save_bulk_to_sheet(results)

    return {"results": results}