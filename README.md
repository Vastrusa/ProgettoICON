🏥 Pronto Soccorso Intelligente
Progetto di Ingegneria della Conoscenza
Università degli Studi di Bari – Dipartimento di Informatica

👩‍💻 Autore
Valeria Agostinacchio  
Corso di Ingegneria della Conoscenza — Università degli Studi di Bari

📌 Descrizione del progetto
Il progetto implementa un sistema intelligente di triage per il Pronto Soccorso, basato su un’architettura ibrida che integra:
🧠 Regole cliniche (rule-based)
📚 Ontologia del triage (OWL) con reasoner Pellet
🔍 Knowledge Base in Prolog
🤖 Modelli di Machine Learning (Logistic Regression, Random Forest, Naive Bayes)
🎲 Rete Bayesiana discreta con 7 variabili e 672 combinazioni
🗺️ Algoritmo A\* per la simulazione dell’evoluzione clinica e la validazione del triage.
🖥️ Backend Flask per la gestione operativa
📊 Dashboard interattiva con grafici
📥 Importazione pazienti da file XML

L’obiettivo è supportare gli operatori sanitari nell’assegnazione del codice triage (Bianco, Verde, Giallo, Rosso) e nella gestione dinamica della coda, combinando conoscenza medica strutturata, ragionamento automatico e predizione statistica.

🧩 Architettura del sistema
🔹 Ontologia (OWL)
Modellazione formale del dominio del triage
Reasoning con Pellet
Mappatura proprietà tramite file .properties

🔹 Knowledge Base Prolog
Regole cliniche
Inferenza del codice triage
Integrazione con Python via pyswip

🔹 Machine Learning
Generazione dataset realistico
Gestione dello sbilanciamento tramite class_weight="balanced"
Addestramento modelli:
Logistic Regression
Random Forest
Naive Bayes
Valutazione performance
Predizione triage

🔹 Rete Bayesiana
Implementata con pgmpy
Variabili: saturazione, frequenza cardiaca, sintomi principali
672 combinazioni possibili
CPD esportate in JSON
Inferenza manuale tramite indice lineare
Output coerente con le 4 classi di triage

🔹 Algoritmo A\*
Simulazione dell’evoluzione clinica
Calcolo del percorso clinico a costo minimo
Validazione del codice di triage assegnato dagli altri moduli

🔹 Backend Flask
Inserimento pazienti
Calcolo triage tramite tutti i modelli
Gestione coda
Import XML
Persistenza tramite JSON
Il backend integra i risultati dei modelli tramite una logica di fusione e registra eventuali conflitti in conflitti.log.

🔹 Dashboard Web
Tabella pazienti in tempo reale
Grafici Chart.js
Stato della coda
Dettagli pazienti

📁 Struttura del progetto
Codice
ProntoSoccorsoIntelligente/
├── Backend/
│   ├── app.py
│   ├── coda.json
│   ├── prossimo.json
│   ├── prontoSoccorso.owl
│   ├── prontoSoccorso.properties
│   ├── triage.pl
│   ├── pazienti_test.xml
│   ├── conflitti.log
│   ├── bayes/
│   │   ├──__init__.py
│   │   ├── train_bayes.py
│   │   ├── export_cpd.py
│   │   ├── bayes_inference.py
│   ├── astar/
│   │   └── astar.py
│   ├── ml_pipeline/
│   │   ├── genera_dataset_sporco.py
│   │   ├── genera_modelli.py
│   │   └──clean_dataset.py
│   ├── data/
│   │   ├── dataset_pulito.csv
│   │   ├── dataset_sporco.csv
│   │   └── genera_dataset_bayes.py
│   ├── templates/
│   │   └── dashboard.html
│   ├── models/
│   │   ├──bayes_cpd.json  
│   │   ├──bayes_model.pkl 
│   │   ├──modello_logistico_triage.pkl
│   │   ├──modello_random_forest_triage.pkl
│   │   ├──naive_encoder.joblib
│   │   └──naive_model.joblib
├── requirements.txt
└── README.md
🚀 Come eseguire il progetto
1. Clona la repository
Codice
git clone https://github.com/tuo_username/ProgettoICON.git
cd ProgettoICON
2. Installa le dipendenze
Codice
pip install -r requirements.txt
3. Avvia il backend Flask
Codice
cd Backend
python app.py
4. Apri il browser
Codice
http://127.0.0.1:5000
🧪 Machine Learning
Rigenerare il modello ML
Codice
cd Backend/ml_pipeline
python genera_dataset_sporco.py
python clean_dataset.py
python genera_modelli.py

Rigenerare la rete Bayesiana
  cd Backend
  bayes_env\Scripts\activate
  python data/genera_dataset_bayes.py
  python bayes/train_bayes.py
  python bayes/export_cpd.py
  deactivate
📚 Tecnologie utilizzate
Python
Flask
Scikit-learn
Pandas
Matplotlib / Seaborn
pgmpy
Prolog (pyswip)
OWL / Protégé
A\* Search
HTML / Bootstrap / Chart.js

📄 Licenza
Progetto accademico — uso didattico.
