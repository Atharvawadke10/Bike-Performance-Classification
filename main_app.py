import random
import streamlit as st
import pandas as pd
import requests
import time

# -------------------- SETTINGS --------------------
st.set_page_config(page_title="🏍️ Bike Rider Behavior Dashboard", layout="wide")

API_URL = "http://127.0.0.1:8000/predict"
st.title("🏍️ Bike Rider Behavior Dashboard")
st.markdown("Monitor, simulate, and predict rider behavior in real time or via manual input.")

# -------------------- SIDEBAR MODE SELECTION --------------------
mode = st.sidebar.radio("Select Mode", ["🔴 Live Simulation", "🧾 Manual Input"])

# Shared placeholder for dashboard updates
placeholder = st.empty()


# -------------------- MODE 1: LIVE SIMULATION --------------------
if mode == "🔴 Live Simulation":
    st.sidebar.markdown("### ⚙️ Simulation Controls")
    run_sim = st.sidebar.checkbox("Start Live Simulation", value=False)
    delay = st.sidebar.slider("Update Interval (seconds)", 1, 10, 3)

    data_log = []

    if run_sim:
        st.subheader("📡 Real-Time Data Stream")
        st.markdown("Simulated live input data updating every few seconds...")

        while True:
            # Simulated input features
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

            try:
                res = requests.post(API_URL, json=features)
                res.raise_for_status()
                prediction = res.json()
                behavior = prediction["prediction"]["behavior"]
                conf = prediction["prediction"]["confidence"]
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
                break

            data_log.append({**features, "behavior": behavior, "confidence": conf})
            df = pd.DataFrame(data_log[-20:])  # show last 20 readings

            with placeholder.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Latest Behavior Prediction", behavior)
                    st.progress(conf)
                    st.metric("Confidence Level", f"{conf * 100:.1f}%")
                with col2:
                    st.line_chart(df[["avg_speed", "rpm_mean", "acceleration_mean"]])

                st.dataframe(df)

            time.sleep(delay)
    else:
        st.info("▶️ Enable **Start Live Simulation** from the sidebar to begin.")


# -------------------- MODE 2: MANUAL INPUT --------------------
elif mode == "🧾 Manual Input":
    st.subheader("🧍 Manual Data Entry")
    st.write("Enter test or real-world sensor values to get instant predictions.")

    with st.form("prediction_form"):
        avg_speed = st.number_input("Average Speed (km/h)", 0.0, 200.0, 60.0)
        acceleration_mean = st.number_input("Acceleration Mean (m/s²)", 0.0, 10.0, 1.5)
        acceleration_std = st.number_input("Acceleration Std (m/s²)", 0.0, 5.0, 0.2)
        braking_events = st.number_input("Braking Events", 0, 50, 5)
        rpm_mean = st.number_input("RPM Mean", 0.0, 10000.0, 3000.0)
        gear_shifts = st.number_input("Gear Shifts", 0, 100, 10)
        trip_duration = st.number_input("Trip Duration (min)", 0.0, 1000.0, 60.0)
        idle_time = st.number_input("Idle Time (min)", 0.0, 200.0, 5.0)
        mileage = st.number_input("Mileage (km)", 0.0, 100000.0, 1000.0)
        jerk_mean = st.number_input("Jerk Mean (m/s³)", 0.0, 5.0, 0.5)
        speed_var = st.number_input("Speed Variance", 0.0, 20.0, 1.0)

        submit = st.form_submit_button("🚀 Predict Behavior")

    if submit:
        features = {
            "avg_speed": avg_speed,
            "acceleration_mean": acceleration_mean,
            "acceleration_std": acceleration_std,
            "braking_events": braking_events,
            "rpm_mean": rpm_mean,
            "gear_shifts": gear_shifts,
            "trip_duration": trip_duration,
            "idle_time": idle_time,
            "mileage": mileage,
            "jerk_mean": jerk_mean,
            "speed_var": speed_var,
        }

        with st.spinner("Predicting behavior..."):
            try:
                response = requests.post(API_URL, json=features)
                if response.status_code == 200:
                    result = response.json()
                    behavior = result["prediction"]["behavior"]
                    confidence = result["prediction"]["confidence"]

                    st.success(f"**Predicted Behavior:** {behavior}")
                    st.progress(int(confidence * 100))
                    st.metric(label="Confidence Level", value=f"{confidence * 100:.1f}%")

                    # Behavior insights
                    st.write("### 🧠 Model Insights")
                    if behavior == "Aggressive":
                        st.warning("⚠️ The rider is showing **Aggressive** behavior. Try smoother acceleration and braking.")
                    elif behavior == "Normal":
                        st.info("🙂 The rider’s behavior is **Normal** and within acceptable limits.")
                    else:
                        st.success("🛡️ The rider shows **Safe** and controlled behavior. Keep it up!")
                else:
                    st.error("Error: Unable to get prediction from the server.")
            except requests.exceptions.ConnectionError:
                st.error("🚫 Could not connect to FastAPI backend. Make sure it’s running.")
