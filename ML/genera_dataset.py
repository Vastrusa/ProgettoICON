import random
import pandas as pd
import numpy as np

# -----------------------------
# Funzione per assegnare triage
# -----------------------------
def assegna_triage(sat, fc, dolore, dispnea, febbre, trauma, raffreddore):

    # Rosso
    if (
        fc > 140 or fc < 40 or
        sat < 90 or
        dolore == 1 or
        dispnea == 1 or
        trauma == 1
    ):
        return "Rosso"

    # Giallo
    if (
        121 <= fc <= 140 or
        40 <= fc <= 49 or
        90 <= sat <= 94 or
        febbre == 1
    ):
        return "Giallo"

    # Bianco per raffreddore semplice
    if raffreddore == 1 and sat > 94:
        return "Bianco"

    # Verde
    if (
        101 <= fc <= 120 or
        50 <= fc <= 59 or
        sat > 94
    ):
        return "Verde"

    # Bianco
    if 60 <= fc <= 100:
        return "Bianco"

    return "Bianco"


# -----------------------------
# Generazione dataset sporco
# -----------------------------
def genera_dataset_sporco(n=2000):
    dati = []

    for i in range(n):

        # Valori realistici
        sat = random.randint(70, 100)
        fc = random.randint(30, 180)

        # AUMENTO probabilità di casi VERDI e BIANCHI
        dolore = random.choices([0, 1], weights=[0.95, 0.05])[0]
        dispnea = random.choices([0, 1], weights=[0.90, 0.10])[0]
        febbre = random.choices([0, 1], weights=[0.80, 0.20])[0]
        trauma = random.choices([0, 1], weights=[0.97, 0.03])[0]
        raffreddore = random.choices([0, 1], weights=[0.50, 0.50])[0]

        triage = assegna_triage(sat, fc, dolore, dispnea, febbre, trauma, raffreddore)

        dati.append({
            "saturazione": sat,
            "frequenza_cardiaca": fc,
            "dolore_toracico": dolore,
            "difficolta_respiratoria": dispnea,
            "febbre": febbre,
            "trauma": trauma,
            "raffreddore": raffreddore,
            "triage": triage
        })

    df = pd.DataFrame(dati)

    # -----------------------------
    # INTRODUZIONE ERRORI REALISTICI
    # -----------------------------

    # 1. Valori mancanti (ridotti al 3%)
    for col in df.columns:
        df.loc[df.sample(frac=0.03).index, col] = np.nan

    # 2. Saturazioni fuori range (1%)
    df.loc[df.sample(frac=0.01).index, "saturazione"] = random.choice([150, -10, 300])

    # 3. Frequenze cardiache impossibili (1%)
    df.loc[df.sample(frac=0.01).index, "frequenza_cardiaca"] = random.choice([-20, 500])

    # 4. Sintomi non binari (2%)
    df.loc[df.sample(frac=0.02).index, "febbre"] = random.choice(["yes", "no", "maybe"])

    # 5. Duplicati (20 righe)
    df = pd.concat([df, df.sample(20)], ignore_index=True)

    return df


# -----------------------------
# Creazione e salvataggio CSV
# -----------------------------
df = genera_dataset_sporco(2000)
df.to_csv("dataset_triage_sporco.csv", index=False)

print("Dataset SPORCO generato correttamente!")
print(df.head(20))
