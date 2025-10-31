import streamlit as st
import pandas as pd
import joblib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

st.title("🧠 Visualisasi Model SVM")

# --- Muat model dan data ---
try:
    model = joblib.load("model/svm_model.pkl")
    data = pd.read_excel("data/train.xlsx")
except FileNotFoundError:
    st.error("❌ File model atau data tidak ditemukan! Pastikan path 'model/svm_model.pkl' dan 'data/train.xlsx' benar.")
    st.stop()

# --- Cek kolom ---
if 'Disorder' not in data.columns:
    st.error("Kolom 'Disorder' tidak ditemukan dalam data!")
    st.write("Kolom yang tersedia:", data.columns.tolist())
    st.stop()

# --- Pisahkan fitur dan label ---
X = data.drop(['Disorder', 'severity'], axis=1)
y_true = data['Disorder']

# --- Prediksi model ---
try:
    y_pred = model.predict(X)
except Exception as e:
    st.error(f"Terjadi error saat memprediksi dengan model: {e}")
    st.stop()

# --- Pilihan visualisasi ---
mode = st.radio("Pilih jenis visualisasi:", ["2D PCA", "3D PCA"])
display_mode = st.radio("Tampilkan warna berdasarkan:", ["Label Asli", "Prediksi Model"])

# --- PCA untuk reduksi dimensi ---
if mode == "2D PCA":
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    x1, x2 = X_pca[:, 0], X_pca[:, 1]

    # Tentukan label warna
    if display_mode == "Label Asli":
        labels = y_true
        title = "Visualisasi Berdasarkan Label Asli (PCA 2D)"
    else:
        labels = y_pred
        title = "Visualisasi Berdasarkan Prediksi Model (PCA 2D)"

    fig, ax = plt.subplots()
    scatter = ax.scatter(x1, x2, c=pd.factorize(labels)[0], cmap='tab10', alpha=0.8)
    legend_labels = np.unique(labels)

    handles, _ = scatter.legend_elements()
    legend_labels = np.unique(labels).tolist()
    handles, _ = scatter.legend_elements()
    legend_labels = np.unique(labels).tolist()
    ax.legend(
    handles=list(handles),
    labels=legend_labels,
    title="Kelas",
    bbox_to_anchor=(1.25, 1),  # 👉 geser lebih jauh ke kanan
    loc='upper left',
    borderaxespad=0.
)
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.set_title(title)
    st.pyplot(fig)

else:  # 3D PCA
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)
    x1, x2, x3 = X_pca[:, 0], X_pca[:, 1], X_pca[:, 2]

    if display_mode == "Label Asli":
        labels = y_true
        title = "Visualisasi Berdasarkan Label Asli (PCA 3D)"
    else:
        labels = y_pred
        title = "Visualisasi Berdasarkan Prediksi Model (PCA 3D)"

        fig = plt.figure()
        plt.tight_layout()
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x1, x2, x3, c=pd.factorize(labels)[0], cmap='tab10', alpha=0.8)

    handles, _ = scatter.legend_elements()
    legend_labels = np.unique(labels).tolist()
    ax.legend(
    handles=list(handles),
    labels=legend_labels,
    title="Kelas",
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0.
    )

    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.set_zlabel("PC 3")
    ax.set_title(title)
    st.pyplot(fig)


# --- Info tambahan ---
st.markdown("""
---
**Keterangan:**
- Titik-titik merepresentasikan data latih yang direduksi ke dimensi 2D/3D menggunakan PCA.
- Warna menggambarkan kelas sesuai pilihan di atas:
  - **Label Asli** → dari dataset (kolom `Disorder`)
  - **Prediksi Model** → hasil klasifikasi dari model SVM
""")
