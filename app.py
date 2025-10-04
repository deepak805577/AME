import streamlit as st
from PIL import Image
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Aircraft Maintenance Explorer", page_icon="✈️", layout="wide")

# --- LOAD CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("assets/styles.css")

# Background styling
background_image_url = "https://flyxo.com/_next/image/?url=https%3A%2F%2Fwebsite-cdn.flyxo.com%2Fdata%2Fwebapi%2Fnew_plane_home_326d044e05.jpg&w=1920&q=80"
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .img-container img {{
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: transform 0.3s;
    }}
    .img-container img:hover {{
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)



# --- HEADER SECTION ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("data/airbus.png", use_container_width=True)
with col2:
    st.markdown("<h1 class='title'>Aircraft Maintenance Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Smart Maintenance • Real-time Analytics • AI Insights</p>", unsafe_allow_html=True)
with col3:
    st.image("data/Boeing.png", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🛫 Aircraft List", "🧠 Maintenance Predictor", "📊 Performance"])

# --- HOME TAB ---
with tab1:
    st.markdown("### Welcome to the Aircraft Maintenance Explorer")
    st.markdown("""
    Analyze your aircraft fleet, predict maintenance needs, and track performance insights — all in one place.
    """)

    st.markdown("### 📦 Data Overview")
    data_files = ["aircraft_data.csv", "components.csv", "maintenance_log.csv", "performance.csv"]
    df_summary = pd.DataFrame({
        "File": data_files,
        "Description": [
            "Aircraft specifications and details",
            "Component inventory with expiry dates",
            "Maintenance logs and service history",
            "Performance and efficiency metrics"
        ]
    })
    st.dataframe(df_summary, use_container_width=True)

# --- AIRCRAFT LIST TAB ---
with tab2:
    st.subheader("🛩 Aircraft Fleet Overview")
    data = pd.read_csv("data/aircraft_data.csv")
    st.dataframe(data, use_container_width=True)

# --- MAINTENANCE PREDICTOR TAB ---
with tab3:
    st.subheader("🧠 Predictive Maintenance")

    brand = st.selectbox("✈️ Select Aircraft Brand", ["Airbus", "Boeing"])
    st.image(f"data/{brand.lower()}.png", width=200)

    if st.button("🚀 Open Aircraft List"):
        st.session_state.selected_brand = brand
        st.switch_page("pages/aircraft_list.py")

# --- PERFORMANCE TAB ---
with tab4:
    st.subheader("📈 Performance Metrics")
    perf = pd.read_csv("data/performance.csv")
    st.line_chart(perf.set_index(perf.columns[0]))

# --- FOOTER ---
st.markdown("""
<hr>
<div style='text-align:center; color:gray;'>
Aircraft Maintenance Explorer © 2025 • Developed with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
