import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Impostazioni estetiche
sns.set(style="whitegrid")

# ---------------------------------------------------------
# 1. CARICAMENTO DATASET SPORCO
# ---------------------------------------------------------
df = pd.read_csv("dataset_triage_sporco.csv")

# ---------------------------------------------------------
# 2. DISTRIBUZIONE DELLE CLASSI (DATASET SPORCO)
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="triage", palette="Set2")
plt.title("Distribuzione delle classi (dataset sporco)")
plt.xlabel("Triage")
plt.ylabel("Conteggio")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 3. VALORI MANCANTI PER COLONNA
# ---------------------------------------------------------
plt.figure(figsize=(10,5))
df.isnull().sum().plot(kind="bar", color="salmon")
plt.title("Valori mancanti per colonna")
plt.ylabel("Numero di valori mancanti")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 4. BOXPLOT SATURAZIONE (OUTLIER)
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.boxplot(x=df["saturazione"], color="skyblue")
plt.title("Boxplot saturazione (dataset sporco)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 5. BOXPLOT FREQUENZA CARDIACA
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.boxplot(x=df["frequenza_cardiaca"], color="lightgreen")
plt.title("Boxplot frequenza cardiaca (dataset sporco)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 6. HEATMAP DELLE CORRELAZIONI (CONVERSIONE NUMERICA)
# ---------------------------------------------------------
df_num = df.copy()

for col in df_num.columns:
    df_num[col] = pd.to_numeric(df_num[col], errors="coerce")

plt.figure(figsize=(10,7))
sns.heatmap(df_num.corr(), annot=True, cmap="coolwarm")
plt.title("Heatmap delle correlazioni (dataset sporco)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 7. RICREAZIONE DATASET PULITO (STESSO CLEANING DEL MODELLO)
# ---------------------------------------------------------
df_clean = df.copy()

# Rimozione duplicati
df_clean = df_clean.drop_duplicates()

# Rimozione righe completamente vuote
df_clean = df_clean.dropna(how="all")

# Conversione forzata a numerico
for col in ["saturazione", "frequenza_cardiaca",
            "dolore_toracico", "difficolta_respiratoria",
            "febbre", "trauma", "raffreddore"]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# Rimozione valori mancanti
df_clean = df_clean.dropna()

# Range fisiologici
df_clean = df_clean[(df_clean["saturazione"] >= 0) & (df_clean["saturazione"] <= 100)]
df_clean = df_clean[(df_clean["frequenza_cardiaca"] >= 20) & (df_clean["frequenza_cardiaca"] <= 250)]

# Clipping sintomi
for col in ["dolore_toracico", "difficolta_respiratoria",
            "febbre", "trauma", "raffreddore"]:
    df_clean[col] = df_clean[col].clip(0, 1)

# ---------------------------------------------------------
# 8. DISTRIBUZIONE DELLE CLASSI (DATASET PULITO)
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.countplot(data=df_clean, x="triage", palette="viridis")
plt.title("Distribuzione delle classi (dataset pulito)")
plt.xlabel("Triage")
plt.ylabel("Conteggio")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 9. CONFRONTO RIGHE PRIMA / DOPO CLEANING
# ---------------------------------------------------------
plt.figure(figsize=(6,5))
plt.bar(["Sporco", "Pulito"], [len(df), len(df_clean)], color=["red", "green"])
plt.title("Confronto dimensione dataset: sporco vs pulito")
plt.ylabel("Numero di righe")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 10. ISTOGRAMMA SATURAZIONE
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.histplot(df["saturazione"], kde=True, color="blue")
plt.title("Distribuzione saturazione (dataset sporco)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 11. ISTOGRAMMA FREQUENZA CARDIACA
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
sns.histplot(df["frequenza_cardiaca"], kde=True, color="orange")
plt.title("Distribuzione frequenza cardiaca (dataset sporco)")
plt.tight_layout()
plt.show()
