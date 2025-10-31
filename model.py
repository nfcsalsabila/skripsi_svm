import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix
)
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# === 1. Load data ===
data = pd.read_excel("data/train.xlsx")

# === 2. Pisahkan fitur dan label ===
X = data.drop(columns=["Disorder", "severity"])
y = data["Disorder"]

# === 3. Split data sebelum SMOTE ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# === 4. Scaling data ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === 5. Oversampling SMOTE di data training SAJA ===
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

# === 6. Latih model SVM ===
model = SVC(
    kernel="rbf",
    C=2,
    gamma="scale",
    class_weight="balanced",
    probability=True,
    random_state=42
)
model.fit(X_train_res, y_train_res)

# === 7. Evaluasi di data test ===
y_pred = model.predict(X_test_scaled)

print("\n=== HASIL EVALUASI MODEL SVM ===")
print("Akurasi :", accuracy_score(y_test, y_pred))
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred))

# === 8. Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred)
labels = sorted(y.unique())  # otomatis pakai urutan label dari data

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=labels,
    yticklabels=labels
)
plt.xlabel('Prediksi')
plt.ylabel('Aktual')
plt.title('Confusion Matrix SVM')
plt.tight_layout()
plt.show()

# === 9. Simpan model & scaler ===
joblib.dump(model, "model/svm_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

# === 10. Cek distribusi kelas ===
print("\nDistribusi awal data:")
print(y.value_counts())

print("\nDistribusi setelah SMOTE (data train):")
print(pd.Series(y_train_res).value_counts())
