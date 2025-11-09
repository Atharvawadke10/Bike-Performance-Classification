
import joblib, pandas as pd, numpy as np
_model = joblib.load("bike_behavior_model.pkl")

def predict_behavior(features: dict):
    df = pd.DataFrame([features])
    pred = _model.predict(df)[0]
    proba = _model.predict_proba(df).max()
    return {"behavior": pred, "confidence": float(proba)}