from fastapi import APIRouter
from pydantic import BaseModel
from experiments.tracker import save_experiment, get_experiments

router = APIRouter()

class Experiment(BaseModel):
    name: str
    metrics: dict


@router.post("/experiment")
def add_experiment(exp: Experiment):
    return save_experiment(exp.name, exp.metrics)


@router.get("/experiments")
def list_experiments():
    return get_experiments()