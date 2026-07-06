import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import base64

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

# --- CALCULATION PART ---
st.markdown("---")
st.subheader("🐄 Holstein Cow Calcium Apparent Absorption Model")

col_input1, col_input2 = st.columns(2)
with col_input1:
    ca_intake = st.number_input("Calcium Intake in Feed (grams/day):", min_value=1.0, value=100.0, step=5.0)
with col_input2:
    ca_excrete = st.number_input("Calcium Excreted in Feces (grams/day):", min_value=0.0, value=60.0, step=5.0)

ca_absorbed = ca_intake - ca_excrete
if ca_intake > 0:
    apparent_absorption_pct = (ca_absorbed / ca_intake) * 100
else:
    apparent_absorption_pct = 0.0

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium", value=f"{ca_intake} g")
with col_res2:
    st.metric(label="💩 Excreted Calcium", value=f"{ca_excrete} g", delta=f"-{ca_excrete} g", delta_color="inverse")
with col_res3:
    st.metric(label="✅ Apparent Absorbed", value=f"{ca_absorbed} g")

st.markdown("### 🧮 Apparent Absorption Formula")
st.latex(r"\text{Apparent Absorption \%} = \left( \frac{\text{Intake Calcium} - \text{Excreted Calcium}}{\text{Intake Calcium}} \right) \times 100")
st.info(f"**Step-by-step Math:** (({ca_intake}g - {ca_excrete}g) ÷ {ca_intake}g) × 100 = **{apparent_absorption_pct:.1f}%**")

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

# --- ANIMATION PART ---
st.markdown("---")
st.subheader("🎬 Animated Apparent Absorption Flow Model")

def generate_absorption_animation(intake_val, excrete_val):
    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    ax.add_patch(plt.Rectangle((3.8, 1.5), 2.4, 2, fill=True, color='#f0f0f0', ec='#333333', lw=2))
    ax.text(5.0, 2.5, "🐄 Holstein Body\n(Retention)", ha='center', va='center', weight='bold', color='#222')
    
    num_particles = 15
    frames_count = 40
    absorbed_count = max(1, int(num_particles * ((intake_val - excrete_val) / intake_val)))
    
    particle_paths = []
    for i in range(num_particles):
        start_y = np.random.uniform(2.2, 2.8)
        if i < absorbed_count:
            x_track = np.linspace(0.5, 5.0, frames_count)
            y_track = np.linspace(start_y, 2.5, frames_count)
        else:
            x_track = np.concatenate([np.linspace(0.5, 5.0, 20), np.linspace(5.0, 9.5, 20)])
            y_track = np.concatenate([np.linspace(start_y, 2.0, 20), np.linspace(2.0, 1.2, 20)])
        particle_paths.append((x_track, y_track))
        
    scat = ax.scatter([], [], c=[], s=80, zorder=5)
    
    def update(frame):
        x_display, y_display, colors = [], [], []
        for i in range(num_particles):
            x_display.append(particle_paths[i][0][frame])
            y_display.append(particle_paths[i][1][frame])
            colors.append('#2ca25f' if i < absorbed_count else '#de2d26')
        scat.set_offsets(np.c_[x_display, y_display])
        scat.set_color(colors)
        return scat,

    ani = animation.FuncAnimation(fig, update, frames=frames_count, interval=100, blit=True)
    gif_path = "absorption_flow.gif"
    ani.save(gif_path, writer='pillow', fps=10)
    plt.close(fig)
    return gif_path

with st.spinner("Generating animation track..."):
    gif_file = generate_absorption_animation(ca_intake, ca_excrete)
    with open(gif_file, "rb") as f:
        data_bytes = f.read()
        b64_encoded = base64.b64encode(data_bytes).decode()
        st.markdown(f'<img src="data:image/gif;base64,{b64_encoded}" width="100%">', unsafe_allow_html=True)import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import base64

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

# --- USER SIDEBAR INPUTS ---
st.sidebar.header("🔬 Input Herd & Feed Metrics")
days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)

# --- CALCULATION PART & CORE PREDICTOR VARIABLES ---
st.markdown("---")
st.subheader("🐄 Holstein Cow Calcium Apparent Absorption Model")

col_input1, col_input2 = st.columns(2)
with col_input1:
    ca_intake = st.number_input("Calcium Intake in Feed (X, grams/day):", min_value=1.0, value=100.0, step=5.0)
with col_input2:
    ca_excrete = st.number_input("Calcium Excreted in Feces (grams/day):", min_value=0.0, value=60.0, step=5.0)

# Calculating standard manual total-tract absorption metric
ca_absorbed = ca_intake - ca_excrete
if ca_intake > 0:
    apparent_absorption_pct = (ca_absorbed / ca_intake) * 100
else:
    apparent_absorption_pct = 0.0

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium (X)", value=f"{ca_intake} g")
with col_res2:
    st.metric(label="💩 Excreted Calcium", value=f"{ca_excrete} g", delta=f"-{ca_excrete} g", delta_color="inverse")
