app_py_content = """
import streamlit as st
import pandas as pd
import pickle

# ==================================
# LOAD MODEL
# ==================================
with open('linear_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Prediksi Harga Rumah - Baby Blue PRO Edition",
    layout="wide"
)

# ==================================
# BABY BLUE PRO CSS (ANIMATED)
# ==================================
st.markdown(\"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800;900&display=swap');

html, body, .stApp {
    font-family: 'Poppins', sans-serif;

    /* BABY BLUE BACKGROUND + SHIMMER */
    background: linear-gradient(135deg, #dff1ff 0%, #c7e7ff 35%, #b7e1ff 65%, #a3d8ff 100%);
    background-size: 400% 400%;
    animation: bgMove 18s ease infinite;
}

@keyframes bgMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* TITLE SHINE EFFECT */
.main-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #1a6fff, #4ab4ff, #9be4ff, #4ab4ff, #1a6fff);
    background-size: 300%;
    -webkit-background-clip: text;
    color: transparent;
    animation: shine 6s infinite linear;
}

@keyframes shine {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

.sub-title {
    font-size: 20px;
    text-align: center;
    opacity: 0.8;
    margin-bottom: 25px;
    animation: fadeIn 1.5s ease;
}

/* Input Card Animation */
.glass-card {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 25px;
    border: 2px solid rgba(255,255,255,0.7);
    box-shadow: 0 8px 26px rgba(0,0,0,0.15);

    animation: fadeInUp 1.3s ease;
    transition: all 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 35px rgba(0,0,0,0.25);
}

/* Input Box Glow */
input[type=number], select {
    border-radius: 12px !important;
    border: 2px solid #a4d9ff !important;
    padding: 10px !important;
    background: rgba(255,255,255,0.8) !important;
    transition: all 0.25s ease !important;
}

input[type=number]:hover, select:hover {
    transform: scale(1.015);
    border-color: #5ec6ff !important;
}

input[type=number]:focus, select:focus {
    border-color: #0099ff !important;
    box-shadow: 0 0 10px rgba(0,153,255,0.45);
}

/* Prediction Card Floating + Glow */
.pred-card {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0099ff, #33bbff);
    color: white;
    font-size: 32px;
    font-weight: 900;
    text-align: center;

    animation: float 4s ease-in-out infinite, glow 2s infinite alternate ease-in-out;
    box-shadow: 0 0 25px rgba(0,153,255,0.6);
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

@keyframes glow {
    0% { box-shadow: 0 0 14px rgba(0,153,255,0.4); }
    100% { box-shadow: 0 0 28px rgba(0,200,255,0.8); }
}

/* Predict Button: Ripple + Glow */
.stButton>button {
    background: linear-gradient(135deg, #0099ff, #3ac7ff);
    color: white;
    padding: 14px 30px;
    border-radius: 14px;
    border: none;
    font-size: 22px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    transition: 0.2s ease;
    position: relative;
    overflow: hidden;
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 10px 28px rgba(0,153,255,0.55);
}

.stButton>button:active::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.4);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: ripple 0.6s forwards;
}
@keyframes ripple {
    0% { opacity: 0.6; transform: translate(-50%, -50%) scale(0.1); }
    100% { opacity: 0; transform: translate(-50%, -50%) scale(1.5); }
}

/* Fade animations */
@keyframes fadeInUp { from {opacity:0; transform: translateY(20px);} to {opacity:1; transform: translateY(0);} }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }

</style>
\""", unsafe_allow_html=True)


# ==================================
# HEADER
# ==================================
st.markdown('<div class="main-title">🏠 Prediksi Harga Rumah</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Baby Blue PRO • Animasi Premium • UI Level Aesthetic</div>', unsafe_allow_html=True)


# ==================================
# NEIGHBORHOOD LIST (Translated)
# ==================================
neigh_map = {
    'NAmes': 'North Ames','CollgCr': 'College Creek','OldTown': 'Old Town',
    'Edwards': 'Edwards','Somerst': 'Somerset','Gilbert': 'Gilbert',
    'NridgHt': 'Northridge Heights','Sawyer': 'Sawyer','NWAmes': 'Northwest Ames',
    'SawyerW': 'Sawyer West','BrkSide': 'Brookside','Mitchel': 'Mitchell',
    'Crawfor': 'Crawford','IDOTRR': 'Iowa DOT & Rel','Timber': 'Timberland',
    'NoRidge': 'Northridge','StoneBr': 'Stone Brook','SWISU': 'SW of ISU',
    'ClearCr': 'Clear Creek','MeadowV': 'Meadow Village','Blmngtn': 'Bloomington Heights',
    'BrDale': 'Briardale','NPkVill': 'Northpark Villa','Veenker': 'Veenker',
    'Blueste': 'Bluestem','Greens': 'Greens','GrnHill': 'Green Hill','Landmrk': 'Landmark'
}

neigh_keys = list(neigh_map.keys())

# ==================================
# INPUT BOXES – ANIMATED
# ==================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("⚙️ Parameter Rumah (Form Premium)")

col1, col2, col3 = st.columns(3)

with col1:
    overall_qual = st.number_input("🏅 Kualitas Rumah", 1, 10, 5)
    garage_cars = st.number_input("🚗 Kapasitas Garasi", 0, 4, 1)
    full_bath = st.number_input("🛁 Jumlah Kamar Mandi", 0, 4, 1)

with col2:
    gr_liv_area = st.number_input("📏 Luas Area Tinggal", 300, 4000, 1500)
    garage_area = st.number_input("📐 Luas Garasi (SF)", 0, 1200, 300)
    tot_rooms = st.number_input("🚪 Total Ruangan", 2, 18, 6)

with col3:
    total_bsmt_sf = st.number_input("⬇️ Total Basement (SF)", 0, 3000, 800)
    first_flr_sf = st.number_input("🏠 Luas Lantai 1 (SF)", 200, 3000, 1000)
    month_name = st.selectbox("📅 Bulan Penjualan",
        ['January','February','March','April','May','June',
         'July','August','September','October','November','December'])

neighborhood = st.selectbox("📍 Lingkungan Perumahan", neigh_keys, format_func=lambda x: neigh_map[x])

st.markdown("</div>", unsafe_allow_html=True)


# ==================================
# PROCESS INPUT
# ==================================
df_input = pd.DataFrame({
    'Overall Qual': [overall_qual],
    'Gr Liv Area': [gr_liv_area],
    'Garage Cars': [garage_cars],
    'Garage Area': [garage_area],
    'Total Bsmt SF': [total_bsmt_sf],
    '1st Flr SF': [first_flr_sf],
    'Full Bath': [full_bath],
    'TotRms AbvGrd': [tot_rooms],
    'month_name': [month_name],
    'Neighborhood': [neighborhood]
})

# ==================================
# OHE
# ==================================
training_columns = list(model.feature_names_in_)
final_input = pd.DataFrame(columns=training_columns)
final_input.loc[0] = 0

for col in ['Overall Qual','Gr Liv Area','Garage Cars','Garage Area','Total Bsmt SF','1st Flr SF','Full Bath','TotRms AbvGrd']:
    final_input.loc[0, col] = df_input[col][0]

for col in training_columns:
    if col.startswith("month_name_"):
        final_input.loc[0, col] = col == f"month_name_{df_input['month_name'][0]}"
    if col.startswith("Neighborhood_"):
        final_input.loc[0, col] = col == f"Neighborhood_{df_input['Neighborhood'][0]}"

# ==================================
# PREDICTION
# ==================================
st.header("🔮 Hasil Prediksi")

if st.button("✨ Hitung Prediksi Harga"):
    pred = model.predict(final_input)[0]
    st.markdown(
        f"<div class='pred-card'>💙 Harga Rumah Diprediksi:<br><b>${pred:,.2f}</b></div>",
        unsafe_allow_html=True
    )
"""

with open('app.py', 'w') as f:
    f.write(app_py_content)

print("app.py created successfully.")
