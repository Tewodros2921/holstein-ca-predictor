# ---------------------------------------------------------
# MODEL RESULT
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🔮 Model Prediction Result (Y)")
st.metric("Predicted Apparent Calcium Absorption Efficiency (Y)", f"{predicted_y:.2f} %")

st.markdown("### 🧮 Quadratic Model Regression Formula")
st.latex(r"Y = 62.47 + (-0.2611 \times X) + (0.000561 \times X^2) + (-0.0202 \times \text{DIM})")

st.info(f"**Live Equation Process:** 62.47 + (-0.2611 × {ca_intake}) + (0.000561 × {ca_intake}²) + (-0.0202 × {days_in_milk}) = **{predicted_y:.2f}%**")
st.success(f"**Fecal Mass Derivation:** {ca_intake}g Intake - ({predicted_y:.2f}% Absorption × {ca_intake}g) = **{calculated_feces:.1f} grams of Fecal Calcium**")

# ---------------------------------------------------------
# CLEAN IF / ELIF / ELSE BLOCK
# ---------------------------------------------------------
if predicted_y < 25.0:
    st.warning("⚠️ Low Predicted Efficiency: High risk of mineral pass-through and environmental fecal excretion.")
elif predicted_y > 55.0:
    st.info("📈 High Predicted Activity: Intestinal active transport channels upregulated (high metabolic draw).")
else:
    st.success("✅ Normal Range: Physiological baseline absorption levels maintained.")

# ---------------------------------------------------------
# DATASET CALCULATION BLOCK
# ---------------------------------------------------------
if "Ca_Intake" in df.columns and "Fecal_Ca" in df.columns:
    df["Apparent_Ca_Absorption"] = (
