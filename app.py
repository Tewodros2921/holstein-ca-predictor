import streamlit as st
import numpy as np

# Force page configuration metadata for global mobile devices
st.set_page_config(
    page_title="Holstein Ca Predictor", 
    page_icon="🥛", 
    layout="centered"
)

st.title("🥛 Holstein Calcium Absorption Predictor")
st.markdown("### 🎓 M.Sc. Research Project | The Hebrew University of Jerusalem (HUJI)")
st.info("🔬 Developed at the **Volcani Agricultural Research Organization**, Department of Soil, Water, and Environmental Sciences.")

st.markdown("""
**Project Objective:** 
This interactive multi-level meta-regression tool calculates the non-linear apparent calcium absorption 
efficiency in lactating Holstein dairy cattle. It translates core metabolic data into actionable physiological 
insights to optimize livestock mineral management and reduce environmental excretion pathways.
""")

st.sidebar.header("🔬 Input Herd & Feed Metrics")

tmr_ca_pct = st.sidebar.slider("TMR Calcium Concentration (%)", 0.2, 2.0, 0.7, 0.05)
dmi_kg_d = st.sidebar.slider("Dry Matter Intake (DMI, kg/day)", 10.0, 30.0, 22.0, 0.5)
days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)
urinary_ca_g_d = st.sidebar.slider("Urinary Calcium (g/day)", 0.1, 10.0, 1.5, 0.1)
milk_ca_g_d = st.sidebar.slider("Milk Calcium Output (g/day)", 10.0, 60.0, 35.0, 1.0)

intercept = 334.37
beta_tmr_ca = -343.88
beta_dmi = 17.26
beta_dim = -2.01
beta_urinary = 4.96
beta_milk_ca = -14.20

int_ca_dmi = -26.31
int_ca_dim = 2.42
int_ca_urinary = -9.41
int_ca_milk = 17.04

predicted_absorption = (
    intercept + 
    (beta_tmr_ca * tmr_ca_pct) + 
    (beta_dmi * dmi_kg_d) + 
    (beta_dim * days_in_milk) + 
    (beta_urinary * urinary_ca_g_d) + 
    (beta_milk_ca * milk_ca_g_d) +
    (int_ca_dmi * tmr_ca_pct * dmi_kg_d) +
    (int_ca_dim * tmr_ca_pct * days_in_milk) +
    (int_ca_urinary * tmr_ca_pct * urinary_ca_g_d) +
    (int_ca_milk * tmr_ca_pct * milk_ca_g_d)
)

predicted_absorption = max(0.0, min(100.0, predicted_absorption))

st.subheader("🔮 Model Prediction Result")
st.metric(label="Predicted Apparent Calcium Absorption Efficiency", value=f"{predicted_absorption:.2f} %")

if predicted_absorption < 25.0:
    st.warning("⚠️ **Low Efficiency:** High risk of mineral pass-through and environmental fecal excretion.")
elif predicted_absorption > 55.0:
    st.info("📈 **High Activity:** Intestinal active transport channels upregulated (high metabolic draw).")
else:
    st.success("✅ **Normal Range:** Physiological baseline absorption levels maintained.")
