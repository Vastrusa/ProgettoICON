import os
import json
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CPD_PATH = os.path.join(BASE_DIR, "models", "bayes_cpd.json")

with open(CPD_PATH, "r") as f:
    CPDS = json.load(f)

# 🔥 Appiattiamo il tensore in liste 1D per ogni classe
def flatten(values):
    flat = []
    def rec(x):
        if isinstance(x, list):
            for e in x:
                rec(e)
        else:
            flat.append(x)
    rec(values)
    return flat

# Pre-elaboriamo le CPD
triage_cpd = CPDS["triage"]
raw_values = triage_cpd["values"]

# 🔥 Ora abbiamo 4 liste piatte, una per classe
FLAT_VALUES = [flatten(raw_values[c]) for c in range(4)]

def sat_id_to_index(sat_id):
    return {"Saturazione1": 0, "Saturazione2": 1, "Saturazione3": 2}.get(sat_id, 2)

def fc_id_to_index(fc_id):
    mapping = {
        "FCminore40": 0, "FC40-49": 1, "FC50-59": 2,
        "FC60-100": 3, "FC101-120": 4,
        "FC121-140": 5, "FCMaggiore140": 6
    }
    return mapping.get(fc_id, 3)

def predici_codice_bayes(sintomi_ids, sat_id, fc_id):
    dispnea = 1 if "DifficoltaRespiratoria1" in sintomi_ids else 0
    dolore = 1 if "DoloreToracico1" in sintomi_ids else 0
    febbre = 1 if "Febbre1" in sintomi_ids else 0
    trauma = 1 if "Trauma1" in sintomi_ids else 0
    raffreddore = 1 if "Raffreddore1" in sintomi_ids else 0

    evidence = {
        "difficolta_respiratoria": dispnea,
        "dolore_toracico": dolore,
        "fc_cat": fc_id_to_index(fc_id),
        "febbre": febbre,
        "raffreddore": raffreddore,
        "sat_cat": sat_id_to_index(sat_id),
        "trauma": trauma,
    }

    evidence_vars = triage_cpd["evidence"]
    evidence_card = triage_cpd["evidence_card"]

    # 🔥 Calcolo indice lineare
    index = 0
    multiplier = 1

    for var, card in reversed(list(zip(evidence_vars, evidence_card))):
        index += evidence[var] * multiplier
        multiplier *= card

    # 🔥 Ora possiamo indicizzare senza errori
    probs = [FLAT_VALUES[c][index] for c in range(4)]

    labels = ["Bianco", "Verde", "Giallo", "Rosso"]
    return labels[int(np.argmax(probs))]
