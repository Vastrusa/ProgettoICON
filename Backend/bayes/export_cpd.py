import os
import json
import joblib
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "bayes_model.pkl")
OUTPUT_PATH = os.path.join(BASE_DIR, "models", "bayes_cpd.json")

model = joblib.load(MODEL_PATH)

def to_python(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

cpd_dict = {}

for cpd in model.get_cpds():
    variable = cpd.variables[0]
    evidence = cpd.variables[1:]
    cardinalities = cpd.cardinality

    cpd_dict[variable] = {
        "variable": variable,
        "cardinality": int(cardinalities[0]),
        "evidence": evidence,
        "evidence_card": [int(c) for c in cardinalities[1:]],
        "values": to_python(cpd.values)
    }

with open(OUTPUT_PATH, "w") as f:
    json.dump(cpd_dict, f, indent=4)

print("CPD salvate in:", OUTPUT_PATH)
