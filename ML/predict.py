import joblib
import pandas as pd

# -----------------------------
# Funzione per valori neutri
# -----------------------------
def valori_neutri():
    return {
        "saturazione": 98,
        "frequenza_cardiaca": 80,
        "dolore_toracico": 0,
        "difficolta_respiratoria": 0,
        "febbre": 0,
        "trauma": 0,
        "raffreddore": 0
    }

# -----------------------------
# 1. Caricamento modello
# -----------------------------
model = joblib.load("modello_triage.pkl")

# -----------------------------
# 2. Inserimento dati utente
# -----------------------------
print("Inserisci i dati del paziente (premi invio per lasciare vuoto):\n")

sat = input("Saturazione (%): ")
fc = input("Frequenza cardiaca (bpm): ")
dolore = input("Dolore toracico (0=no, 1=sì): ")
dispnea = input("Difficoltà respiratoria (0=no, 1=sì): ")
febbre = input("Febbre (0=no, 1=sì): ")
trauma = input("Trauma (0=no, 1=sì): ")
raffreddore = input("Raffreddore (0=no, 1=sì): ")

# -----------------------------
# 3. Gestione valori vuoti
# -----------------------------
base = valori_neutri()

sat = int(sat) if sat else base["saturazione"]
fc = int(fc) if fc else base["frequenza_cardiaca"]
dolore = int(dolore) if dolore else base["dolore_toracico"]
dispnea = int(dispnea) if dispnea else base["difficolta_respiratoria"]
febbre = int(febbre) if febbre else base["febbre"]
trauma = int(trauma) if trauma else base["trauma"]
raffreddore = int(raffreddore) if raffreddore else base["raffreddore"]

# -----------------------------
# 4. Creazione DataFrame
# -----------------------------
dati_input = pd.DataFrame([{
    "saturazione": sat,
    "frequenza_cardiaca": fc,
    "dolore_toracico": dolore,
    "difficolta_respiratoria": dispnea,
    "febbre": febbre,
    "trauma": trauma,
    "raffreddore": raffreddore
}])

# -----------------------------
# 5. Predizione
# -----------------------------
predizione = model.predict(dati_input)[0]

print("\n---------------------------")
print(f"⚕️  Triage previsto: **{predizione}**")
print("---------------------------")
