import streamlit as st
import pandas as pd
import altair as alt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Project", page_icon="🛠️")
# Judul Aplikasi
st.title("Faktor Demografis dan Sosioekonomi Yang Mempengaruhi Keputusan Customer Membeli Rumah Menggunakan Model Regresi Logistik")

# Upload file CSV
uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    # Membaca data CSV yang diunggah
    zein = pd.read_csv(uploaded_file, delimiter=';')

    # Preprocessing Data
    variabel_kategorik = ['Jenis Kelamin', 'Sumber', 'Status', 'Pekerjaan']
    for var in variabel_kategorik:
        le = LabelEncoder()
        zein[var] = le.fit_transform(zein[var])

    # Ubah tipe data menjadi numerik
    zein['Pendapatan'] = zein['Pendapatan'].str.replace('.', '').str.replace(' ', '').astype(float)
    zein['Budget'] = zein['Budget'].str.replace('.', '').str.replace(' ', '').astype(float)

    # Gabungkan proyek sesuai dengan permintaan
    proyek_mapping = {
        'BANDUNG I': 'BANDUNG',
        'BANDUNG II': 'BANDUNG',
        'JATIM 1': 'JATIM JATENG',
        'JATIM 2': 'JATIM JATENG',
        'SOLO JOGJA': 'JATIM JATENG',
        'SEMARANG': 'JATIM JATENG',
        'SULSEL': 'Sulawesi',
        'SULUT': 'Sulawesi',
        'SUTRA': 'Sulawesi',
        'SUMUT': 'SUMATERA',
        'LAMPUNG': 'SUMATERA',
        'KEPRI': 'SUMATERA',
        'SUMSEL': 'SUMATERA',
        'MAHATA MARGONDA': 'JABODETABEK',
        'MAHATA TANJUNG BARAT': 'JABODETABEK',
        'MAHATA SERPONG': 'JABODETABEK',
        'PARUNG PANJANG': 'JABODETABEK',
        'CENGKARENG': 'JABODETABEK',
        'DRAMAGA': 'JABODETABEK',
        'EAST POINT': 'JABODETABEK'
    }

    # Menerapkan penggantian proyek
    zein['Proyek'] = zein['Proyek'].replace(proyek_mapping)

    # Menambahkan opsi NASIONAL ke dalam proyek
    proyek_options = zein['Proyek'].unique().tolist()  # Mendapatkan opsi proyek yang unik
    proyek_options.append("NASIONAL")  # Menambahkan opsi NASIONAL

    # Tambahkan filter untuk proyek
    selected_proyek = st.selectbox("Pilih Proyek", proyek_options)

    # Filter data berdasarkan proyek yang dipilih
    if selected_proyek == "NASIONAL":
        zein_filtered = zein  # Jika NASIONAL, gunakan semua data
    else:
        zein_filtered = zein[zein['Proyek'] == selected_proyek]

    X = zein_filtered[['Jenis Kelamin', 'Sumber', 'Budget', 'Status', 'Pekerjaan', 'Pendapatan']]
    y = zein_filtered['Keputusan']

    # Pisahkan data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Standardisasi data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model Regresi Logistik
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Prediksi
    y_pred = model.predict(X_test_scaled)

    # Evaluasi model
    akurasi = accuracy_score(y_test, y_pred)
    st.write(f"Akurasi: {akurasi:.2f}")

    # Visualisasi koefisien fitur
    koefisien = model.coef_[0]
    fitur = X.columns
    df_penting = pd.DataFrame({'Fitur': fitur, 'Koefisien': koefisien})

    # Pisahkan koefisien positif dan negatif
    df_positif = df_penting[df_penting['Koefisien'] > 0]
    df_negatif = df_penting[df_penting['Koefisien'] < 0]

    # Mendapatkan fitur yang paling berpengaruh untuk positif dan negatif
    fitur_tertinggi_positif = df_positif.loc[df_positif['Koefisien'].idxmax(), 'Fitur']
    fitur_terendah_negatif = df_negatif.loc[df_negatif['Koefisien'].idxmin(), 'Fitur']

    # Plot koefisien positif dengan altair (horizontal bar chart)
    st.subheader("Variabel Yang Paling Berpengaruh Terhadap Keputusan Pembelian")
    chart_positif = alt.Chart(df_positif).mark_bar(color='steelblue').encode(
        x=alt.X('Koefisien:Q', title='Koefisien'),
        y=alt.Y('Fitur:N', sort='-x', title='Fitur'),
        tooltip=[alt.Tooltip('Fitur:N', title='Fitur'), alt.Tooltip('Koefisien:Q', title='Koefisien')]
    ).properties(
        title='Variabel Yang Paling Berpengaruh Terhadap Keputusan Pembelian'
    )

    # Menambahkan label untuk koefisien positif
    label_positif = chart_positif.mark_text(
        align='left',
        baseline='middle',
        dx=3,  # Jarak dari batang
        color='black'  # Warna label hitam
    ).encode(
        text=alt.Text('Koefisien:Q', format='.2f')
    )

    # Gabungkan chart batang dengan label
    st.altair_chart(chart_positif + label_positif, use_container_width=True)

    # Tampilkan kalimat fitur paling berpengaruh positif
    st.write(f"Variabel yang paling berpengaruh terhadap Keputusan Pembelian adalah Variabel **{fitur_tertinggi_positif}**.")

    # Plot koefisien negatif dengan altair (horizontal bar chart)
    st.subheader("Variabel Yang Paling Tidak Berpengaruh Terhadap Keputusan Pembelian")
    chart_negatif = alt.Chart(df_negatif).mark_bar(color='salmon').encode(
        x=alt.X('Koefisien:Q', title='Koefisien'),
        y=alt.Y('Fitur:N', sort='x', title='Fitur'),
        tooltip=[alt.Tooltip('Fitur:N', title='Fitur'), alt.Tooltip('Koefisien:Q', title='Koefisien')]
    ).properties(
        title='Variabel Yang Paling Tidak Berpengaruh Terhadap Keputusan Pembelian'
    )

    # Menambahkan label untuk koefisien negatif
    label_negatif = chart_negatif.mark_text(
        align='right',
        baseline='middle',
        dx=-3,  # Jarak dari batang (ke kiri)
        color='black'  # Warna label hitam
    ).encode(
        text=alt.Text('Koefisien:Q', format='.2f')
    )

    # Gabungkan chart batang dengan label
    st.altair_chart(chart_negatif + label_negatif, use_container_width=True)

    # Tampilkan kalimat fitur paling tidak berpengaruh negatif
    st.write(f"Variabel yang paling tidak berpengaruh terhadap Keputusan Pembelian adalah Variabel **{fitur_terendah_negatif}**.")
