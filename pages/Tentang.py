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
    .info-box {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #5dade2;
        margin-top: 20px;
    }
    .tech-card {
        background-color: #1c1c28;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px;
        transition: transform 0.2s ease;
    }
    .tech-card:hover {
        transform: scale(1.05);
        background-color: #2e4053;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Judul halaman ---
st.title("ℹ️ Tentang Aplikasi")

# --- Deskripsi umum ---
st.markdown("""
Aplikasi ini merupakan bagian dari **Tugas Akhir S1 Teknik Informatika** yang dikembangkan oleh  
**Nafcha Salsabila** 💻  

Tujuan utama aplikasi ini adalah membantu proses **identifikasi dini gangguan jiwa** berdasarkan gejala yang dialami oleh pengguna melalui sistem berbasis **machine learning**.
""")

# --- Info box deskripsi ---
st.markdown(
    """
    <div class="info-box">
    <h4>🎯 Tujuan Pengembangan</h4>
    <p>
    Dengan adanya aplikasi ini, diharapkan pengguna dapat memperoleh <b>informasi awal</b> mengenai kondisi mentalnya secara cepat dan efisien.
    Hasil dari sistem ini bukan diagnosis medis, melainkan sebagai <b>alat bantu awal</b> dalam proses identifikasi gejala.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Teknologi yang digunakan ---
st.markdown("### 🧩 Teknologi yang Digunakan")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="tech-card">
        <h4>🐍 Python</h4>
        <p>Bahasa pemrograman utama untuk logika sistem dan pemrosesan data.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="tech-card">
        <h4>🎨 Streamlit</h4>
        <p>Digunakan untuk membuat tampilan antarmuka web yang interaktif dan ringan.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="tech-card">
        <h4>🤖 Support Vector Machine (SVM)</h4>
        <p>Algoritma machine learning yang digunakan untuk klasifikasi jenis gangguan jiwa.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Catatan tambahan ---
st.markdown("---")
st.markdown("""
📘 **Catatan:**  
Aplikasi ini tidak menggantikan peran tenaga medis atau psikolog profesional.  
Hasil klasifikasi hanya digunakan sebagai **referensi awal** untuk membantu proses penilaian lanjutan.
""")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2025 | Dikembangkan oleh **Nafcha Salsabila** — Mahasiswa Teknik Informatika 💻")
