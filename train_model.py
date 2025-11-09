import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

np.random.seed(42)
N = 2000
df = pd.DataFrame({
    'avg_speed': np.random.uniform(20, 100, N),
    'acceleration_mean': np.random.uniform(0.5, 3.0, N),
    'acceleration_std': np.random.uniform(0.1, 1.5, N),
    'braking_events': np.random.randint(0, 6, N),
    'rpm_mean': np.random.uniform(2000, 8000, N),
    'gear_shifts': np.random.randint(5, 40, N),
    'trip_duration': np.random.uniform(5, 60, N),
    'idle_time': np.random.uniform(0, 5, N),
    'mileage': np.random.uniform(20, 50, N),
    'jerk_mean': np.random.uniform(0.2, 2.0, N),
    'speed_var': np.random.uniform(2, 12, N)
})

def label_row(r):
    if r['avg_speed'] > 75 or r['acceleration_mean'] > 2.6:
        return "Aggressive"
    if r['avg_speed'] < 40 and r['mileage'] > 38:
        return "Efficient"
    return "Moderate"

df['behavior'] = df.apply(label_row, axis=1)

X = df.drop(columns='behavior')
y = df['behavior']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "bike_behavior_model.pkl")
print("Saved bike_behavior_model.pkl")