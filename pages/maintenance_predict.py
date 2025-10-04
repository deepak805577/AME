import streamlit as st 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --- PAGE CONFIG ---
st.set_page_config(page_title="Maintenance Predictor", layout="wide")

# --- VALIDATE SESSION ---
if "selected_aircraft" not in st.session_state:
    st.warning("No aircraft selected. Please go back to Aircraft List.")
    st.stop()

aircraft_id = st.session_state.selected_aircraft
st.title(f"🛠 Maintenance Prediction for Aircraft: {aircraft_id}")

# --- TRAIN MODEL (demo model) ---
data = {
    'Flight_Hours': [1000, 400, 1200, 200, 850, 1600, 300, 900, 1800, 100],
    'Landings': [500, 150, 600, 80, 400, 900, 100, 450, 950, 30],
    'Engine_Temp': [620, 540, 650, 500, 610, 680, 520, 630, 700, 490],
    'Vibration': [3.0, 1.2, 3.4, 1.0, 2.5, 3.8, 1.1, 3.1, 4.0, 0.9],
    'Last_Maintenance': [150, 60, 200, 40, 120, 250, 50, 130, 270, 30],
    'Maintenance_Needed': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
}
df = pd.DataFrame(data)
X = df.drop('Maintenance_Needed', axis=1)
y = df['Maintenance_Needed']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# --- USER INPUT ---
st.subheader("🔧 Enter Current Flight Data")
c1, c2, c3 = st.columns(3)
with c1:
    flight_hours = st.slider("Flight Hours", 0, 2000, 500)
    landings = st.slider("Landings", 0, 1000, 250)
with c2:
    engine_temp = st.slider("Engine Temp (°C)", 400, 800, 600)
    vibration = st.slider("Vibration Level", 0.0, 5.0, 2.0)
with c3:
    last_maintenance = st.slider("Hours Since Last Maintenance", 0, 300, 100)

input_data = pd.DataFrame([[flight_hours, landings, engine_temp, vibration, last_maintenance]],
    columns=['Flight_Hours', 'Landings', 'Engine_Temp', 'Vibration', 'Last_Maintenance'])

# --- PREDICTION ---
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# --- RESULT ---
st.subheader("📊 Maintenance Prediction Result")
if prediction == 1:
    st.error(f"⚠️ Maintenance likely needed — Confidence: {probability:.2%}")
else:
    st.success(f"✅ No immediate maintenance needed — Confidence: {(1 - probability):.2%}")

# --- COMPONENT EXPIRY ---
st.subheader("🚨 Expired Components Check")
try:
    components_df = pd.read_csv("data/components.csv")
    components_df["Expiry Date"] = pd.to_datetime(components_df["Expiry Date"])
    expired = components_df[
        (components_df["Aircraft ID"] == aircraft_id) &
        (components_df["Expiry Date"] < pd.Timestamp.today())
    ]
    if not expired.empty:
        st.error("⚠️ The following components are expired:")
        st.dataframe(expired, use_container_width=True)
    else:
        st.success("✅ No expired components found.")
except Exception:
    st.warning("Component data missing or incorrect format.")

# --- MAINTENANCE HISTORY ---
st.subheader("📜 Maintenance History")
try:
    history_df = pd.read_csv("data/maintenance_log.csv")
    history_df = history_df[history_df["Aircraft ID"] == aircraft_id]
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No maintenance history for this aircraft.")
except Exception:
    st.warning("Maintenance history file missing or invalid.")

# --- BACK BUTTON ---
if st.button("⬅️ Back to Aircraft List"):
    st.switch_page("pages/aircraft_list.py")
