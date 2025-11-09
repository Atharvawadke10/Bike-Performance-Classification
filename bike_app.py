import random
import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Bike Performance Dashboard", page_icon="🏍️", layout="wide")
st.title("🏍️ Bike Rider Behavior Classification")

api_url = "http://127.0.0.1:8000/predict"
placeholder = st.empty()

data_log = []

while True:
    # Simulate input
    features = {
        "avg_speed": round(random.uniform(20, 100), 2),
        "acceleration_mean": round(random.uniform(0.5, 3.0), 2),
        "acceleration_std": round(random.uniform(0.1, 1.5), 2),
        "braking_events": random.randint(0, 5),
        "rpm_mean": round(random.uniform(2000, 8000), 2),
        "gear_shifts": random.randint(5, 40),
        "trip_duration": round(random.uniform(5, 60), 2),
        "idle_time": round(random.uniform(0, 5), 2),
        "mileage": round(random.uniform(25, 50), 2),
        "jerk_mean": round(random.uniform(0.2, 2.0), 2),
        "speed_var": round(random.uniform(2, 10), 2)
    }

    res = requests.post(api_url, json=features).json()
    behavior = res['prediction']['behavior']
    conf = res['prediction']['confidence']

    data_log.append({**features, "behavior": behavior, "confidence": conf})

    df = pd.DataFrame(data_log[-20:])  # last 20 entries

    with placeholder.container():
        st.metric("Latest Prediction", behavior)
        st.progress(conf)
        st.line_chart(df[['avg_speed', 'rpm_mean', 'acceleration_mean']])
        st.dataframe(df)

    time.sleep(3)
