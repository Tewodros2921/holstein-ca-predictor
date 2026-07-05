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
    import streamlit as st

# 1. Section Divider and Header
st.markdown("---")
st.header("🐄 Holstein Cow Calcium Apparent Absorption Model")

# 2. Metric Input Selectors
col_input1, col_input2 = st.columns(2)
with col_input1:
    ca_intake = st.number_input("Calcium Intake in Feed (grams/day):", min_value=1.0, value=100.0, step=5.0)
with col_input2:
    ca_excrete = st.number_input("Calcium Excreted in Feces (grams/day):", min_value=0.0, value=60.0, step=5.0)

# 3. Dynamic Biological Math Processing
ca_absorbed = ca_intake - ca_excrete
if ca_intake > 0:
    apparent_absorption_pct = (ca_absorbed / ca_intake) * 100
else:
    apparent_absorption_pct = 0.0

# 4. Live Metric KPI Scoreboards
col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium", value=f"{ca_intake} g")
with col_res2:
    st.metric(label="💩 Excreted Calcium", value=f"{ca_excrete} g", delta=f"-{ca_excrete} g", delta_color="inverse")
with col_res3:
    st.metric(label="✅ Apparent Absorbed", value=f"{ca_absorbed} g")

# 5. Scientific Equation Breakdown
st.markdown("### 🧮 Apparent Absorption Formula")
st.latex(r"\text{Apparent Absorption \%} = \left( \frac{\text{Intake Calcium} - \text{Excreted Calcium}}{\text{Intake Calcium}} \right) \times 100")
st.info(f"**Step-by-step Math:** (({ca_intake}g - {ca_excrete}g) ÷ {ca_intake}g) × 100 = **{apparent_absorption_pct:.1f}%**")

# 6. Conceptual Diagram Visual Flowchart Layout
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-around; align-items: center; background-color: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #eaeaea; margin-top: 15px;">
        <div style="text-align: center; background-color: #2b7bba; color: white; padding: 12px; border-radius: 6px; width: 25%;">
            <p style="margin: 0; font-weight: bold;">1. Feed Intake</p>
            <p style="font-size: 18px; margin: 3px 0 0 0;">{ca_intake} g</p>
        </div>
        <div style="font-size: 24px; color: #2b7bba;">➡️</div>
        <div style="text-align: center; background-color: #ffffff; color: #333; padding: 12px; border-radius: 6px; width: 30%; border: 2px solid #555;">
            <p style="margin: 0; font-weight: bold;">🐄 Holstein Body</p>
            <p style="font-size: 14px; margin: 3px 0 0 0;"><b>Apparent Absorption:</b> {apparent_absorption_pct:.1f}%</p>
        </div>
        <div style="font-size: 24px; color: #d9534f;">➡️</div>
        <div style="text-align: center; background-color: #d9534f; color: white; padding: 12px; border-radius: 6px; width: 25%;">
            <p style="margin: 0; font-weight: bold;">2. Fecal Waste</p>
            <p style="font-size: 18px; margin: 3px 0 0 0;">{ca_excrete} g</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

