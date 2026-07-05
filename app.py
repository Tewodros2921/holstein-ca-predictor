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
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import base64
import os

st.markdown("---")
st.subheader("🎬 Animated Apparent Absorption Flow Model")
st.markdown("This animated simulation traces the path of calcium molecules, visualizing the absolute physical difference between intake metrics and fecal output waste blocks.")

def generate_absorption_animation(intake_val, excrete_val):
    # Setup plotting figure canvas
    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Draw static structural components (Mouth, Cow Body Tissue, Waste Pipeline)
    ax.add_patch(plt.Rectangle((3.8, 1.5), 2.4, 2, fill=True, color='#f0f0f0', ec='#333333', lw=2))
    ax.text(5.0, 2.5, "🐄 Holstein Body\n(Retention)", ha='center', va='center', weight='bold', color='#222')
    
    # Generate point coordinates for nutrient particle motion tracks
    num_particles = 15
    frames_count = 40
    
    # Calculate partition thresholds based on user efficiency configurations
    absorbed_count = max(1, int(num_particles * ((intake_val - excrete_val) / intake_val)))
    
    particle_paths = []
    for i in range(num_particles):
        start_y = np.random.uniform(2.2, 2.8)
        if i < absorbed_count:
            # Route A: Particles entering and staying absorbed inside body mass
            x_track = np.linspace(0.5, 5.0, frames_count)
            y_track = np.linspace(start_y, 2.5, frames_count)
        else:
            # Route B: Particles bypassing retention, exiting as waste
            x_track = np.concatenate([np.linspace(0.5, 5.0, 20), np.linspace(5.0, 9.5, 20)])
            y_track = np.concatenate([np.linspace(start_y, 2.0, 20), np.linspace(2.0, 1.2, 20)])
        particle_paths.append((x_track, y_track))
        
    scat = ax.scatter([], [], c=[], s=80, zorder=5)
    
    def update(frame):
        x_display, y_display, colors = [], [], []
        for i in range(num_particles):
            x_display.append(particle_paths[i][0][frame])
            y_display.append(particle_paths[i][1][frame])
            # Highlight absorbed molecules green, unabsorbed waste paths red
            colors.append('#2ca25f' if i < absorbed_count else '#de2d26')
        scat.set_offsets(np.c_[x_display, y_display])
        scat.set_color(colors)
        return scat,

    # Build the animation matrix and save it out as a local GIF file format
    ani = animation.FuncAnimation(fig, update, frames=frames_count, interval=100, blit=True)
    gif_path = "absorption_flow.gif"
    ani.save(gif_path, writer='pillow', fps=10)
    plt.close(fig)
    return gif_path

# Execute generator function and pipe rendering out into base64 HTML tags
# (This ensures it bypasses browser sandbox filters perfectly)
with st.spinner("Generating animation track..."):
    gif_file = generate_absorption_animation(ca_intake, ca_excrete)
    with open(gif_file, "rb") as f:
        data_bytes = f.read()
        b64_encoded = base64.b64encode(data_bytes).decode()
        st.markdown(f'<img src="data:image/gif;base64,{b64_encoded}" width="100%">', unsafe_allow_html=True)
        import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.markdown("---")
st.header("🎯 Thesis Objective Analysis: Dietary Effects on Mid-Lactation Absorption")
st.markdown("""
**Research Focus:** Evaluating how incremental shifts in daily dietary calcium intake 
influence the overall apparent absorption efficiency (%) specifically during mid-lactation for Holstein cows.
""")

# --- MODULE 1: THE PHYSIOLOGICAL TREND GRAPH ---
def simulate_absorption_curve(current_intake):
    # Simulated data points showing efficiency drop as intake exceeds requirements
    intake_range = np.linspace(50, 200, 50)
    efficiency_curve = 65 - (intake_range * 0.15) + np.sin(intake_range / 10) * 2
    return intake_range, efficiency_curve

intake_track, eff_track = simulate_absorption_curve(ca_intake)

fig_obj, ax_obj = plt.subplots(figsize=(6, 3), dpi=100)
ax_obj.plot(intake_track, eff_track, color='#2b7bba', lw=2.5, label='Mid-Lactation Response Curve')
ax_obj.scatter(ca_intake, apparent_absorption_pct, color='#d9534f', s=120, zorder=5, 
               label=f'Your Test Layout ({ca_intake}g)')

ax_obj.set_title("Dietary Intake Level vs. Apparent Absorption Efficiency", fontsize=10, weight='bold')
ax_obj.set_xlabel("Dietary Calcium Intake (g/day)", fontsize=8)
ax_obj.set_ylabel("Apparent Absorption (%)", fontsize=8)
ax_obj.grid(True, linestyle='--', alpha=0.5)
ax_obj.legend(fontsize=7, loc='upper right')
st.pyplot(fig_obj)

# --- MODULE 2: INTERPRETATION SHIFTS ---
st.markdown("### 📝 Mid-Lactation Physiological Interpretation")
if ca_intake < 80:
    st.info("💡 **Low Dietary Intake Phase:** In mid-lactation, low dietary calcium forces the animal to increase gut absorption efficiency active transport mechanisms (calbindin-D9k upregulation) to meet milk output demands.")
elif 80 <= ca_intake <= 140:
    st.success("💡 **Optimal Dietary Balance Phase:** Homeostasis is comfortably maintained. The transition between active gut transport and passive paracellular absorption is optimized for stable milk production margins.")
else:
    st.warning("💡 **Excess Dietary Intake Phase:** High calcium diets trigger passive absorption pathways while down-regulating active transport. Excess calcium passes unabsorbed, causing a noticeable drop in overall apparent absorption efficiency.")

# --- MODULE 3: DATA EXPORT FOR USERS ---
st.subheader("📊 Export Experimental Trial Data")
export_data = {
    "Parameter Metric": ["Total Calcium Intake", "Fecal Calcium Excretion", "Apparent Absorption Efficiency"],
    "Value": [f"{ca_intake} g/day", f"{ca_excrete} g/day", f"{apparent_absorption_pct:.2f}%"]
}
df_report = pd.DataFrame(export_data)
st.dataframe(df_report, use_container_width=True)

csv_buffer = io.StringIO()
df_report.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode('utf-8')

st.download_button(
    label="📥 Download Data Report (CSV File)",
    data=csv_bytes,
    file_name="holstein_calcium_trial_report.csv",
    mime="text/csv"
)



