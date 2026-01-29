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

ProntoSoccorsoIntelligente/
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

---

## 🚀 Funzionalità principali

### 🔹 Backend Flask
- Inserimento pazienti  
- Calcolo triage rule-based  
- Integrazione con modello ML  
- Gestione coda con priorità  
- Chiamata del prossimo paziente  
- Persistenza tramite file JSON  

### 🔹 Dashboard
- Tabella pazienti aggiornata in tempo reale  
- Grafico distribuzione triage  
- Visualizzazione sintomi e parametri vitali  

### 🔹 Machine Learning
- Pulizia dataset  
- Generazione dataset bilanciato  
- Analisi grafica  
- Addestramento modello  
- Predizione codice triage  

### 🔹 Ontologia e KB
- Ontologia del triage in OWL  
- Mappatura proprietà  
- Regole cliniche in Prolog  
- Query e aggiornamento KB  

---

## ▶️ Come eseguire il progetto

### 1. Clona la repository
git clone https://github.com/tuo_username/ProgettoICON.git
cd ProgettoICON

### 2. Installa le dipendenze
pip install -r requirements.txt

### 3. Avvia il backend Flask
cd backend
python app.py

### 4. Apri il browser
http://127.0.0.1:5000

---

## 🧪 Machine Learning

### Rigenerare il modello
cd ml
python genera_dataset.py
python grafici_dataset.py
python train_model.py

### Effettuare una predizione
python predict.py

---

## 📚 Tecnologie utilizzate

- Python  
- Flask  
- Scikit-learn  
- Pandas  
- Matplotlib  
- Prolog (pyswip)  
- OWL / Protégé  
- HTML / Bootstrap / Chart.js  

---

## 👩‍💻 Autore
Valeria — Università degli Studi di Bari  
Corso di Ingegneria della Conoscenza

---

## 📄 Licenza
Progetto accademico — uso didattico.
