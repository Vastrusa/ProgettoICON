import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "dataset_pulito.csv")

np.random.seed(42)

def genera_sintomi(n):
    return {
        "dolore_toracico": np.random.binomial(1, 0.20, n),
        "difficolta_respiratoria": np.random.binomial(1, 0.25, n),
        "febbre": np.random.binomial(1, 0.30, n),
        "trauma": np.random.binomial(1, 0.10, n),
        "raffreddore": np.random.binomial(1, 0.35, n),
    }

def assegna_triage(row):
    sat = row["saturazione"]
    fc = row["frequenza_cardiaca"]
    dt = row["dolore_toracico"]
    dr = row["difficolta_respiratoria"]
    feb = row["febbre"]
    tra = row["trauma"]

    if sat < 90 or fc < 40 or fc > 140 or (dr == 1 and sat < 94):
        return "Rosso"

    if dt == 1 or dr == 1 or (feb == 1 and sat < 94):
        return "Giallo"

    if feb == 1 or tra == 1:
        return "Verde"

    return "Bianco"

def main():
    N = 5000

    sat = np.random.randint(85, 100, N)
    fc = np.random.randint(35, 150, N)
    sintomi = genera_sintomi(N)

    df = pd.DataFrame({
        "saturazione": sat,
        "frequenza_cardiaca": fc,
        "dolore_toracico": sintomi["dolore_toracico"],
        "difficolta_respiratoria": sintomi["difficolta_respiratoria"],
        "febbre": sintomi["febbre"],
        "trauma": sintomi["trauma"],
        "raffreddore": sintomi["raffreddore"],
    })

    df["triage"] = df.apply(assegna_triage, axis=1)

    df.to_csv(OUTPUT_PATH, index=False)
    print("Dataset salvato in:", OUTPUT_PATH)
    print(df["triage"].value_counts())

if __name__ == "__main__":
    main()
