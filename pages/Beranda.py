import streamlit as st

# --- Styling dark mode (selaras dengan halaman utama) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    h1, h2, h3, h4 {
        color: #5dade2 !important;
    }
    p, div, label, span {
        color: #e0e0e0 !important;
    }
    .stButton>button {
        background-color: #2e4053 !important;
        color: #e0e0e0 !important;
        border: none !important;
        border-radius: 8px !important;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #5dade2 !important;
        color: #ffffff !important;
    }
    .info-box {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #5dade2;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Konten utama ---
st.title("🏠 Beranda")
st.write("""
Selamat datang di **Sistem Klasifikasi & Identifikasi Jenis Gangguan Jiwa** 🧠  
Aplikasi ini dirancang untuk membantu proses identifikasi awal gangguan jiwa berdasarkan **jawaban kuisioner gejala mental**.
""")

# --- Info box ---
st.markdown(
    """
    <div class="info-box">
    <h4>🎯 Tujuan Sistem</h4>
    <p>
    Aplikasi ini membantu pengguna atau tenaga profesional untuk mendapatkan <b>gambaran awal</b>
    mengenai kondisi psikologis seseorang.  
    Model ini memanfaatkan <b>algoritma Support Vector Machine (SVM)</b> yang telah dilatih dengan data gangguan jiwa,
    seperti <i>Depresi, Skizofrenia, Gangguan Bipolar, dan lainnya.</i>
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Fitur utama ---
st.markdown("### ⚙️ Fitur Utama")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📋 Klasifikasi Gejala**")
    st.write("Isi kuisioner untuk mengetahui kemungkinan jenis gangguan jiwa dan tingkat keparahannya.")
with col2:
    st.markdown("**📊 Hasil Analisis**")
    st.write("Sistem menampilkan hasil prediksi lengkap dengan penjelasan gangguan dan rekomendasi tindakan.")
with col3:
    st.markdown("**💾 Penyimpanan Otomatis**")
    st.write("Setiap hasil klasifikasi disimpan agar dapat digunakan untuk analisis selanjutnya.")

# --- Petunjuk penggunaan ---
st.markdown("---")
st.subheader("💡 Cara Menggunakan")
st.write("""
1. Buka menu **'Klasifikasi'** di sidebar.  
2. Isi identitas dan seluruh pertanyaan kuisioner.  
3. Klik tombol **'Lakukan Klasifikasi'** untuk memproses hasil.  
4. Lihat hasil jenis gangguan beserta **tingkat keparahan dalam bentuk persentase**.
""")

# --- Tombol mulai ---
st.markdown("---")
if st.button("🧠 Mulai Klasifikasi Sekarang"):
    st.switch_page("pages/Klasifikasi.py")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2025 | Aplikasi Skripsi oleh **Nafcha Salsabila**, Teknik Informatika 💻")
