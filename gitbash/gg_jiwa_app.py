import streamlit as st
import pandas as pd
import joblib


# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Sistem Klasifikasi & Identifikasi Jenis Gangguan Jiwa",
    page_icon="🧠",
    layout="wide"
)

# --- Sidebar bawah: identitas aplikasi ---
with st.sidebar:
    st.caption("Dibuat oleh **Nafcha Salsabila** — Mahasiswa Teknik Informatika 💻")

# --- Styling sidebar & halaman utama (dark mode elegan) ---
st.markdown(
    """
    <style>
    /* ---------------- Sidebar ---------------- */
    [data-testid="stSidebar"] {
        background-color: #1e1e2f; /* warna sidebar gelap */
        color: #f0f0f0;
    }

    /* Hilangkan teks "Pages" bawaan Streamlit dan ganti custom title */
    [data-testid="stSidebarNav"]::before {
        content: "🧭 Navigasi Utama";
        font-size: 20px;
        font-weight: 600;
        color: #5dade2;
        margin-left: 20px;
        margin-top: 10px;
        display: block;
    }

    /* Style menu di sidebar */
    [data-testid="stSidebarNav"] li a {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
        border-radius: 8px !important;
        transition: background-color 0.2s ease, color 0.2s ease;
        padding: 6px 14px !important;
    }

    [data-testid="stSidebarNav"] li a:hover {
        background-color: #27374d !important;
        color: #5dade2 !important;
    }

    /* ---------------- Konten utama ---------------- */
    .stApp {
        background-color: #121212; /* latar belakang halaman */
        color: #e0e0e0; /* teks utama */
    }

    h1, h2, h3, h4 {
        color: #5dade2 !important; /* warna judul */
    }

    p, div, label, span {
        color: #e0e0e0 !important;
    }

    /* Tambahkan efek lembut pada tombol */
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
    </style>
    """,
    unsafe_allow_html=True
)

# --- Halaman utama ---
st.title("🧠 Sistem Klasifikasi & Identifikasi Jenis Gangguan Jiwa")
st.write("""
"Selamat datang di aplikasi **Klasifikasi dan Identifikasi Jenis Gangguan Jiwa** berbasis **Support Vector Machine (SVM)**."  

Gunakan menu di sidebar untuk berpindah halaman.
""")

# --- Tambahan tampilan utama --- #

# Seksi deskripsi
st.markdown("---")
st.subheader("📘 Tentang Sistem Ini")
st.write("""
Aplikasi ini dirancang untuk membantu **identifikasi awal jenis gangguan jiwa** berdasarkan gejala yang dilaporkan oleh pengguna.  
Model ini menggunakan algoritma **Support Vector Machine (SVM)** yang telah dilatih pada data gejala mental,  
dan dapat memberikan hasil berupa **jenis gangguan jiwa** beserta **tingkat keparahannya** secara otomatis.
""")

# Seksi alur kerja
st.markdown("---")
st.subheader("⚙️ Cara Kerja Sistem")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 1️⃣ Input Data")
    st.write("Pengguna mengisi identitas dan menjawab kuisioner gejala mental.")
with col2:
    st.markdown("### 2️⃣ Proses Klasifikasi")
    st.write("Sistem memproses data menggunakan model SVM untuk menentukan jenis gangguan.")
with col3:
    st.markdown("### 3️⃣ Hasil & Rekomendasi")
    st.write("Sistem menampilkan hasil klasifikasi serta rekomendasi tindak lanjut.")

# Seksi petunjuk penggunaan
st.markdown("---")
st.subheader("💡 Petunjuk Penggunaan")
st.write("""
- Pilih menu **Klasifikasi** di sidebar untuk mulai mengisi kuisioner.  
- Pastikan semua pertanyaan dijawab agar hasil dapat dihitung dengan benar.  
- Setelah proses selesai, sistem akan menampilkan **jenis gangguan jiwa** dan **tingkat keparahan** dalam bentuk persentase.  
""")

# Seksi tombol cepat
st.markdown("---")
st.subheader("🚀 Ayo Mulai!")
if st.button("Mulai Klasifikasi Sekarang 🧠"):
    st.switch_page("pages/Klasifikasi.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2025 | Aplikasi Skripsi oleh **Nafcha Salsabila**, Teknik Informatika 💻")


