import os
import pandas as pd
import joblib
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_pulito.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "bayes_model.pkl")

def discretizza_sat(val):
    if val < 90:
        return "<90"
    elif 90 <= val <= 94:
        return "90-94"
    else:
        return ">94"

def discretizza_fc(val):
    if val < 40:
        return "<40"
    elif 40 <= val <= 49:
        return "40-49"
    elif 50 <= val <= 59:
        return "50-59"
    elif 60 <= val <= 100:
        return "60-100"
    elif 101 <= val <= 120:
        return "101-120"
    elif 121 <= val <= 140:
        return "121-140"
    else:
        return ">140"

def main():
    print("Caricamento dataset:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)

    # Discretizzazione
    df["sat_cat"] = df["saturazione"].apply(discretizza_sat)
    df["fc_cat"] = df["frequenza_cardiaca"].apply(discretizza_fc)

    # Manteniamo solo le colonne utili
    df = df[[
        "sat_cat", "fc_cat",
        "dolore_toracico", "difficolta_respiratoria",
        "febbre", "trauma", "raffreddore",
        "triage"
    ]]

    # 🔥 CONVERSIONE OBBLIGATORIA PER PGMPY
    categorical_cols = ["sat_cat", "fc_cat", "triage"]
    for col in categorical_cols:
        df[col] = df[col].astype("category")

    print("Inizializzazione rete bayesiana...")
    model = DiscreteBayesianNetwork([
        ("sat_cat", "triage"),
        ("fc_cat", "triage"),
        ("dolore_toracico", "triage"),
        ("difficolta_respiratoria", "triage"),
        ("febbre", "triage"),
        ("trauma", "triage"),
        ("raffreddore", "triage"),
    ])

    print("Addestramento rete bayesiana...")
    model.fit(df, estimator=MaximumLikelihoodEstimator)

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Modello salvato in:", MODEL_PATH)

if __name__ == "__main__":
    main()
