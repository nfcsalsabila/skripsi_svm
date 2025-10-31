import streamlit as st
import pandas as pd
import joblib
from sklearn.decomposition import PCA
import plotly.express as px

# --- Load model & data ---
model = joblib.load('model/svm_model.pkl')
data = pd.read_excel('data/train.xlsx')

# --- Pisahkan fitur dan label ---
X = data.drop(['Disorder', 'severity'], axis=1)
y = data['Disorder']   # <---- Tambahkan baris ini

# --- PCA ke 3D ---
pca = PCA(n_components=3)
X_3d = pca.fit_transform(X)

# --- DataFrame untuk visualisasi ---
df_3d = pd.DataFrame(X_3d, columns=['PCA1', 'PCA2', 'PCA3'])
df_3d['Label'] = y

# --- Plot interaktif ---
fig = px.scatter_3d(
    df_3d,
    x='PCA1',
    y='PCA2',
    z='PCA3',
    color='Label',
    title="Visualisasi Data SVM dalam Ruang 3D PCA",
    symbol='Label',
    opacity=0.8
)

st.subheader("Visualisasi PCA 3D (Interaktif)")
st.plotly_chart(fig)
