from fastapi import APIRouter, HTTPException
from db.sheets import sheet

router = APIRouter()


# GET SHEET
@router.get("/get-sheet")
def get_sheet():
    return sheet.get_all_records()


# UPDATE CELL
@router.post("/update-cell")
def update_cell(data: dict):
    row = data.get("row")
    col = data.get("col")
    value = data.get("value", "")

    if row is None or col is None:
        raise HTTPException(status_code=400, detail="Missing row or col value")

    try:
        row = int(row)
        col = int(col)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="row and col must be integers")

    sheet.update_cell(row, col, value)

    return {"status": "updated"}