with col_res3:
    st.metric(label="✅ Apparent Absorbed", value=f"{ca_absorbed} g")

# --- EXPERIMENTAL MODEL COEFFICIENTS (UPDATED FROM USER IMAGE) ---
# Equation: Y = 62.47 + (-0.2611 * X) + (0.000561 * X^2) + (-0.0202 * DIM)
intercept = 62.47
beta_x = -0.2611
beta_x_sq = 0.000561
beta_dim = -0.0202

predicted_absorption = (
    intercept + 
    (beta_x * ca_intake) + 
    (beta_x_sq * (ca_intake ** 2)) + 
    (beta_dim * days_in_milk)
)

# Apply physiological boundary constraints (0% to 100%)
predicted_absorption = max(0.0, min(100.0, predicted_absorption))

# --- RENDERING THE MODEL OUTCOME METRIC PANEL ---
st.markdown("---")
st.subheader("🔮 Model Prediction Result (Y)")
st.metric(label="Predicted Apparent Calcium Absorption Efficiency (Y)", value=f"{predicted_absorption:.2f} %")

# Displaying updated specific LaTeX formatting representation for thesis panel clarity
st.markdown("### 🧮 Quadratic Model Regression Formula")
st.latex(r"Y = 62.47 + (-0.2611 \times X) + (0.000561 \times X^2) + (-0.0202 \times \text{DIM})")
st.info(f"**Live Equation Process:** 62.47 + (-0.2611 × {ca_intake}) + (0.000561 × {ca_intake}²) + (-0.0202 × {days_in_milk}) = **{predicted_absorption:.2f}%**")

if predicted_absorption < 25.0:
    st.warning("⚠️ **Low Predicted Efficiency:** High risk of mineral pass-through and environmental fecal excretion.")
elif predicted_absorption > 55.0:
    st.info("📈 **High Predicted Activity:** Intestinal active transport channels upregulated (high metabolic draw).")
else:
    st.success("✅ **Normal Range:** Physiological baseline absorption levels maintained.")

# --- DYNAMIC FLOWCHART LAYOUT CANVAS ---
st.markdown("---")
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-around; align-items: center; background-color: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #eaeaea; margin-top: 15px;">
        <div style="text-align: center; background-color: #2b7bba; color: white; padding: 12px; border-radius: 6px; width: 25%;">
            <p style="margin: 0; font-weight: bold;">1. Feed Intake (X)</p>
            <p style="font-size: 18px; margin: 3px 0 0 0;">{ca_intake} g</p>
        </div>
        <div style="font-size: 24px; color: #2b7bba;">➡️</div>
        <div style="text-align: center; background-color: #ffffff; color: #333; padding: 12px; border-radius: 6px; width: 30%; border: 2px solid #555;">
            <p style="margin: 0; font-weight: bold;">🐄 Holstein Body</p>
            <p style="font-size: 14px; margin: 3px 0 0 0;"><b>Observed Efficiency:</b> {apparent_absorption_pct:.1f}%</p>
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

# --- ANIMATION MAKER SECTION ---
st.markdown("---")
st.subheader("🎬 Animated Apparent Absorption Flow Model")

def generate_absorption_animation(intake_val, excrete_val):
    fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    ax.add_patch(plt.Rectangle((3.8, 1.5), 2.4, 2, fill=True, color='#f0f0f0', ec='#333333', lw=2))
    ax.text(5.0, 2.5, "🐄 Holstein Body\n(Retention)", ha='center', va='center', weight='bold', color='#222')
    
    num_particles = 15
    frames_count = 40
    absorbed_count = max(1, int(num_particles * ((intake_val - excrete_val) / intake_val)))
    
    particle_paths = []
    for i in range(num_particles):
        start_y = np.random.uniform(2.2, 2.8)
        if i < absorbed_count:
            x_track = np.linspace(0.5, 5.0, frames_count)
            y_track = np.linspace(start_y, 2.5, frames_count)
        else:
            x_track = np.concatenate([np.linspace(0.5, 5.0, 20), np.linspace(5.0, 9.5, 20)])
            y_track = np.concatenate([np.linspace(start_y, 2.0, 20), np.linspace(2.0, 1.2, 20)])
        particle_paths.append((x_track, y_track))
        
    scat = ax.scatter([], [], c=[], s=80, zorder=5)
    
    def update(frame):
        x_display, y_display, colors = [], [], []
        for i in range(num_particles):
            x_display.append(particle_paths[i][frame])
            y_display.append(particle_paths[i][frame])
            colors.append('#2ca25f' if i < absorbed_count else '#de2d26')
        scat.set_offsets(np.c_[x_display, y_display])
        scat.set_color(colors)
        return scat,

    ani = animation.FuncAnimation(fig, update, frames=frames_count, interval=100, blit=True)
    gif_path = "absorption_flow.gif"
    ani.save(gif_path, writer='pillow', fps=10)
    plt.close(fig)
    return gif_path

