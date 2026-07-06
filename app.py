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

# --- USER SIDEBAR INPUT PARAMETERS ---
st.sidebar.header("🔬 Input Herd & Feed Metrics")
# Changing this slider will now directly recalculate the apparent absorption (Y) below
days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)

# --- THE CALCULATOR AND DYNAMIC VARIABLE METRICS ---
st.markdown("---")
st.subheader("🐄 Holstein Cow Calcium Apparent Absorption Model")

# Input fields for your math parameters
ca_intake = st.number_input("Calcium Intake in Feed (X, grams/day):", min_value=1.0, value=100.0, step=5.0)

# --- CORE QUADRATIC MODEL PREDICTOR (Y) ---
# Image Equation Formula Matrix: Y = 62.47 + (-0.2611 * X) + (0.000561 * X^2) + (-0.0202 * DIM)
intercept = 62.47
beta_x = -0.2611
beta_x_sq = 0.000561
beta_dim = -0.0202

predicted_y = (
    intercept + 
    (beta_x * ca_intake) + 
    (beta_x_sq * (ca_intake ** 2)) + 
    (beta_dim * days_in_milk)
)

# Constrain prediction output boundaries between realistic physiological scales (0% - 100%)
predicted_y = max(0.0, min(100.0, predicted_y))

# Back-calculating the physical excreted feces amount based on your quadratic formula prediction
# Since Y% = ((Intake - Feces) / Intake) * 100 -> Feces = Intake - (Y% * Intake / 100)
calculated_feces = ca_intake - ((predicted_y / 100.0) * ca_intake)
calculated_absorbed_g = ca_intake - calculated_feces

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium (X)", value=f"{ca_intake:.1f} g")
with col_res2:
    st.metric(label="💩 Estimated Fecal Excretion", value=f"{calculated_feces:.1f} g")
with col_res3:
    st.metric(label="✅ Predicted Absorbed Mass", value=f"{calculated_absorbed_g:.1f} g")


# --- RENDERING THE ACTIVE OUTCOME MODEL SCOREBOARD PANEL ---
st.markdown("---")
st.subheader("🔮 Model Prediction Result (Y)")
st.metric(label="Predicted Apparent Calcium Absorption Efficiency (Y)", value=f"{predicted_y:.2f} %")

# Academic LaTex presentation formula card block
st.markdown("### 🧮 Quadratic Model Regression Formula")
st.latex(r"Y = 62.47 + (-0.2611 \times X) + (0.000561 \times X^2) + (-0.0202 \times \text{DIM})")
st.info(f"**Live Math Loop Execution:** 62.47 + (-0.2611 × {ca_intake}) + (0.000561 × {ca_intake}²) + (-0.0202 × {days_in_milk}) = **{predicted_y:.2f}%**")

if predicted_y < 25.0:
    st.warning("⚠️ **Low Predicted Efficiency:** High risk of mineral pass-through and environmental fecal excretion.")
elif predicted_y > 55.0:
    st.info("📈 **High Predicted Activity:** Intestinal active transport channels upregulated (high metabolic draw).")
else:
    st.success("✅ **Normal Range:** Physiological baseline absorption levels maintained.")


# --- STABLE VISUAL PIPELINE FLOW LAYOUT PANEL ---
st.markdown("---")
st.markdown(
    f"""
    <style>
    @keyframes waveFlow {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 100% 50%; }}
    }}
    .animated-arrow {{
        font-size: 28px;
        background: linear-gradient(90deg, #2b7bba, #2ca25f, #2b7bba);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: waveFlow 2s linear infinite;
    }}
    .animated-arrow-waste {{
        font-size: 28px;
        background: linear-gradient(90deg, #d9534f, #f0ad4e, #d9534f);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: waveFlow 1.5s linear infinite;
    }}
    </style>
    
    <div style="display: flex; justify-content: space-around; align-items: center; background-color: #f9f9f9; padding: 25px; border-radius: 10px; border: 1px solid #eaeaea;">
        <div style="text-align: center; background-color: #2b7bba; color: white; padding: 15px; border-radius: 8px; width: 25%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">1. Intake Feed (X)</p>
            <p style="font-size: 20px; margin: 5px 0 0 0; font-weight: bold;">{ca_intake:.1f} g</p>
        </div>
        <div class="animated-arrow">➡️  ➡️</div>
        <div style="text-align: center; background-color: #ffffff; color: #333; padding: 15px; border-radius: 8px; width: 32%; border: 2px solid #555; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">🐄 Holstein Body</p>
            <p style="font-size: 15px; margin: 5px 0 0 0; color: #2ca25f;"><b>Predicted Abs (Y):</b> {predicted_y:.1f}%</p>
            <p style="font-size: 13px; margin: 2px 0 0 0; color: #666;">Retained: {calculated_absorbed_g:.1f} g/day</p>
        </div>
        <div class="animated-arrow-waste">➡️  ➡️</div>
        <div style="text-align: center; background-color: #d9534f; color: white; padding: 15px; border-radius: 8px; width: 25%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">2. Fecal Waste</p>
            <p style="font-size: 20px; margin: 5px 0 0 0; font-weight: bold;">{calculated_feces:.1f} g</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
