import streamlit as st, pandas as pd, requests, time, random
st.set_page_config(layout="wide", page_title="Bike Perf Dashboard")
st.title("Bike Rider Behavior")

api_url = st.text_input("API URL", value="http://127.0.0.1:8000/predict")
start = st.button("Start")
stop = st.button("Stop")
placeholder = st.empty()
log = []

running = False
if start:
    running = True
if stop:
    running = False

if running or start:
    for i in range(200):
        features = {
            "avg_speed": round(random.uniform(20, 95),2),
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
        try:
            res = requests.post(api_url, json=features, timeout=3).json()
            pred = res['prediction']
        except Exception as e:
            pred = {"behavior":"error", "confidence":0.0}
        entry = {**features, **pred}
        log.append(entry)
        df = pd.DataFrame(log[-30:])
        with placeholder.container():
            st.metric("Latest", df.iloc[-1]['behavior'])
            st.write(df.tail(10))
            st.line_chart(df[["avg_speed","rpm_mean","acceleration_mean"]])
        time.sleep(1)
