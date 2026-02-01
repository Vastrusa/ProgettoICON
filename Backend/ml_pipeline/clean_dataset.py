import pandas as pd

# ---------------------------------------------------------
# FUNZIONE PER CONVERTIRE SI/NO IN 1/0
# ---------------------------------------------------------

def binarizza(val):
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ["yes", "si", "true", "1"]:
            return 1
        if v in ["no", "false", "0", "", "none", "nan"]:
            return 0
    return int(val) if not pd.isna(val) else 0


# ---------------------------------------------------------
# FUNZIONE PER ASSEGNARE IL CODICE TRIAGE
# ---------------------------------------------------------

def assegna_codice_triage(row):
    sat = row["saturazione"]
    fc = row["frequenza_cardiaca"]
    dt = row["dolore_toracico"]
    dr = row["difficolta_respiratoria"]
    feb = row["febbre"]
    tra = row["trauma"]
    raf = row["raffreddore"]

    # ROSSO
    if dr == 1:
        return "Rosso"
    if dt == 1:
        return "Rosso"
    if sat < 90:
        return "Rosso"
    if fc > 140 or fc < 40:
        return "Rosso"

    # GIALLO
    if tra == 1:
        return "Giallo"
    if 90 <= sat <= 94:
        return "Giallo"
    if 121 <= fc <= 140:
        return "Giallo"
    if 40 <= fc <= 49:
        return "Giallo"

    # VERDE
    if feb == 1:
        return "Verde"
    if sat > 94:
        return "Verde"
    if 50 <= fc <= 59:
        return "Verde"
    if 100 <= fc <= 120:
        return "Verde"

    # BIANCO
    if raf == 1:
        return "Bianco"
    if 60 <= fc <= 100:
        return "Bianco"

    return "Bianco"


# ---------------------------------------------------------
# CARICA DATASET SPORCO
# ---------------------------------------------------------

df = pd.read_csv("../data/dataset_sporco.csv")

# ---------------------------------------------------------
# BINARIZZA TUTTI I SINTOMI
# ---------------------------------------------------------

for col in ["dolore_toracico", "difficolta_respiratoria", "febbre", "trauma", "raffreddore"]:
    df[col] = df[col].apply(binarizza)

# ---------------------------------------------------------
# CONVERSIONE PARAMETRI VITALI
# ---------------------------------------------------------

df["saturazione"] = pd.to_numeric(df["saturazione"], errors="coerce").fillna(0)
df["frequenza_cardiaca"] = pd.to_numeric(df["frequenza_cardiaca"], errors="coerce").fillna(0)

# ---------------------------------------------------------
# ASSEGNAZIONE CODICE TRIAGE
# ---------------------------------------------------------

df["triage"] = df.apply(assegna_codice_triage, axis=1)

# ---------------------------------------------------------
# SALVA DATASET PULITO
# ---------------------------------------------------------

df.to_csv("../data/dataset_pulito.csv", index=False)

print("Dataset pulito generato correttamente!")
