import pandas as pd
import numpy as np

def genera_dataset_sporco(n=1500):
    np.random.seed(42)

    # Distribuzione realistica
    n_bianco = int(n * 0.40)
    n_verde = int(n * 0.40)
    n_giallo = int(n * 0.15)
    n_rosso = n - (n_bianco + n_verde + n_giallo)

    rows = []

    # -------------------------
    # BIANCO (40%)
    # -------------------------
    for _ in range(n_bianco):
        rows.append({
            "saturazione": np.random.randint(96, 101),
            "frequenza_cardiaca": np.random.randint(60, 101),
            "dolore_toracico": 0,
            "difficolta_respiratoria": 0,
            "febbre": np.random.choice([0, 1], p=[0.8, 0.2]),
            "trauma": 0,
            "raffreddore": np.random.choice([0, 1], p=[0.7, 0.3]),
            "triage": "Bianco"
        })

    # -------------------------
    # VERDE (40%)
    # -------------------------
    for _ in range(n_verde):
        rows.append({
            "saturazione": np.random.randint(92, 96),
            "frequenza_cardiaca": np.random.randint(100, 121),
            "dolore_toracico": 0,
            "difficolta_respiratoria": 0,
            "febbre": np.random.choice([0, 1], p=[0.4, 0.6]),
            "trauma": 0,
            "raffreddore": np.random.choice([0, 1], p=[0.4, 0.6]),
            "triage": "Verde"
        })

    # -------------------------
    # GIALLO (15%)
    # -------------------------
    for _ in range(n_giallo):
        rows.append({
            "saturazione": np.random.randint(90, 93),
            "frequenza_cardiaca": np.random.randint(120, 141),
            "dolore_toracico": np.random.choice([0, 1], p=[0.5, 0.5]),
            "difficolta_respiratoria": np.random.choice([0, 1], p=[0.6, 0.4]),
            "febbre": np.random.choice([0, 1], p=[0.5, 0.5]),
            "trauma": np.random.choice([0, 1], p=[0.8, 0.2]),
            "raffreddore": np.random.choice([0, 1], p=[0.6, 0.4]),
            "triage": "Giallo"
        })

    # -------------------------
    # ROSSO (5%)
    # -------------------------
    for _ in range(n_rosso):
        rows.append({
            "saturazione": np.random.randint(70, 90),
            "frequenza_cardiaca": np.random.randint(140, 181),
            "dolore_toracico": np.random.choice([0, 1], p=[0.3, 0.7]),
            "difficolta_respiratoria": np.random.choice([0, 1], p=[0.2, 0.8]),
            "febbre": np.random.choice([0, 1], p=[0.5, 0.5]),
            "trauma": np.random.choice([0, 1], p=[0.4, 0.6]),
            "raffreddore": np.random.choice([0, 1], p=[0.7, 0.3]),
            "triage": "Rosso"
        })

    df = pd.DataFrame(rows)

    # ----------------------------------------------------
    # AGGIUNTA DI RIGHE SPORCHE PER IL DATA CLEANING
    # ----------------------------------------------------

    sporche = []

    # saturazione impossibile
    r = df.iloc[0].copy()
    r["saturazione"] = 150
    sporche.append(r.to_dict())

    r = df.iloc[1].copy()
    r["saturazione"] = 20
    sporche.append(r.to_dict())

    # FC impossibile
    r = df.iloc[2].copy()
    r["frequenza_cardiaca"] = 5
    sporche.append(r.to_dict())

    r = df.iloc[3].copy()
    r["frequenza_cardiaca"] = 300
    sporche.append(r.to_dict())

    # sintomi incoerenti (tutti 1)
    r = df.iloc[4].copy()
    r["dolore_toracico"] = 1
    r["difficolta_respiratoria"] = 1
    r["febbre"] = 1
    r["trauma"] = 1
    r["raffreddore"] = 1
    sporche.append(r.to_dict())

    # sintomi tutti 0 ma triage rosso
    sporche.append({
        "saturazione": 98,
        "frequenza_cardiaca": 80,
        "dolore_toracico": 0,
        "difficolta_respiratoria": 0,
        "febbre": 0,
        "trauma": 0,
        "raffreddore": 0,
        "triage": "Rosso"
    })

    # valori mancanti
    sporche.append({
        "saturazione": np.nan,
        "frequenza_cardiaca": 110,
        "dolore_toracico": 1,
        "difficolta_respiratoria": 0,
        "febbre": 1,
        "trauma": 0,
        "raffreddore": 0,
        "triage": "Giallo"
    })

    # triage mancante
    sporche.append({
        "saturazione": 95,
        "frequenza_cardiaca": 90,
        "dolore_toracico": 0,
        "difficolta_respiratoria": 0,
        "febbre": 0,
        "trauma": 0,
        "raffreddore": 1,
        "triage": None
    })

    # riga duplicata
    sporche.append(df.iloc[10].to_dict())

    # Concat finale SENZA errori
    df_sporco = pd.concat([df, pd.DataFrame(sporche)], ignore_index=True)
    df_sporco = df_sporco.sample(frac=1).reset_index(drop=True)

    df_sporco.to_csv("dataset_sporco.csv", index=False)
    print("Dataset sporco generato: dataset_sporco.csv")

genera_dataset_sporco()
