from fastapi import FastAPI
from pydantic import BaseModel
from model_utils import predict_behavior

class BikeData(BaseModel):
    avg_speed: float
    acceleration_mean: float
    acceleration_std: float
    braking_events: int
    rpm_mean: float
    gear_shifts: int
    trip_duration: float
    idle_time: float
    mileage: float
    jerk_mean: float
    speed_var: float

app = FastAPI()

@app.post("/predict")
def predict(data: BikeData):
    return {"prediction": predict_behavior(data.dict())}
