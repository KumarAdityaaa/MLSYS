import json
import os
from datetime import datetime

FILE = "experiments.json"

def save_experiment(name, metrics):
    experiment = {
        "name": name,
        "metrics": metrics,
        "timestamp": str(datetime.now())
    }

    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append(experiment)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

    return experiment


def get_experiments():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)