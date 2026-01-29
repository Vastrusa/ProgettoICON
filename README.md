# ProgettoICON
# 🏥 Sistema di Triage Intelligente  
Progetto di Ingegneria della Conoscenza e Machine Learning  
Università degli Studi di Bari – Dipartimento di Informatica

---

## 📌 Descrizione del progetto

Questo progetto implementa un **sistema intelligente di triage per il Pronto Soccorso**, integrando:

- 🧠 Regole cliniche (rule-based)  
- 📚 Ontologia del triage (OWL)  
- 🔍 Knowledge Base in Prolog  
- 🤖 Modello di Machine Learning supervisionato  
- 🖥️ Backend Flask per la gestione della coda pazienti  
- 📊 Dashboard interattiva con grafici in tempo reale  

L’obiettivo è supportare gli operatori sanitari nell’assegnazione del **codice triage** (Rosso, Giallo, Verde, Bianco) e nella gestione della coda, combinando conoscenza medica strutturata e predizione automatica.

---

## 📁 Struttura del progetto
ProntoSoccorsoIntelligente
├── backend/
│   ├── app.py
│   ├── coda.json
│   ├── prossimo.json
│   ├── prontoSoccorso.owl
│   ├── prontoSoccorso.properties
│   ├── templates/
│   │   └── dashboard.html
│
├── ml/
│   ├── dataset_triage_sporco.csv
│   ├── genera_dataset.py
│   ├── grafici_dataset.py
│   ├── train_model.py
│   ├── modello_triage.pkl
│   └── predict.py
│
├── requirements.txt
└── README.md
