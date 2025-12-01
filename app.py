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
    page_title="Prediksi Harga Rumah Ames - Ultra Edition",
    layout="wide"
)

# ==================================
# ULTRA LEVEL CSS (PREMIUM PURPLE)
# ==================================
st.markdown(\"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

html, body, .stApp {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #6a00f4 0%, #8a15ff 35%, #b23fff 70%, #fbd3ff 100%);
    background-attachment: fixed;
    color: white !important;
}

/* Floating glass sidebar */
section[data-testid="stSidebar"] > div:first-child {
    background: rgba(255, 255, 255, 0.20);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 20px;
    padding-top: 40px;
    box-shadow: 0 0 25px rgba(255,255,255,0.2);
}

/* Main title with floating glow */
.main-title {
    font-size: 50px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #ffffff, #f3d9ff, #fdf5ff);
    -webkit-background-clip: text;
    color: transparent;
    filter: drop-shadow(0px 0px 10px rgba(255, 255, 255, .5));
    animation: fadeInDown 1.3s ease;
}

/* Subtitle */
.sub-title {
    font-size: 22px;
    text-align: center;
    opacity: 0.92;
    margin-bottom: 35px;
    animation: fadeInUp 1.7s ease;
}

/* GLASS CARD ULTRA */
.glass-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 22px;
    padding: 28px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.35);
    animation: fadeIn 1.5s ease;
    border: 1px solid rgba(255,255,255,0.3);
}

/* ULTRA PREDICTION CARD */
.pred-card {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #7b00ff, #bc3bff, #ff9bff);
    color: white;
    font-size: 34px;
    font-weight: 900;
    text-align: center;
    animation: neonGlow 2s infinite alternate ease-in-out, fadeIn 1.3s ease-out;
    box-shadow: 0 0 35px rgba(255, 180, 255, 0.6);
}

@keyframes neonGlow {
    0% { box-shadow: 0 0 15px #ff71ff; }
    100% { box-shadow: 0 0 35px #ffaaff; }
}

/* ULTRA BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #7b00ff, #bc3bff);
    color: white;
    padding: 15px 30px;
    border-radius: 15px;
    border: none;
    font-size: 20px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s ease;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 10px 30px rgba(255, 170, 255, 0.55);
}

/* Fade Animations */
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }
@keyframes fadeInDown { from {opacity:0; transform:translateY(-20px);} to {opacity:1; transform:translateY(0);} }
@keyframes fadeInUp { from {opacity:0; transform:translateY(20px);} to {opacity:1; transform:translateY(0);} }

/* Table */
.dataframe td, .dataframe th {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}
</style>
\""", unsafe_allow_html=True)

# ==================================
# HEADER
# ==================================
st.markdown('<div class="main-title">💜 Prediksi Harga Rumah – Ultra Edition</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Tampilan mewah, prediksi akurat, model premium.</div>', unsafe_allow_html=True)


# ==================================
# NEIGHBORHOOD
# ==================================
neigh_map = {
    'NAmes': 'North Ames','CollgCr': 'College Creek','OldTown': 'Old Town',
    'Edwards': 'Edwards','Somerst': 'Somerset','Gilbert': 'Gilbert',
    'NridgHt': 'Northridge Heights','Sawyer': 'Sawyer','NWAmes': 'Northwest Ames',
    'SawyerW': 'Sawyer West','BrkSide': 'Brookside','Mitchel': 'Mitchell',
    'Crawfor': 'Crawford','IDOTRR': 'Iowa DOT and Railroad','Timber': 'Timberland',
    'NoRidge': 'Northridge','StoneBr': 'Stone Brook','SWISU': 'South & West of ISU',
    'ClearCr': 'Clear Creek','MeadowV': 'Meadow Village','Blmngtn': 'Bloomington Heights',
    'BrDale': 'Briardale','NPkVill': 'Northpark Villa','Veenker': 'Veenker',
    'Blueste': 'Bluestem','Greens': 'Greens','GrnHill': 'Green Hill','Landmrk': 'Landmark'
}
neigh_keys = list(neigh_map.keys())


# ==================================
# INPUT SECTION (Ultra Glass Card)
# ==================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("⚙️ Input Parameter")

col1, col2, col3 = st.columns(3)

with col1:
    overall_qual = st.slider("🏅 Overall Quality", 1, 10, 5)
    garage_cars = st.slider("🚗 Garage Cars", 0, 4, 1)
    full_bath = st.slider("🛁 Full Bath", 0, 4, 1)

with col2:
    gr_liv_area = st.slider("📏 Gr Liv Area", 300, 4000, 1500)
    garage_area = st.slider("📐 Garage Area", 0, 1200, 300)
    tot_rooms = st.slider("🚪 TotRms AbvGrd", 2, 14, 6)

with col3:
    total_bsmt_sf = st.slider("⬇️ Total Bsmt SF", 0, 3000, 800)
    first_flr_sf = st.slider("🏠 1st Flr SF", 200, 3000, 1000)
    month_name = st.selectbox("📅 Month Sold", 
        ['January','February','March','April','May','June','July','August','September','October','November','December'])

neighborhood = st.selectbox("📍 Neighborhood", neigh_keys, format_func=lambda x: neigh_map[x])

st.markdown("</div>", unsafe_allow_html=True)

# convert to df
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
# SHOW INPUT TABLE
# ==================================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📋 Input Pengguna")
st.dataframe(df_input, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ==================================
# ENCODING & PREPARATION
# ==================================
training_columns = list(model.feature_names_in_)
final_input = pd.DataFrame(columns=training_columns)
final_input.loc[0] = 0

numeric_cols = ['Overall Qual','Gr Liv Area','Garage Cars','Garage Area',
                'Total Bsmt SF','1st Flr SF','Full Bath','TotRms AbvGrd']

for col in numeric_cols:
    final_input.loc[0, col] = df_input[col][0]

for col in training_columns:
    if col.startswith("month_name_"):
        final_input.loc[0, col] = (col == f"month_name_{df_input['month_name'][0]}")
    if col.startswith("Neighborhood_"):
        final_input.loc[0, col] = (col == f"Neighborhood_{df_input['Neighborhood'][0]}")

# ==================================
# PREDIKSI
# ==================================
st.header("🔮 Prediksi Harga Rumah")

if st.button("💜 Prediksi Harga Sekarang!"):
    pred = model.predict(final_input)[0]
    st.markdown(
        f"<div class='pred-card'>💎 Harga Rumah Diprediksi:<br><b>${pred:,.2f}</b></div>",
        unsafe_allow_html=True
    )
"""

with open('app.py', 'w') as f:
    f.write(app_py_content)

print("app.py created successfully.")
