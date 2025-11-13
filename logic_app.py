import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# --------------------------------------------
# 🚀 PAGE CONFIGURATION
# --------------------------------------------
st.set_page_config(
    page_title="Bike Performance Classification",
    page_icon="🏍️",
    layout="wide"
)

st.title("🏍️ Bike Performance Classification Based on Rider Behavior")
st.markdown("### A Minor Project")
st.markdown("---")

# --------------------------------------------
# 🧠 LOAD OR CREATE MODEL
# --------------------------------------------
try:
    model = joblib.load("model/rider_model.pkl")
    st.success("✅ ML Model Loaded Successfully!")
except:
    st.warning("⚠️ No trained model found. Using a mock Random Forest model for demo.")
    # Mock model for simulation
    model = RandomForestClassifier()
    X_dummy = np.random.rand(30, 3)
    y_dummy = np.random.choice(["Smooth", "Aggressive", "Risky"], 30)
    model.fit(X_dummy, y_dummy)

# --------------------------------------------
# 📊 DATA SIMULATION FUNCTION
# --------------------------------------------
def generate_simulated_data(n=1):
    speed = np.random.uniform(20, 120, n)  # km/h
    acceleration = np.random.uniform(-3, 4, n)  # m/s²
    tilt = np.random.uniform(-20, 20, n)  # degrees
    return pd.DataFrame({"Speed": speed, "Acceleration": acceleration, "Tilt": tilt})

# --------------------------------------------
# ⚙️ SIDEBAR CONTROLS
# --------------------------------------------
st.sidebar.header("⚙️ Controls")
simulate = st.sidebar.checkbox("Simulate Live Data", value=True)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 0.5, 5.0, 1.0)
num_samples = st.sidebar.slider("Samples per update", 1, 10, 5)

st.sidebar.markdown("---")
st.sidebar.info("This app analyzes simulated bike data to classify rider behavior into: **Smooth**, **Aggressive**, or **Risky**.")

# --------------------------------------------
# 📈 DASHBOARD DISPLAY
# --------------------------------------------
data_placeholder = st.empty()
data_history = pd.DataFrame(columns=["Speed", "Acceleration", "Tilt", "Prediction"])

if simulate:
    st.markdown("### 📡 Live Data Simulation")

    run_simulation = st.button("▶️ Start Simulation")

    if run_simulation:
        with data_placeholder.container():
            for i in range(100):
                new_data = generate_simulated_data(num_samples)
                pred = model.predict(new_data)
                new_data["Prediction"] = pred

                data_history = pd.concat([data_history, new_data]).tail(100)

                # Layout columns
                col1, col2, col3 = st.columns(3)
                latest_row = new_data.iloc[-1]

                with col1:
                    st.metric("Current Speed (km/h)", f"{latest_row['Speed']:.2f}")
                with col2:
                    st.metric("Acceleration (m/s²)", f"{latest_row['Acceleration']:.2f}")
                with col3:
                    st.metric("Tilt Angle (°)", f"{latest_row['Tilt']:.2f}")

                # Behavior display
                st.markdown(f"### 🚦 Rider Behavior: **{latest_row['Prediction']}**")

                # Line chart for trends
                fig, ax = plt.subplots(1, 1, figsize=(8, 3))
                ax.plot(data_history["Speed"].values, label="Speed (km/h)")
                ax.plot(data_history["Acceleration"].values, label="Acceleration (m/s²)")
                ax.legend()
                ax.set_xlabel("Time Steps")
                ax.set_ylabel("Value")
                st.pyplot(fig)

                # Behavior distribution
                behavior_counts = data_history["Prediction"].value_counts()
                st.bar_chart(behavior_counts)

                time.sleep(refresh_rate)
                st.toast(f"Updated at iteration {i+1}")

else:
    st.markdown("☑️ Simulation is off. Turn it on from the sidebar to view live updates.")

# --------------------------------------------
# 📘 ABOUT SECTION
# --------------------------------------------
st.markdown("---")
st.subheader("📘 About Project")
st.write("""
This project classifies rider behavior based on simulated or real bike data.  
It uses machine learning algorithms (like Random Forest or XGBoost) to categorize rides as:
- 🟢 **Smooth** — consistent acceleration and speed  
- 🟠 **Aggressive** — high acceleration and frequent braking  
- 🔴 **Risky** — abrupt turns, large tilt angles  

Future versions will integrate IoT sensors (ESP32 + MPU6050) for real-time bike monitoring.
""")
