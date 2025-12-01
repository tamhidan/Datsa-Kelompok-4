app_py_content = """
import streamlit as st
import pandas as pd
import pickle

# =====================
# LOAD MODEL
# =====================
with open('linear_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Prediksi Harga Rumah - Baby Blue Indonesian Edition",
    layout="wide"
)

# =====================
# BABY BLUE UI CSS
# =====================
st.markdown(\"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800;900&display=swap');

html, body, .stApp {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #dff1ff 0%, #c7e7ff 40%, #b7e1ff 70%, #a3d8ff 100%);
    background-attachment: fixed;
    color: #0f1c2d !important;
}

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.50);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 22px 30px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.4);
}

/* Header Title */
.main-title {
    font-size: 44px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #0088ff, #00b7ff, #57d1ff);
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 5px;
}
.sub-title {
    font-size: 18px;
    text-align: center;
    opacity: 0.75;
    margin-bottom: 25px;
}

/* Prediction Card */
.pred-card {
    padding: 32px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0099ff, #33bbff);
    color: white;
    font-size: 30px;
    font-weight: 900;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,153,255,0.7);
    animation: glow 2s infinite alternate ease-in-out;
}

@keyframes glow {
    0% { box-shadow: 0 0 14px rgba(0,153,255,0.4); }
    100% { box-shadow: 0 0 28px rgba(0,200,255,0.8); }
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #0099ff, #3ac7ff);
    color: white;
    padding: 14px 30px;
    border-radius: 12px;
    border: none;
    font-size: 20px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    transition: 0.25s ease;
}
.stButton>button:hover {
    transform: scale(1.06);
    box-shadow: 0 8px 25px rgba(0,153,255,0.55);
}

/* Number input styling */
input[type=number] {
    border-radius: 10px !important;
    border: 2px solid #a4d9ff !important;
    padding: 8px !important;
    background: rgba(255,255,255,0.7) !important;
}

</style>
\""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="main-title">🏠 Prediksi Harga Rumah</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Masukkan parameter rumah di bawah untuk memprediksi harga.</div>', unsafe_allow_html=True)


# =====================
# NEIGHBORHOOD (LIngkungan)
# =====================
neigh_map = {
    'NAmes': 'North Ames','CollgCr': 'College Creek','OldTown': 'Old Town',
    'Edwards': 'Edwards','Somerst': 'Somerset','Gilbert': 'Gilbert',
    'NridgHt': 'Northridge Heights','Sawyer': 'Sawyer','NWAmes': 'Northwest Ames',
    'SawyerW': 'Sawyer West','BrkSide': 'Brookside','Mitchel': 'Mitchell',
    'Crawfor': 'Crawford','IDOTRR': 'Iowa DOT dan Railroad','Timber': 'Timberland',
    'NoRidge': 'Northridge','StoneBr': 'Stone Brook','SWISU': 'SW of ISU',
    'ClearCr': 'Clear Creek','MeadowV': 'Meadow Village','Blmngtn': 'Bloomington Heights',
    'BrDale': 'Briardale','NPkVill': 'Northpark Villa','Veenker': 'Veenker',
    'Blueste': 'Bluestem','Greens': 'Greens','GrnHill': 'Green Hill','Landmrk': 'Landmark'
}
neigh_keys = list(neigh_map.keys())

# =====================
# INPUT FORM (BOXES) — INDONESIAN LABELS
# =====================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("⚙️ Input Parameter Rumah (Formulir)")

col1, col2, col3 = st.columns(3)

with col1:
    overall_qual = st.number_input("🏅 Kualitas Rumah", 1, 10, 5)
    garage_cars = st.number_input("🚗 Kapasitas Garasi", 0, 4, 1)
    full_bath = st.number_input("🛁 Jumlah Kamar Mandi", 0, 4, 1)

with col2:
    gr_liv_area = st.number_input("📏 Luas Area Tinggal (Gr Liv Area)", 300, 4000, 1500)
    garage_area = st.number_input("📐 Luas Garasi", 0, 1200, 300)
    tot_rooms = st.number_input("🚪 Total Ruangan", 2, 14, 6)

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
# ENCODING
# ==================================
training_columns = list(model.feature_names_in_)
final_input = pd.DataFrame(columns=training_columns)
final_input.loc[0] = 0

num_cols = ['Overall Qual','Gr Liv Area','Garage Cars','Garage Area',
            'Total Bsmt SF','1st Flr SF','Full Bath','TotRms AbvGrd']

for col in num_cols:
    final_input.loc[0, col] = df_input[col][0]

for col in training_columns:
    if col.startswith("month_name_"):
        final_input.loc[0, col] = (col == f"month_name_{df_input['month_name'][0]}")
    if col.startswith("Neighborhood_"):
        final_input.loc[0, col] = (col == f"Neighborhood_{df_input['Neighborhood'][0]}")

# ==================================
# PREDICTION
# ==================================
st.header("🔮 Hasil Prediksi Harga Rumah")

if st.button("🔵 Prediksi Harga"):
    pred = model.predict(final_input)[0]
    st.markdown(
        f"<div class='pred-card'>Perkiraan Harga Rumah:<br><b>${pred:,.2f}</b></div>",
        unsafe_allow_html=True
    )
"""

with open('app.py', 'w') as f:
    f.write(app_py_content)

print("app.py created successfully.")
