from fastapi import APIRouter

router = APIRouter()

@router.get("/results")
def get_results():
    return {"message": "Check Google Sheets"}