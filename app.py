import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Holstein Ca Predictor",
    page_icon="🥛",
    layout="centered"
)

# ---------------------------------------------------------
# TITLE & INTRO
# ---------------------------------------------------------
st.title("🥛 Holstein Calcium Absorption Predictor")
st.markdown("### 🎓 M.Sc. Research Project | The Hebrew University of Jerusalem (HUJI)")
st.info("🔬 Developed at the Agricultural Research Organization - Volcani Institute.")

st.markdown("""
This tool estimates apparent calcium absorption efficiency in lactating Holstein cows.
""")

# ---------------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------------
st.sidebar.header("🔬 Input Herd & Feed Metrics")

days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)
milk_yield = st.sidebar.slider("Milk Yield (kg/day)", 10, 60, 35)
dietary_ca = st.sidebar.slider("Dietary Ca (%)", 0.3, 1.2, 0.7)

# ---------------------------------------------------------
# CAMERA STREAM INPUT
# ---------------------------------------------------------
st.sidebar.header("📷 Camera Stream")
camera_url = st.sidebar.text_input(
    "Enter camera URL",
    "http://10.147.17.10:8080/video"
)

# ---------------------------------------------------------
# SIMPLE DEMO MODEL (replace with your real regression)
# ---------------------------------------------------------
absorption = (
    0.25 +
    (milk_yield * 0.005) +
    (dietary_ca * 0.15) -
    (days_in_milk * 0.0003)
)

# ---------------------------------------------------------
# OUTPUT SECTION
# ---------------------------------------------------------
st.subheader("📈 Predicted Apparent Ca Absorption")
st.metric("Absorption Efficiency (%)", f"{absorption*100:.2f}")

# ---------------------------------------------------------
# CAMERA DISPLAY
# ---------------------------------------------------------
st.subheader("📷 Live Camera Stream")

if camera_url:
    st.markdown(f"**Camera URL:** {camera_url}")
    st.video(camera_url)
else:
    st.warning("Please enter a camera URL.")
