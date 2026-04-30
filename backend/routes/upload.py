from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    filename = (file.filename or "").lower()
    allowed_types = {"text/csv", "application/vnd.ms-excel", "text/plain"}
    if not filename.endswith(".csv") and file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to parse uploaded CSV file.")

    df = df.drop_duplicates()

    cleaned = []

    for _, row in df.iterrows():
        cleaned.append({
            "company": row.get("Company Name") or row.get("company"),
            "website": row.get("Website") or row.get("website")
        })

    return {"data": cleaned}