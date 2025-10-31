import streamlit as st
import pandas as pd
import joblib
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import io
import os

# --- Styling dark mode ---
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
    p, div, label {
        color: #e0e0e0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load model dan scaler ---
model = joblib.load("model/svm_model.pkl")
scaler = joblib.load("model/scaler.pkl")

st.title("🧠 Sistem Klasifikasi & Identifikasi Gangguan Jiwa")
st.write("Masukkan data pasien di bawah ini untuk melakukan klasifikasi:")

# --- Identitas Pasien ---
st.header("🧍 Identitas Pasien")

hasil_file = "data/hasil_klasifikasi.xlsx"

if os.path.exists(hasil_file):
    existing_data = pd.read_excel(hasil_file)
    next_id = len(existing_data) + 1
else:
    next_id = 1

kode_pasien = f"P{next_id:03d}"
st.text_input("Kode Pasien", kode_pasien, disabled=True)
col1, col2 = st.columns(2)

with col1:
    umur = st.number_input("Umur", min_value=1, max_value=120, step=1)
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

with col2:
    pekerjaan = st.text_input("Pekerjaan")
    pendidikan = st.selectbox("Pendidikan Terakhir", ["SD", "SMP", "SMA/SMK", "D3", "S1", "S2", "S3"])

# --- Pertanyaan Kuisioner ---
st.header("💬 Pilih Jawaban Yang Sesuai")

questions = {
    "merasa.gugup": "Apakah sering merasa gugup atau tegang tanpa alasan yang jelas?",
    "panik": "Apakah pernah mengalami serangan panik secara tiba-tiba?",
    "hiperventilasi": "Apakah pernah bernapas terlalu cepat hingga sulit mengendalikan napas?",
    "hyperhidrosis": "Apakah mengalami keringat berlebih meskipun tidak sedang beraktivitas berat?",
    "sulit.konsentrasi": "Apakah belakangan ini sulit untuk tetap fokus atau berkonsentrasi?",
    "gangguan.tidur": "Apakah mengalami kesulitan tidur atau tidur tidak nyenyak dalam beberapa minggu terakhir?",
    "bermasalah.dgn.pekerjaan": "Apakah kondisi emosional atau mental mulai mengganggu pekerjaan atau aktivitas harian?",
    "hopelessness": "Apakah sering merasa tidak memiliki harapan terhadap masa depan?",
    "marah": "Apakah menjadi lebih mudah marah atau tersulut emosi?",
    "halusinasi": "Apakah pernah mendengar atau melihat sesuatu yang sebenarnya tidak ada?",
    "reaksi.berlebihan": "Apakah sering memberikan reaksi berlebihan terhadap situasi kecil?",
    "perubahan.pola.makan": "Apakah pola makan berubah drastis (lebih banyak atau jauh lebih sedikit dari biasanya)?",
    "pikiran.bunuh.diri": "Apakah pernah muncul pikiran untuk mengakhiri hidup?",
    "perasaan.lelah": "Apakah sering merasa lelah meskipun tidak banyak beraktivitas?",
    "menarik.diri": "Apakah cenderung menarik diri dan menghindari interaksi dengan orang lain?",
    "kecanduan.media.sosial": "Apakah penggunaan media sosial terasa berlebihan hingga mengganggu aktivitas penting?",
    "kenaikan.berat.badan": "Apakah belakangan ini berat badan meningkat secara signifikan?",
    "kurangnya.interaksi.sosial": "Apakah frekuensi interaksi sosial menurun dibanding biasanya?",
    "ingatan.intrusif.traumatis": "Apakah muncul ingatan traumatis yang tiba-tiba muncul dan sulit dikendalikan?",
    "mimpi.buruk.berulang": "Apakah sering mengalami mimpi buruk berulang terkait pengalaman tertentu?",
    "anhedonia": "Apakah kehilangan minat atau tidak merasakan kesenangan dari hal-hal yang biasanya disukai?",
    "perasaan.negatif": "Apakah sering dipenuhi perasaan negatif seperti sedih, takut, atau gelisah?",
    "gangguan.konsentrasi": "Apakah kesulitan mempertahankan fokus dalam aktivitas sehari-hari?",
    "menyalahkan.diri.sendiri": "Apakah sering menyalahkan diri sendiri atas hal-hal yang terjadi?",
    "perilaku.berulang": "Apakah sering melakukan tindakan secara berulang tanpa bisa mengontrolnya?",
    "depresi.musiman": "Apakah suasana hati menurun secara signifikan pada waktu atau musim tertentu?",
    "aktivitas.berlebihan": "Apakah muncul dorongan untuk aktif atau bergerak secara berlebihan tanpa rasa lelah?"
}

choices = {
    "Tidak Pernah": 0,
    "Kadang": 1,
    "Sering": 2,
    "Sangat Sering": 3
}

answers = []
for key, q in questions.items():
    ans = st.radio(q, list(choices.keys()), index=0, key=key)
    answers.append(choices[ans])

# --- Tombol Prediksi ---
if st.button("🔍 Lakukan Klasifikasi"):
    # --- Validasi input identitas ---
    if not all([umur, jenis_kelamin, pekerjaan, pendidikan]):
        st.warning("⚠️ Harap isi semua identitas terlebih dahulu sebelum melakukan klasifikasi.")
    else:
        # --- Siapkan data input ---
        input_data = dict(zip(questions.keys(), answers))
        input_df = pd.DataFrame([input_data])

        # Samakan kolom agar sesuai dengan scaler
        missing_cols = [col for col in scaler.feature_names_in_ if col not in input_df.columns]
        for col in missing_cols:
            input_df[col] = 0
        input_df = input_df[scaler.feature_names_in_]
        X_scaled = scaler.transform(input_df)
        hasil_prediksi = model.predict(X_scaled)[0]
        total_score = sum(answers)

        # Transformasi skala
        X_scaled = scaler.transform(input_df)

        # Prediksi hasil
        hasil_prediksi = model.predict(X_scaled)[0]

        # Hitung tingkat keparahan
        total_score = sum(answers)
        max_score = len(questions) * 3
        severity_ratio = total_score / max_score
        severity_percent = severity_ratio * 100 

        if severity_ratio < 0.33:
            tingkat = "Rendah"
        elif severity_ratio < 0.66:
            tingkat = "Sedang"
        else:
            tingkat = "Berat"

        # --- Data penjelasan gangguan (versi formal ilmiah) ---
        penjelasan_gangguan = {
    "MDD": {
        "deskripsi": "Major Depressive Disorder (MDD) atau Gangguan Depresi Mayor merupakan gangguan suasana hati yang ditandai oleh perasaan sedih mendalam, "
        "kehilangan minat terhadap aktivitas yang sebelumnya menyenangkan, serta disertai gangguan pada pola tidur, nafsu makan, dan kemampuan berkonsentrasi. "
        "Gangguan ini berlangsung minimal selama dua minggu dan dapat menghambat fungsi sosial, akademik, maupun pekerjaan individu. "
        "Penyebab MDD meliputi kombinasi faktor biologis, genetik, psikologis, serta lingkungan. Penanganannya umumnya dilakukan melalui psikoterapi dan farmakoterapi."
        "Durasi minimal: 2 minggu berturut-turut.",
        "warna": "#a569bd",
        "ikon": "🌀"
    },
    "OCD": {
        "deskripsi": "Obsessive-Compulsive Disorder (OCD) atau Gangguan Obsesif-Kompulsif merupakan gangguan kecemasan yang ditandai oleh adanya obsesi dan kompulsi. "
        "Obsesi adalah pikiran, dorongan, atau gambaran yang muncul berulang dan menimbulkan kecemasan, sedangkan kompulsi merupakan tindakan atau perilaku berulang "
        "yang dilakukan untuk mengurangi kecemasan akibat obsesi tersebut. Penderita menyadari bahwa pikirannya berlebihan, namun merasa sulit untuk mengendalikan perilaku tersebut. "
        "Gangguan ini dapat mengganggu aktivitas harian dan hubungan sosial jika tidak ditangani dengan tepat."
        "Tidak ditentukan durasi waktu yang spesifik, tetapi obsesi dan kompulsi harus menetap cukup lama untuk menyebabkan gangguan bermakna terhadap fungsi sosial, pekerjaan, atau kehidupan sehari-hari.",
        "warna": "#c0392b",
        "ikon": "👁️"
    },
    "ASD": {
        "deskripsi": "Autism Spectrum Disorder (ASD) atau Gangguan Spektrum Autisme merupakan gangguan perkembangan saraf yang memengaruhi kemampuan komunikasi, "
        "interaksi sosial, dan pola perilaku individu. Penderita ASD umumnya menunjukkan minat terbatas, perilaku berulang, serta kesulitan dalam memahami ekspresi sosial. "
        "Gangguan ini muncul sejak masa kanak-kanak dan bersifat spektrum, artinya tingkat keparahannya berbeda-beda pada setiap individu. "
        "Faktor penyebabnya meliputi aspek genetik dan neurobiologis, sedangkan penanganan dapat dilakukan melalui terapi perilaku, terapi wicara, dan pendidikan khusus."
        "Tidak memiliki batas durasi tertentu karena merupakan gangguan perkembangan saraf (neurodevelopmental) — artinya gejala sudah muncul sejak masa kanak-kanak dini dan bersifat jangka panjang.",
        "warna": "#5dade2",
        "ikon": "💧"
    },
    "Gangguan Kecemasan": {
        "deskripsi": "Gangguan Kecemasan (Anxiety Disorder) merupakan kondisi psikologis yang ditandai oleh perasaan takut atau khawatir yang berlebihan tanpa penyebab yang jelas. "
        "Penderitanya sering mengalami gejala fisik seperti jantung berdebar, keringat dingin, gemetar, serta gangguan tidur dan konsentrasi. "
        "Gangguan ini dapat disebabkan oleh stres berkepanjangan, pengalaman traumatis, atau ketidakseimbangan neurotransmiter di otak. "
        "Terapi perilaku kognitif dan manajemen stres merupakan pendekatan umum yang digunakan dalam penanganan gangguan ini.",
        "warna": "#f39c12",
        "ikon": "⚡"
    },
    "Gangguan Bipolar": {
        "deskripsi": "Gangguan Bipolar merupakan gangguan suasana hati yang ditandai oleh perubahan emosi yang ekstrem antara episode mania dan depresi. "
        "Pada fase mania, individu menunjukkan peningkatan energi, euforia, dan perilaku impulsif, sedangkan pada fase depresi individu mengalami penurunan motivasi, "
        "kesedihan mendalam, serta kehilangan minat terhadap aktivitas sehari-hari. Gangguan ini memiliki dasar biologis yang kuat dan memerlukan kombinasi pengobatan "
        "psikoterapi serta penggunaan penstabil suasana hati untuk mengendalikan gejalanya."
        "Episode mania harus berlangsung minimal 1 minggu, sedangkan episode hipomania minimal 4 hari.",
        "warna": "#16a085",
        "ikon": "🌗"
    },
    "Anxiety": {
        "deskripsi": "Anxiety atau gangguan kecemasan adalah kondisi psikologis yang ditandai dengan kekhawatiran berlebihan, ketegangan emosional, serta rasa takut yang sulit dikendalikan. "
        "Walaupun kecemasan merupakan reaksi normal terhadap stres, gangguan ini menjadi patologis apabila mengganggu fungsi kehidupan sehari-hari. "
        "Faktor penyebabnya meliputi stres kronis, trauma emosional, maupun ketidakseimbangan zat kimia otak. "
        "Pendekatan terapi yang umum digunakan meliputi terapi perilaku kognitif, teknik relaksasi, serta pemberian obat anti-kecemasan.",
        "warna": "#d35400",
        "ikon": "😰"
    },
    "Eating Disorder": {
        "deskripsi": "Eating Disorder atau Gangguan Pola Makan adalah gangguan psikologis yang memengaruhi perilaku makan dan persepsi terhadap bentuk tubuh. "
        "Jenis gangguan ini mencakup anoreksia nervosa, bulimia nervosa, dan binge-eating disorder. "
        "Penderita sering memiliki citra tubuh yang negatif, rasa takut berlebihan terhadap kenaikan berat badan, atau perilaku kompulsif terkait makan. "
        "Gangguan ini dapat menyebabkan komplikasi medis serius seperti malnutrisi, gangguan hormonal, dan masalah jantung. "
        "Pendekatan terapeutik melibatkan konseling psikologis, terapi gizi, serta dukungan keluarga."
        "gejala muncul setidaknya 3 kali seminggu selama 3 bulan.",
        "warna": "#e67e22",
        "ikon": "🍽️"
    },
    "PDD": {
        "deskripsi": "Persistent Depressive Disorder (PDD) atau Dysthymia adalah bentuk depresi kronis yang berlangsung selama dua tahun atau lebih. "
        "Meskipun gejalanya lebih ringan dibandingkan depresi mayor, kondisi ini bersifat persisten dan dapat menurunkan kualitas hidup secara signifikan. "
        "Gejala umum meliputi perasaan sedih berkepanjangan, kelelahan, gangguan tidur, serta kehilangan minat terhadap aktivitas. "
        "Penanganan PDD dilakukan melalui kombinasi psikoterapi jangka panjang dan pemberian obat antidepresan sesuai kebutuhan klinis."
        "Durasi minimal: 2 tahun (pada orang dewasa) atau 1 tahun (pada anak-anak/remaja).",
        "warna": "#884ea0",
        "ikon": "🌧️"
    },
    "PTSD": {
        "deskripsi": "Post-Traumatic Stress Disorder (PTSD) atau Gangguan Stres Pascatrauma merupakan gangguan mental yang muncul setelah seseorang mengalami peristiwa traumatis, "
        "seperti kekerasan, bencana alam, atau kecelakaan berat. Penderita umumnya mengalami kilas balik (flashback), mimpi buruk, gangguan tidur, serta kecenderungan menghindari situasi "
        "yang mengingatkan pada peristiwa tersebut. PTSD juga dapat menyebabkan perubahan suasana hati, iritabilitas, dan kewaspadaan berlebihan. "
        "Terapi perilaku kognitif, konseling trauma, serta dukungan sosial terbukti efektif dalam membantu pemulihan individu yang mengalami PTSD."
        "Durasi minimal: 1 bulan setelah peristiwa traumatis.",
        "warna": "#7d3c98",
        "ikon": "🔥"
    },
    "ADHD": {
        "deskripsi": "Attention Deficit Hyperactivity Disorder (ADHD) merupakan gangguan perkembangan saraf yang ditandai oleh kesulitan dalam memusatkan perhatian, "
        "hiperaktivitas, dan impulsivitas yang tidak sesuai dengan tahap perkembangan usia. Gangguan ini sering muncul pada masa kanak-kanak dan dapat berlanjut hingga dewasa. "
        "Individu dengan ADHD cenderung mudah terdistraksi, sulit mengatur waktu, serta memiliki kesulitan dalam menyelesaikan tugas. "
        "Penanganan dilakukan melalui kombinasi terapi perilaku, konseling, serta pemberian obat stimulan sesuai rekomendasi profesional medis."
        "Gejala harus muncul sebelum usia 12 tahun dan bertahan minimal 6 bulan, serta tampak pada lebih dari satu situasi (misalnya di sekolah dan di rumah).",
        "warna": "#3498db",
        "ikon": "⚙️"
    },
    "Sleeping Disorder": {
        "deskripsi": "Sleeping Disorder atau Gangguan Tidur mencakup berbagai kondisi yang memengaruhi kualitas dan kuantitas tidur seseorang. "
        "Beberapa bentuk gangguan tidur antara lain insomnia, sleep apnea, hypersomnia, dan parasomnia. "
        "Gangguan tidur yang berkepanjangan dapat menyebabkan kelelahan, gangguan kognitif, penurunan daya tahan tubuh, serta gangguan suasana hati. "
        "Penatalaksanaan dilakukan melalui terapi perilaku, pengaturan pola tidur yang konsisten, serta pengobatan medis bila diperlukan."
        "gejala muncul setidaknya 3 kali seminggu selama 3 bulan.",
        "warna": "#2ecc71",
        "ikon": "🌙"
    },
    "Loneliness": {
        "deskripsi": "Loneliness atau perasaan kesepian merupakan kondisi emosional yang ditandai oleh perasaan terisolasi, kurangnya hubungan sosial yang bermakna, "
        "atau ketidakpuasan terhadap kualitas hubungan interpersonal. Kondisi ini dapat meningkatkan risiko depresi, gangguan kecemasan, serta penurunan kesejahteraan psikologis. "
        "Intervensi yang efektif meliputi peningkatan dukungan sosial, keterlibatan dalam aktivitas kelompok, serta konseling psikologis untuk meningkatkan koneksi sosial dan rasa kebermaknaan.",
        "warna": "#95a5a6",
        "ikon": "🫧"
    },
    "Psychotic Depression": {
        "deskripsi": "Psychotic Depression atau Depresi Psikotik merupakan bentuk depresi berat yang disertai dengan gejala psikotik seperti halusinasi atau delusi. "
        "Penderita mengalami kehilangan kontak dengan realitas, disertai perasaan bersalah berlebihan, kecurigaan tidak rasional, atau persepsi yang menyimpang. "
        "Gangguan ini membutuhkan penanganan intensif dengan kombinasi antidepresan dan antipsikotik, serta dukungan psikoterapi yang berkelanjutan.",
        "warna": "#9b59b6",
        "ikon": "🕳️"
    },
    "Normal": {
        "deskripsi": "Kondisi normal menunjukkan bahwa tidak terdapat indikasi gangguan kejiwaan yang signifikan. "
        "Individu berada dalam keadaan emosional yang stabil, mampu mengelola stres dengan baik, serta memiliki kemampuan berinteraksi sosial secara adaptif. "
        "Fungsi kognitif, afektif, dan perilaku berada dalam batas kewajaran sesuai norma sosial dan budaya yang berlaku.",
        "warna": "#27ae60",
        "ikon": "🌿"
    }
     }

        # --- Hasil Klasifikasi ---
        st.subheader("📊 Hasil Klasifikasi")
        st.write(f"**🧩 Kemungkinan Tergolong Jenis :** {hasil_prediksi}")
        st.write(f"**🔥 Tingkat Keparahan:** {tingkat}")
        st.write(f"**Persentase:** {severity_percent:.1f}%")
        st.progress(severity_ratio)

        if hasil_prediksi in penjelasan_gangguan:
            g = penjelasan_gangguan[hasil_prediksi]
            st.markdown(
                f"""
                <div style="
                    background-color:{g['warna']}25;
                    border-left:5px solid {g['warna']};
                    padding:15px;
                    border-radius:10px;
                    margin-top:10px;
                ">
                <h4 style="color:{g['warna']}; margin-bottom:5px;">
                {g['ikon']} Penjelasan:
                </h4>
                <p style="color:#e0e0e0;">{g['deskripsi']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # --- Rekomendasi ---
        st.markdown("---")
        st.subheader("💬 Rekomendasi:")
        if tingkat == "Rendah":
            st.write("🌿 Kondisi masih ringan. Jaga pola tidur, olahraga ringan, dan hindari stres berlebih.")
        elif tingkat == "Sedang":
            st.write("⚖️ Kondisi sedang. Coba relaksasi, journaling, atau bicarakan dengan orang terdekat.")
        else:
            st.write("🔥 Kondisi cukup berat. Disarankan segera berkonsultasi dengan psikolog atau psikiater.")

        st.markdown("---")
        st.caption("Aplikasi ini bersifat edukatif dan tidak menggantikan diagnosis profesional.")

        # --- Simpan hasil klasifikasi ---
        hasil_data = {
        "Kode Pasien": [kode_pasien],
        "Umur": [umur],
        "Jenis Kelamin": [jenis_kelamin],
        "Pekerjaan": [pekerjaan],
        "Pendidikan": [pendidikan],
        "Jenis Gangguan": [hasil_prediksi],
        "Tingkat Keparahan": [tingkat],
        "Skor Total": [total_score],
        "Waktu": [pd.Timestamp.now()]
        }

        hasil_df = pd.DataFrame(hasil_data)

        try:
            existing_df = pd.read_excel("data/hasil_klasifikasi.xlsx")
            updated_df = pd.concat([existing_df, hasil_df], ignore_index=True)
        except FileNotFoundError:
            updated_df = hasil_df

        updated_df.to_excel("data/hasil_klasifikasi.xlsx", index=False)
        st.success("✅ Hasil klasifikasi berhasil disimpan ke 'data/hasil_klasifikasi.xlsx'")

        # === Contoh data gejala (ganti dengan data dari inputmu) ===
        daftar_gejala = {}
        for key, val in zip(questions.keys(), answers):
            
        # Ubah nilai (0-3) jadi persentase biar lebih informatif
            persen = round((val / 3) * 100, 1)
        daftar_gejala[key.replace(".", " ").title()] = persen
        
        # === Buat daftar gejala terdeteksi berdasarkan jawaban ===
        daftar_gejala = {}
        for key, val in zip(questions.keys(), answers):
            persen = round((val / 3) * 100, 1)
            if persen > 0:  # hanya tampilkan gejala yang memiliki nilai
                daftar_gejala[key.replace(".", " ").title()] = persen

        # === Buat PDF ===
        buffer_pdf = io.BytesIO()
        lebar_nota = 80 * mm
        tinggi_nota = max(200, 80 + len(daftar_gejala) * 8) * mm
        c = canvas.Canvas(buffer_pdf, pagesize=portrait((lebar_nota, tinggi_nota)))

        # Header nota
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(lebar_nota / 2, tinggi_nota - 10 * mm, "🧠 HASIL KLASIFIKASI GANGGUAN JIWA")
        c.setFont("Helvetica", 8)
        y = tinggi_nota - 20 * mm
        c.line(5 * mm, y, lebar_nota - 5 * mm, y)
        y -= 5 * mm

        # Fungsi tulis
        def tulis(label, value):
            global y
            c.setFont("Helvetica-Bold", 8)
            c.drawString(6 * mm, y, f"{label}")
            c.setFont("Helvetica", 8)
            c.drawRightString(lebar_nota - 6 * mm, y, str(value))
            y -= 5 * mm

        # Isi nota
        tulis("Kode Pasien", kode_pasien)
        tulis("Umur", umur)
        tulis("Jenis Kelamin", jenis_kelamin)
        tulis("Pendidikan", pendidikan)
        c.line(5 * mm, y, lebar_nota - 5 * mm, y)
        y -= 5 * mm

        tulis("Jenis Gangguan", hasil_prediksi)
        tulis("Tingkat Keparahan", tingkat)
        tulis("Persentase", f"{severity_percent:.1f}%")
        c.line(5 * mm, y, lebar_nota - 5 * mm, y)
        y -= 5 * mm

        # --- Daftar gejala ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(6 * mm, y, "DAFTAR GEJALA TERDETEKSI:")
        y -= 5 * mm
        c.setFont("Helvetica", 8)

        if daftar_gejala:
            for gejala, persen in daftar_gejala.items():
                c.drawString(8 * mm, y, f"- {gejala}")
                c.drawRightString(lebar_nota - 8 * mm, y, f"{persen}%")
                y -= 5 * mm
        else:
            c.drawString(8 * mm, y, "Tidak ada gejala signifikan yang terdeteksi.")
            y -= 5 * mm

        c.line(5 * mm, y, lebar_nota - 5 * mm, y)
        y -= 5 * mm
        c.setFont("Helvetica-Oblique", 7)
        c.drawCentredString(lebar_nota / 2, y, "Hasil bersifat indikatif, bukan diagnosis medis.")
        y -= 5 * mm
        c.drawCentredString(lebar_nota / 2, y, "Terima kasih telah menggunakan sistem ini 💙")

        # Simpan PDF
        c.showPage()
        c.save()
        buffer_pdf.seek(0)

        # Tombol unduh PDF
        st.download_button(
            label="🧾 Unduh Nota Hasil (PDF)",
            data=buffer_pdf,
            file_name=f"nota_hasil_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
