from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router as analyze_router
from routes.upload import router as upload_router
from routes.results import router as results_router
from routes.sheet import router as sheet_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(results_router)
app.include_router(sheet_router)


@app.get("/")
def home():
    return {"message": "Server Working"}