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
    page_title="Prediksi Harga Rumah Ames",
    layout="wide",
)

# =====================
# LEVEL MAX CSS — GLASS, ANIMATION, GRADIENT, DARK/LIGHT MODE
# =====================
st.markdown(\"""
<style>

:root {
    --main-gradient: linear-gradient(135deg, #0f9bff, #6dd5fa);
    --card-bg: rgba(255, 255, 255, 0.55);
}

html, body, .stApp {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    color: white;
}

@media (prefers-color-scheme: light) {
    html, body, .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #eef2f7 100%);
        color: black;
    }
}

/* Glass Card */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

/* Title Animation */
.main-title {
    font-size: 46px;
    font-weight: 900;
    text-align: center;
    background: var(--main-gradient);
    -webkit-background-clip: text;
    color: transparent;
    animation: fadeIn 1.3s ease-in-out;
}

/* Sub Title */
.sub-title {
    font-size: 20px;
    text-align: center;
    opacity: 0.85;
    margin-bottom: 28px;
    animation: fadeIn 1.8s ease-in-out;
}

/* Prediction Card Glow Animation */
.pred-card {
    padding: 30px;
    border-radius: 20px;
    background: var(--main-gradient);
    color: white;
    font-size: 30px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0 8px 25px rgba(15, 155, 255, 0.45);
    animation: glow 2s infinite alternate ease-in-out, fadeIn 1.2s ease-out;
}

@keyframes glow {
    0% { box-shadow: 0px 0px 14px #0f9bff; }
    100% { box-shadow: 0px 0px 28px #6dd5fa; }
}

/* Predict Button Glow */
.stButton>button {
    background: var(--main-gradient);
    color: white;
    padding: 12px 25px;
    border-radius: 12px;
    border: none;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 5px 18px rgba(0,0,0,0.25);
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.07);
    box-shadow: 0 6px 22px rgba(0,0,0,0.3);
}

/* Fade In Animations */
@keyframes fadeIn {
    from { opacity:0; transform: translateY(5px); }
    to { opacity:1; transform: translateY(0); }
}

/* Dataframe Table Styling */
.dataframe th {
    background: rgba(255,255,255,0.2) !important;
}
.dataframe td {
    background: rgba(255,255,255,0.05) !important;
}

</style>
\""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="main-title">🏠 Prediksi Harga Rumah – Ames Housing</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Aplikasi prediksi harga rumah dengan tampilan premium.</div>', unsafe_allow_html=True)


# =====================
# NEIGHBORHOOD MAPPING
# =====================
neigh_map = {
    'NAmes': 'North Ames',
    'CollgCr': 'College Creek',
    'OldTown': 'Old Town',
    'Edwards': 'Edwards',
    'Somerst': 'Somerset',
    'Gilbert': 'Gilbert',
    'NridgHt': 'Northridge Heights',
    'Sawyer': 'Sawyer',
    'NWAmes': 'Northwest Ames',
    'SawyerW': 'Sawyer West',
    'BrkSide': 'Brookside',
    'Mitchel': 'Mitchell',
    'Crawfor': 'Crawford',
    'IDOTRR': 'Iowa DOT and Railroad',
    'Timber': 'Timberland',
    'NoRidge': 'Northridge',
    'StoneBr': 'Stone Brook',
    'SWISU': 'South & West of ISU',
    'ClearCr': 'Clear Creek',
    'MeadowV': 'Meadow Village',
    'Blmngtn': 'Bloomington Heights',
    'BrDale': 'Briardale',
    'NPkVill': 'Northpark Villa',
    'Veenker': 'Veenker',
    'Blueste': 'Bluestem',
    'Greens': 'Greens',
    'GrnHill': 'Green Hill',
    'Landmrk': 'Landmark'
}

neigh_list = list(neigh_map.keys())


# =====================
# SIDEBAR (Input Panel)
# =====================
st.sidebar.header("⚙️ Input Parameter")

def user_input_features():
    overall_qual = st.sidebar.slider('🏅 Overall Quality', 1, 10, 5)
    gr_liv_area = st.sidebar.slider('📏 Gr Liv Area', 300, 4000, 1500)
    garage_cars = st.sidebar.slider('🚗 Garage Cars', 0, 4, 1)
    garage_area = st.sidebar.slider('📐 Garage Area', 0, 1200, 300)
    total_bsmt_sf = st.sidebar.slider('⬇️ Total Bsmt SF', 0, 3000, 800)
    first_flr_sf = st.sidebar.slider('🏠 1st Flr SF', 200, 3000, 1000)
    full_bath = st.sidebar.slider('🛁 Full Bath', 0, 4, 1)
    tot_rooms = st.sidebar.slider('🚪 TotRms AbvGrd', 2, 14, 6)

    month_name = st.sidebar.selectbox(
        '📅 Month Sold',
        ['January','February','March','April','May','June',
         'July','August','September','October','November','December']
    )

    neighborhood = st.sidebar.selectbox(
        '📍 Neighborhood',
        neigh_list,
        format_func=lambda x: neigh_map[x]
    )

    return pd.DataFrame({
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

df_input = user_input_features()

# =====================
# SHOW INPUT (Glass Card)
# =====================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📋 Input Pengguna")
st.dataframe(df_input, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# =====================
# ONE-HOT ENCODING MATCH
# =====================
training_columns = list(model.feature_names_in_)
final_input = pd.DataFrame(columns=training_columns)
final_input.loc[0] = 0

num_cols = ['Overall Qual','Gr Liv Area','Garage Cars','Garage Area',
            'Total Bsmt SF','1st Flr SF','Full Bath','TotRms AbvGrd']

for col in num_cols:
    final_input.loc[0, col] = df_input[col][0]

for col in training_columns:
    if col.startswith('month_name_'):
        final_input.loc[0, col] = (col == f"month_name_{df_input['month_name'][0]}")
    if col.startswith('Neighborhood_'):
        final_input.loc[0, col] = (col == f"Neighborhood_{df_input['Neighborhood'][0]}")

# =====================
# PREDICTION
# =====================
st.markdown("<hr>", unsafe_allow_html=True)
st.header("🔮 Prediksi Harga Rumah")

if st.button("💰 Prediksi Harga"):
    pred = model.predict(final_input)[0]
    st.markdown(
        f"<div class='pred-card'>💵 Harga Prediksi:<br><b>${pred:,.2f}</b></div>",
        unsafe_allow_html=True
    )
"""

with open('app.py', 'w') as f:
    f.write(app_py_content)

print("app.py created successfully.")
