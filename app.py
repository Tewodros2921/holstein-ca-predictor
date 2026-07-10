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
# --- UPDATED INSTITUTIONAL AFFILIATION LINE ---
st.info("🔬 Developed at the **Agricultural Research Organization - Volcani Institute**, Department of Ruminant Science.")

st.markdown("""
**Project Objective:** 
This interactive multi-level meta-regression tool calculates the non-linear apparent calcium absorption 
efficiency in lactating Holstein dairy cattle. It translates core metabolic data into actionable physiological 
insights to optimize livestock mineral management and reduce environmental excretion pathways.
""")

# --- USER SIDEBAR INPUT PARAMETERS ---
st.sidebar.header("🔬 Input Herd & Feed Metrics")
# Variable 2: DIM (Days in Milk)
days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)

# --- THE CALCULATOR AND DYNAMIC VARIABLE METRICS ---
st.markdown("---")
st.subheader("🐄 Holstein Cow Calcium Apparent Absorption Model")

# Variable 1: X (Calcium Intake in Feed)
ca_intake = st.number_input("Calcium Intake in Feed (X, grams/day):", min_value=1.0, value=100.0, step=5.0)


# --- CORE QUADRATIC MODEL PREDICTOR (Y) ---
# Image Equation Formula Matrix: Y = 62.47 + (-0.2611 * X) + (0.000561 * X^2) + (-0.0202 * DIM)
intercept = 62.47
beta_x = -0.2611
beta_x_sq = 0.000561
beta_dim = -0.0202

# Solving for Y (Predicted Apparent Calcium Absorption Efficiency %)
predicted_y = (
    intercept + 
    (beta_x * ca_intake) + 
    (beta_x_sq * (ca_intake ** 2)) + 
    (beta_dim * days_in_milk)
)

# Apply physiological boundary constraints (0% to 100%)
predicted_y = max(0.0, min(100.0, predicted_y))


# --- METABOLIC MASS BALANCE CALCULATIONS ---
# Fecal Calcium is the structural mathematical difference between total Intake and absolute Absorption mass
# Formula: Fecal Ca = Intake - (Absorption % * Intake)
calculated_absorbed_g = (predicted_y / 100.0) * ca_intake
calculated_feces = ca_intake - calculated_absorbed_g


# --- RENDERING THE LIVE EXPERIMENTAL KPI SCOREBOARDS ---
col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium (X)", value=f"{ca_intake:.1f} g")
with col_res2:
    st.metric(label="💩 Calculated Fecal Calcium", value=f"{calculated_feces:.1f} g", delta="Excreted Waste", delta_color="inverse")
with col_res3:
    st.metric(label="✅ Predicted Absorbed Mass", value=f"{calculated_absorbed_g:.1f} g", delta="Retained Balance")


# --- RENDERING THE MODEL OUTCOME METRIC PANEL ---
st.markdown("---")
st.subheader("🔮 Model Prediction Result (Y)")
st.metric(label="Predicted Apparent Calcium Absorption Efficiency (Y)", value=f"{predicted_y:.2f} %")

# Academic LaTex presentation formula card block for your thesis committee
st.markdown("### 🧮 Quadratic Model Regression Formula")
st.latex(r"Y = 62.47 + (-0.2611 \times X) + (0.000561 \times X^2) + (-0.0202 \times \text{DIM})")

# Live math text string showing exact substitution variables dynamically
st.info(f"**Live Equation Process:** 62.47 + (-0.2611 × {ca_intake}) + (0.000561 × {ca_intake}²) + (-0.0202 × {days_in_milk}) = **{predicted_y:.2f}%**")
st.success(f"**Fecal Mass Derivation:** {ca_intake}g Intake - ({predicted_y:.2f}% Absorption × {ca_intake}g) = **{calculated_feces:.1f} grams of Fecal Calcium**")

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
            <p style="font-size: 13px; margin: 2px 0 0 0; color: #666;">Absorbed: {calculated_absorbed_g:.1f} g/day</p>
        </div>
        <div class="animated-arrow-waste">➡️  ➡️</div>
        <div style="text-align: center; background-color: #d9534f; color: white; padding: 15px; border-radius: 8px; width: 25%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">2. Fecal Calcium</p>
            <p style="font-size: 20px; margin: 5px 0 0 0; font-weight: bold;">{calculated_feces:.1f} g</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.header("Data Processing")

if "Ca_Intake" in df.columns and "Fecal_Ca" in df.columns:
    df["Apparent_Ca_Absorption"] = (df["Ca_Intake"] - df["Fecal_Ca"]) / df["Ca_Intake"]
    st.write("### Apparent Calcium Absorption Added to Dataset")
    st.dataframe(df)
else:
    st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats
st.header("Upload Your Dataset")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Raw Data")
    st.dataframe(df
                st.header("Graphing Module")

response = st.selectbox("Select Response Variable", df.columns)
predictor = st.selectbox("Select Predictor Variable", df.columns)

fig, ax = plt.subplots()
sns.regplot(data=df, x=predictor, y=response, ax=ax, scatter_kws={'alpha':0.7})
ax.set_title(f"{response} vs {predictor}")
st.pyplot(fig)
st.header("Statistical Analysis")

formula = f"{response} ~ {predictor}"
model = smf.ols(formula, data=df).fit()

st.subheader("Linear Model Summary")
st.text(model.summary())
anova_table = sm.stats.anova_lm(model, typ=2)
st.subheader("ANOVA Table")
st.write(anova_table)
corr, pval = stats.pearsonr(df[predictor], df[response])
st.write(f"Correlation: {corr:.3f}")
st.write(f"P-value: {pval:.4f}")
fig3, ax3 = plt.subplots()
sns.residplot(x=model.fittedvalues, y=model.resid, lowess=True, ax=ax3)
ax3.set_xlabel("Fitted Values")
ax3.set_ylabel("Residuals")
ax3.set_title("Residual Plot")
st.pyplot(fig3
         st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")import streamlit as st
                                                                        ^
SyntaxError: invalid syntax
st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")

import streamlit as st
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats
if "Ca_Intake" in df.columns and "Fecal_Ca" in df.columns:
    df["Apparent_Ca_Absorption"] = (
        (df["Ca_Intake"] - df["Fecal_Ca"]) / df["Ca_Intake"]
    )
    st.success("Apparent Calcium Absorption calculated successfully.")
else:
    st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")
    st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")import streamlit as st
                                                                        ^
SyntaxError: invalid syntax
st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")import streamlit as st
st.warning("Dataset must include Ca_Intake and Fecal_Ca columns.")import streamlit as st















