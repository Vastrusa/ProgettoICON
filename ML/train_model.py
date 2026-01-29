import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -----------------------------
# 1. Caricamento dataset SPORCO
# -----------------------------
df = pd.read_csv("dataset_triage_sporco.csv")

print("Dataset originale:", df.shape)

# -----------------------------
# 2. DATA CLEANING
# -----------------------------

# 2.1 Rimozione duplicati
df = df.drop_duplicates()

# 2.2 Rimozione righe completamente vuote
df = df.dropna(how="all")

# 2.3 Conversione forzata a numerico (stringhe → NaN)
for col in ["saturazione", "frequenza_cardiaca",
            "dolore_toracico", "difficolta_respiratoria",
            "febbre", "trauma", "raffreddore"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 2.4 Rimozione valori mancanti dopo conversione
df = df.dropna()

# 2.5 Correzione valori fuori range
df = df[(df["saturazione"] >= 0) & (df["saturazione"] <= 100)]
df = df[(df["frequenza_cardiaca"] >= 20) & (df["frequenza_cardiaca"] <= 250)]

# 2.6 Assicurare che i sintomi siano 0/1
for col in ["dolore_toracico", "difficolta_respiratoria",
            "febbre", "trauma", "raffreddore"]:
    df[col] = df[col].clip(0, 1)

print("Dataset pulito:", df.shape)

# -----------------------------
# 3. Separazione feature/target
# -----------------------------
X = df.drop("triage", axis=1)
y = df["triage"]

# -----------------------------
# 4. Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 5. Modello Random Forest
# -----------------------------
model = RandomForestClassifier(
    n_estimators=400,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# 6. Valutazione
# -----------------------------
y_pred = model.predict(X_test)

print("\nCONFUSION MATRIX:")
print(confusion_matrix(y_test, y_pred))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 7. Salvataggio modello
# -----------------------------
joblib.dump(model, "modello_triage.pkl")

print("\nModello salvato come modello_triage.pkl")
