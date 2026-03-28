from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

DATA_PATH = "data.csv"

@router.get("/eda")
def auto_eda():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(
            status_code=404,
            detail="No dataset found. Please upload a CSV file first using /upload-csv."
        )

    try:
        df = pd.read_csv(DATA_PATH)

        summary = {
            "columns": df.columns.tolist(),
            "shape": df.shape,
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "describe": df.describe().to_dict()
        }

        return summary

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyse dataset: {str(e)}"
        )