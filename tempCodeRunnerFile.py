import time, random, requests
API_URL = "http://127.0.0.1:8000/predict"

def gen():
    return {
        "avg_speed": round(random.uniform(20, 100),2),
        "acceleration_mean": round(random.uniform(0.5, 3.0),2),
        "acceleration_std": round(random.uniform(0.1, 1.5),2),
        "braking_events": random.randint(0,5),
        "rpm_mean": round(random.uniform(2000,8000),2),
        "gear_shifts": random.randint(5,40),
        "trip_duration": round(random.uniform(5,60),2),
        "idle_time": round(random.uniform(0,5),2),
        "mileage": round(random.uniform(20,50),2),
        "jerk_mean": round(random.uniform(0.2,2.0),2),
        "speed_var": round(random.uniform(2,12),2)
    }

if __name__=="__main__":
    while True:
        d = gen()
        try:
            r = requests.post(API_URL, json=d, timeout=5)
            print(r.json())
        except Exception as e:
            print("err:", e)
        time.sleep(2)