with st.spinner("Generating animation track..."):
    gif_file = generate_absorption_animation(ca_intake, ca_excrete)
    with open(gif_file, "rb") as f:
        data_bytes = f.read()
        b64_encoded = base64.b64encode(data_bytes).decode()
        st.markdown(f'<img src="data:image/gif;base64,{b64_encoded}" width="100%">', unsafe_allow_html=True)
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

# --- USER SIDEBAR INPUTS ---
st.sidebar.header("🔬 Input Herd & Feed Metrics")
days_in_milk = st.sidebar.slider("Days in Milk (DIM)", 1, 300, 100, 5)

# --- CALCULATION PART & CORE PREDICTOR VARIABLES ---
st.markdown("---")
st.subheader("🐄 Holstein Cow Calcium Apparent Absorption Model")

col_input1, col_input2 = st.columns(2)
with col_input1:
    ca_intake = st.number_input("Calcium Intake in Feed (X, grams/day):", min_value=1.0, value=100.0, step=5.0)
with col_input2:
    ca_excrete = st.number_input("Calcium Excreted in Feces (grams/day):", min_value=0.0, value=60.0, step=5.0)

# Calculating standard manual total-tract absorption metric
ca_absorbed = ca_intake - ca_excrete
if ca_intake > 0:
    apparent_absorption_pct = (ca_absorbed / ca_intake) * 100
else:
    apparent_absorption_pct = 0.0

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric(label="📥 Intake Calcium (X)", value=f"{ca_intake} g")
with col_res2:
    st.metric(label="💩 Excreted Calcium", value=f"{ca_excrete} g", delta=f"-{ca_excrete} g", delta_color="inverse")
with col_res3:
    st.metric(label="✅ Apparent Absorbed", value=f"{ca_absorbed} g")

# --- EXPERIMENTAL MODEL COEFFICIENTS (UPDATED FROM USER IMAGE) ---
# Equation: Y = 62.47 + (-0.2611 * X) + (0.000561 * X^2) + (-0.0202 * DIM)
intercept = 62.47
beta_x = -0.2611
beta_x_sq = 0.000561
beta_dim = -0.0202

predicted_absorption = (
    intercept + 
    (beta_x * ca_intake) + 
    (beta_x_sq * (ca_intake ** 2)) + 
    (beta_dim * days_in_milk)
)

# Apply physiological boundary constraints (0% to 100%)
predicted_absorption = max(0.0, min(100.0, predicted_absorption))

# --- RENDERING THE MODEL OUTCOME METRIC PANEL ---
st.markdown("---")
st.subheader("🔮 Model Prediction Result (Y)")
st.metric(label="Predicted Apparent Calcium Absorption Efficiency (Y)", value=f"{predicted_absorption:.2f} %")

# Displaying updated specific LaTeX formatting representation for thesis panel clarity
st.markdown("### 🧮 Quadratic Model Regression Formula")
st.latex(r"Y = 62.47 + (-0.2611 \times X) + (0.000561 \times X^2) + (-0.0202 \times \text{DIM})")
st.info(f"**Live Equation Process:** 62.47 + (-0.2611 × {ca_intake}) + (0.000561 × {ca_intake}²) + (-0.0202 × {days_in_milk}) = **{predicted_absorption:.2f}%**")

if predicted_absorption < 25.0:
    st.warning("⚠️ **Low Predicted Efficiency:** High risk of mineral pass-through and environmental fecal excretion.")
elif predicted_absorption > 55.0:
    st.info("📈 **High Predicted Activity:** Intestinal active transport channels upregulated (high metabolic draw).")
else:
    st.success("✅ **Normal Range:** Physiological baseline absorption levels maintained.")

# --- HIGH UTILITY STABLE NATIVE ANIMATED FLOW MODEL ---
st.markdown("---")
st.subheader("🎬 Animated Apparent Absorption Flow Model")
st.markdown("This live animation loops custom CSS flow waves across pipelines to visualize the real-time metabolic partition difference between your Intake feed inputs and fecal outputs.")

# Pure CSS Keyframes injection to move molecules cleanly inside any browser container safely
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
            <p style="font-size: 20px; margin: 5px 0 0 0; font-weight: bold;">{ca_intake} g</p>
        </div>
        <div class="animated-arrow">➡️  ➡️</div>
        <div style="text-align: center; background-color: #ffffff; color: #333; padding: 15px; border-radius: 8px; width: 32%; border: 2px solid #555; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">🐄 Holstein Body</p>
            <p style="font-size: 15px; margin: 5px 0 0 0; color: #2ca25f;"><b>Observed Abs:</b> {apparent_absorption_pct:.1f}%</p>
            <p style="font-size: 13px; margin: 2px 0 0 0; color: #666;">Retained: {ca_absorbed:.1f} g/day</p>
        </div>
        <div class="animated-arrow-waste">➡️  ➡️</div>
        <div style="text-align: center; background-color: #d9534f; color: white; padding: 15px; border-radius: 8px; width: 25%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin: 0; font-weight: bold; font-size: 14px;">2. Fecal Waste</p>
            <p style="font-size: 20px; margin: 5px 0 0 0; font-weight: bold;">{ca_excrete} g</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

        

