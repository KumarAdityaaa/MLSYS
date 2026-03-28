from fastapi import APIRouter
import pandas as pd

router = APIRouter()

DATA_PATH = "data.csv"

@router.get("/eda")
def auto_eda():
    df = pd.read_csv(DATA_PATH)

    summary = {
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "describe": df.describe().to_dict()
    }

    return summary