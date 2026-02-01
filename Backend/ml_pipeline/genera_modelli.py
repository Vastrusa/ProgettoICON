import pandas as pd
import joblib
import os

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# CARICA DATASET PULITO
# ---------------------------------------------------------

df = pd.read_csv("../data/dataset_pulito.csv")

# Debug utile: controlla eventuali NaN residui
print("Valori mancanti nel dataset pulito:")
print(df.isna().sum())

# ---------------------------------------------------------
# FEATURE PER ML E NAIVE BAYES
# ---------------------------------------------------------

FEATURES = [
    "saturazione",
    "frequenza_cardiaca",
    "dolore_toracico",
    "difficolta_respiratoria",
    "febbre",
    "trauma",
    "raffreddore"
]

X = df[FEATURES]
y = df["triage"]

# ---------------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------
# LOGISTIC REGRESSION MIGLIORATA
# ---------------------------------------------------------

log_clf = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial",
    class_weight="balanced"   # migliora la sensibilità sulle classi meno frequenti
)
log_clf.fit(X_train, y_train)

# ---------------------------------------------------------
# RANDOM FOREST MIGLIORATA
# ---------------------------------------------------------

rf_clf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",  # evita bias verso classi più frequenti
    n_jobs=-1                 # usa tutti i core → più veloce
)
rf_clf.fit(X_train, y_train)

# ---------------------------------------------------------
# NAIVE BAYES (Gaussian)
# ---------------------------------------------------------

nb_clf = GaussianNB()
nb_clf.fit(X_train, y_train)

# ---------------------------------------------------------
# SALVATAGGIO MODELLI
# ---------------------------------------------------------

os.makedirs("../models", exist_ok=True)

joblib.dump(log_clf, "../models/modello_logistico_triage.pkl")
joblib.dump(rf_clf, "../models/modello_random_forest_triage.pkl")
joblib.dump(nb_clf, "../models/naive_model.joblib")

print("Modelli ML salvati correttamente!")
