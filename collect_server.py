from fastapi import FastAPI
from pydantic import BaseModel
import csv, os, datetime

app = FastAPI()
CSVFILE = "collected_telemetry.csv"
fields = ["timestamp","bike_id","avg_speed","acceleration_mean","acceleration_std","braking_events","rpm_mean","gear_shifts","trip_duration","idle_time","mileage","jerk_mean","speed_var"]

class Telemetry(BaseModel):
    bike_id: str
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

@app.post("/log")
def log(t: Telemetry):
    row = [datetime.datetime.utcnow().isoformat(), t.bike_id, t.avg_speed, t.acceleration_mean, t.acceleration_std, t.braking_events, t.rpm_mean, t.gear_shifts, t.trip_duration, t.idle_time, t.mileage, t.jerk_mean, t.speed_var]
    file_exists = os.path.exists(CSVFILE)
    with open(CSVFILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(row)
    return {"status":"ok"}
