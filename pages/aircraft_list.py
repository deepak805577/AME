import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header

# --- PAGE CONFIG ---
st.set_page_config(page_title="Registered Aircraft", layout="wide")

# --- VALIDATION ---
if "selected_brand" not in st.session_state:
    st.warning("Please go back and select an aircraft brand.")
    st.stop()

selected_brand = st.session_state.selected_brand

# --- HEADER ---
colored_header(
    label=f"✈️ {selected_brand} Aircraft Fleet",
    description="Select an aircraft to view maintenance details or predictions.",
    color_name="blue-70",
)

st.image(f"data/{selected_brand.lower()}.png", width=200)

# --- LOAD DATA ---
df = pd.read_csv("data/aircraft_data.csv")
filtered_df = df[df["Manufacturer"] == selected_brand]

# --- DISPLAY TABLE ---
st.dataframe(filtered_df, use_container_width=True)

# --- AIRCRAFT SELECTOR ---
selected_id = st.selectbox("🔍 Select Aircraft for Maintenance Prediction", filtered_df["Aircraft ID"])

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧠 Predict Maintenance"):
        st.session_state.selected_aircraft = selected_id
        st.switch_page("pages/maintenance_predict.py")
with col2:
    if st.button("⬅️ Back to Home"):
        st.switch_page("app.py")

# --- MAINTENANCE HISTORY ---
st.markdown("### 🛠 Maintenance History")
try:
    log_df = pd.read_csv("data/maintenance_log.csv")
    aircraft_log = log_df[log_df["Aircraft ID"] == selected_id]
    if not aircraft_log.empty:
        st.dataframe(aircraft_log, use_container_width=True)
    else:
        st.info("No maintenance logs found for this aircraft.")
except FileNotFoundError:
    st.error("❌ 'maintenance_log.csv' not found in the 'data' folder.")
except Exception as e:
    st.error(f"⚠️ Unexpected error: {e}")
