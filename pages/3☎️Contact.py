import streamlit as st

st.set_page_config(page_title="Contact", page_icon="☎️")

def kontak_kami():
    # Menampilkan judul Perum Perumnas di atas Kontak Kami
    st.markdown("<h1 style='text-align: center;'>Perum Perumnas</h1>", unsafe_allow_html=True)
    
    # Menampilkan judul di tengah

    st.markdown("<h1 style='text-align: center;'>📞Kontak Kami📞</h1>", unsafe_allow_html=True)

    # Alamat Perusahaan
    st.subheader("Alamat Perusahaan")
    st.write("Jalan Mayor Jenderal DI Panjaitan 13340, RT.7/RW.11, Cipinang Cempedak, Jatinegara, East Jakarta City, Jakarta 13340")

    # Nomor Telepon
    st.subheader("Nomor Telepon")
    st.write("+62 21 819 4807")

    # Email Kontak
    st.subheader("Email Kontak")
    st.write("[ktrpusat@perumnas.co.id](mailto:ktrpusat@perumnas.co.id)")

    # Formulir Kontak
    st.subheader("Hal yang ingin ditanyakan")
    with st.form(key='kontak_form'):
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        pesan = st.text_area("Pesan")
        submit_button = st.form_submit_button("Kirim Pesan")

        if submit_button:
            st.success("Pesan Anda telah dikirim!")

    # Jam Kerja
    st.subheader("Jam Kerja")
    st.write("Senin - Jumat: 08.00 - 17.00 WIB")
    st.write("Sabtu * Minggu: Tutup")

# Panggil fungsi
kontak_kami()
