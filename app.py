
import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open('linear_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title('Prediksi Harga Rumah - Ames Housing')
st.write('Masukkan fitur rumah untuk memprediksi harga rumah.')

# Sidebar input
st.sidebar.header('Input Parameter')

def user_input_features():

    overall_qual = st.sidebar.slider('Kualitas Rumah (Overall Qual)', 1, 10, 5)
    gr_liv_area = st.sidebar.slider('Luas Area Tinggal (Gr Liv Area)', 300, 4000, 1500)
    garage_cars = st.sidebar.slider('Kapasitas Garasi (Garage Cars)', 0, 4, 1)
    garage_area = st.sidebar.slider('Luas Garasi (Garage Area)', 0, 1200, 300)
    total_bsmt_sf = st.sidebar.slider('Total Basement (Total Bsmt SF)', 0, 3000, 800)
    first_flr_sf = st.sidebar.slider('Luas Lantai 1 (1st Flr SF)', 200, 3000, 1000)
    full_bath = st.sidebar.slider('Jumlah Kamar Mandi (Full Bath)', 0, 4, 1)
    tot_rooms = st.sidebar.slider('Total Ruangan (TotRms AbvGrd)', 2, 14, 6)

    month_name = st.sidebar.selectbox('Bulan Terjual', 
                    ['January','February','March','April','May','June',
                     'July','August','September','October','November','December'])

    neighborhood = st.sidebar.selectbox('Neighborhood', [
        'NAmes','CollgCr','OldTown','Edwards','Somerst','Gilbert','NridgHt','Sawyer',
        'NWAmes','SawyerW','BrkSide','Mitchel','Crawfor','IDOTRR','Timber','NoRidge',
        'StoneBr','SWISU','ClearCr','MeadowV','Blmngtn','BrDale','NPkVill','Veenker',
        'Blueste','Greens','GrnHill','Landmrk'
    ])

    data = {
        'Overall Qual': overall_qual,
        'Gr Liv Area': gr_liv_area,
        'Garage Cars': garage_cars,
        'Garage Area': garage_area,
        'Total Bsmt SF': total_bsmt_sf,
        '1st Flr SF': first_flr_sf,
        'Full Bath': full_bath,
        'TotRms AbvGrd': tot_rooms,
        'month_name': month_name,
        'Neighborhood': neighborhood
    }

    return pd.DataFrame(data, index=[0])

df_input = user_input_features()

st.subheader('Input Pengguna:')
st.write(df_input)

# ==== One-Hot Encoding Agar Sama dengan Training ====

training_columns = list(model.feature_names_in_)  # Kolom model hasil training

# DataFrame kosong berisi semua kolom yg dibutuhkan model
final_input = pd.DataFrame(columns=training_columns)
final_input.loc[0] = 0

# 1. Masukkan fitur numerik
for col in ['Overall Qual','Gr Liv Area','Garage Cars','Garage Area',
            'Total Bsmt SF','1st Flr SF','Full Bath','TotRms AbvGrd']:
    final_input.loc[0, col] = df_input[col][0]

# 2. One-hot encoding manual
for col in training_columns:
    if col.startswith('month_name_'):
        final_input.loc[0, col] = (col == f"month_name_{df_input['month_name'][0]}")
    if col.startswith('Neighborhood_'):
        final_input.loc[0, col] = (col == f"Neighborhood_{df_input['Neighborhood'][0]}")

# ==== Prediksi ====
if st.sidebar.button('Prediksi Harga'):
    pred = model.predict(final_input)[0]
    st.subheader('Hasil Prediksi Harga Rumah:')
    st.write(f" Harga Prediksi: **${pred:,.2f}**")

