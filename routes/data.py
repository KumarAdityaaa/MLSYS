from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os

router = APIRouter()

DATA_PATH = "data.csv"

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    with open(DATA_PATH, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(DATA_PATH)

    return {
        "columns": df.columns.tolist(),
        "preview": df.head(5).to_dict(orient="records")
    }