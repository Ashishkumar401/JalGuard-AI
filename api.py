from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "jalguard_cyberattack_model.joblib"

artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
features = artifact["features"]

app = FastAPI(
    title="JalGuard AI API",
    description="Experimental water-network sensor event detection",
    version="0.1.0",
)


class SensorReading(BaseModel):
    readings: dict[str, float]


@app.get("/")
def home():
    return {
        "project": "JalGuard AI",
        "status": "running",
        "model_status": "experimental",
        "sensor_features": len(features),
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(payload: SensorReading):
    missing = [name for name in features if name not in payload.readings]
    extra = [name for name in payload.readings if name not in features]

    if missing or extra:
        raise HTTPException(
            status_code=422,
            detail={"missing_features": missing, "unexpected_features": extra},
        )

    row = pd.DataFrame(
        [[payload.readings[name] for name in features]],
        columns=features,
    )

    prediction = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    event_index = list(model.classes_).index(1)
    event_probability = float(probabilities[event_index])

    return {
        "predicted_label": prediction,
        "event_probability": round(event_probability, 4),
        "interpretation": (
            "Dataset label 1 predicted; investigate"
            if prediction == 1
            else "Dataset label 0 predicted"
        ),
        "model_status": "experimental",
        "warning": "Research-dataset prediction only; not validated for real water networks.",
    }
