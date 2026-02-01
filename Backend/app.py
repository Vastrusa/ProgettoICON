import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyswip import Prolog
from flask import Flask, render_template, request, redirect, url_for
import json
from uuid import uuid4
import joblib
import pandas as pd
import xml.etree.ElementTree as ET
from bayes.bayes_inference import predici_codice_bayes



from owlready2 import get_ontology, sync_reasoner_pellet, onto_path

# --- A* ---
from astar.a_star import a_star

app = Flask(__name__)
app.secret_key = "chiave_super_segreta"

# -------------------------
# CARICAMENTO MODELLI ML
# -------------------------
log_model = joblib.load("models/modello_logistico_triage.pkl")
rf_model = joblib.load("models/modello_random_forest_triage.pkl")

priority_ml = {"bianco": 0, "verde": 1, "giallo": 2, "rosso": 3}

def predici_codice_ml(sat, fc, dt, dr, feb, tra, raf):
    X = pd.DataFrame([{
        "saturazione": sat,
        "frequenza_cardiaca": fc,
        "dolore_toracico": dt,
        "difficolta_respiratoria": dr,
        "febbre": feb,
        "trauma": tra,
        "raffreddore": raf
    }])

    pred_log = log_model.predict(X)[0]
    pred_rf = rf_model.predict(X)[0]

    pred_log_norm = pred_log.lower()
    pred_rf_norm = pred_rf.lower()

    final_pred_norm = (
        pred_rf_norm
        if priority_ml[pred_rf_norm] > priority_ml[pred_log_norm]
        else pred_log_norm
    )

    return final_pred_norm.capitalize(), pred_log.capitalize(), pred_rf.capitalize()


# -------------------------
# NAIVE BAYES
# -------------------------
nb_model = joblib.load("models/naive_model.joblib")

def predici_codice_naive(sintomi_ids, sat_id, fc_id):
    # Sintomi → 1/0
    dispnea = 1 if ("DifficoltaRespiratoria1" in sintomi_ids or "Dispnea" in sintomi_ids) else 0
    dolore = 1 if "DoloreToracico1" in sintomi_ids else 0
    febbre = 1 if "Febbre1" in sintomi_ids else 0
    trauma = 1 if "Trauma1" in sintomi_ids else 0
    raffreddore = 1 if "Raffreddore1" in sintomi_ids else 0

    # Parametri vitali → valori numerici (come ML)
    sat_val = mappa_saturazione_valore(sat_id)
    fc_val = mappa_fc_valore(fc_id)

    df = pd.DataFrame([{
        "saturazione": sat_val,
        "frequenza_cardiaca": fc_val,
        "dolore_toracico": dolore,
        "difficolta_respiratoria": dispnea,
        "febbre": febbre,
        "trauma": trauma,
        "raffreddore": raffreddore
    }])

    pred = nb_model.predict(df)[0]
    return pred.capitalize()





# -------------------------
# ONTOLOGIA OWL
# -------------------------
onto_path.append(os.path.abspath(os.path.dirname(__file__)))
onto = get_ontology("ProntoSoccorso.owl").load()


# -------------------------
# PROLOG
# -------------------------
prolog = Prolog()
prolog.consult("triage.pl")


# -------------------------
# FILE CODA
# -------------------------
CODA_FILE = "coda.json"
PROSSIMO_FILE = "prossimo.json"

def carica_coda():
    if not os.path.exists(CODA_FILE):
        return []
    with open(CODA_FILE, "r") as f:
        return json.load(f)

def salva_coda(coda):
    with open(CODA_FILE, "w") as f:
        json.dump(coda, f, indent=4)

def carica_prossimo():
    if not os.path.exists(PROSSIMO_FILE):
        return None
    with open(PROSSIMO_FILE, "r") as f:
        return json.load(f)

def salva_prossimo(p):
    with open(PROSSIMO_FILE, "w") as f:
        json.dump(p, f, indent=4)


# -------------------------
# PRIORITÀ TRIAGE
# -------------------------
priorita_map = {"Rosso": 1, "Giallo": 2, "Verde": 3, "Bianco": 4}


# -------------------------
# LABELS
# -------------------------
sintomi_label = {
    "DoloreToracico1": "Dolore toracico",
    "DifficoltaRespiratoria1": "Difficoltà respiratoria",
    "Febbre1": "Febbre",
    "Raffreddore1": "Raffreddore",
    "Trauma1": "Trauma",
}

saturazione_label = {
    "Saturazione1": "<90",
    "Saturazione2": "90-94",
    "Saturazione3": ">94",
}

fc_label = {
    "FC60-100": "60-100",
    "FC101-120": "101-120",
    "FC121-140": "121-140",
    "FCMaggiore140": ">140",
    "FC50-59": "50-59",
    "FC40-49": "40-49",
    "FCminore40": "<40",
}


# -------------------------
# OWL TRIAGE
# -------------------------
def codice_ontologia(sintomi_ids, sat_id, fc_id):
    with onto:
        paz_name = f"Paz_{uuid4().hex}"
        Paziente = onto.Paziente
        paz = Paziente(paz_name)

        for s in sintomi_ids:
            ind = getattr(onto, s, None)
            if ind:
                paz.presenzaSintomo.append(ind)

        if sat_id:
            sat_ind = getattr(onto, sat_id, None)
            if sat_ind:
                paz.haParametroVitale.append(sat_ind)

        if fc_id:
            fc_ind = getattr(onto, fc_id, None)
            if fc_ind:
                paz.haParametroVitale.append(fc_ind)

        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

        if paz.assegnatoCodiceTriage:
            mapping = {
                "triageRosso": "Rosso",
                "triageGiallo": "Giallo",
                "triageVerde": "Verde",
                "triageBianco": "Bianco",
    }

    codici = [mapping.get(ind.name, "Bianco") for ind in paz.assegnatoCodiceTriage]

    priorita = {"Rosso": 4, "Giallo": 3, "Verde": 2, "Bianco": 1}

    return max(codici, key=lambda c: priorita[c])

    return "Bianco"


# -------------------------
# ML MAPPING
# -------------------------
def mappa_saturazione_valore(sat_id):
    return {"Saturazione1": 85, "Saturazione2": 92, "Saturazione3": 97}.get(sat_id, 98)

def mappa_fc_valore(fc_id):
    return {
        "FC60-100": 80,
        "FC101-120": 110,
        "FC121-140": 130,
        "FCMaggiore140": 150,
        "FC50-59": 55,
        "FC40-49": 45,
        "FCminore40": 35,
    }.get(fc_id, 80)

def mappa_sintomi_flags(sintomi_ids):
    return (
        1 if "DoloreToracico1" in sintomi_ids else 0,
        1 if "DifficoltaRespiratoria1" in sintomi_ids else 0,
        1 if "Febbre1" in sintomi_ids else 0,
        1 if "Trauma1" in sintomi_ids else 0,
        1 if "Raffreddore1" in sintomi_ids else 0,
    )


# -------------------------
# PROLOG
# -------------------------
def normalizza_id(nome):
    return nome.strip().replace(" ", "_").lower() or f"paz_{uuid4().hex}"

def mappa_sintomo_prolog(s):
    mapping = {
        "DoloreToracico1": "dolore_toracico",
        "DifficoltaRespiratoria1": "difficolta_respiratoria",
        "Febbre1": "febbre",
        "Raffreddore1": "raffreddore",
        "Trauma1": "trauma",
    }
    return mapping.get(s, s.lower())

def codice_prolog(pid, sintomi_ids, sat_val, fc_val):
    for s in sintomi_ids:
        prolog.assertz(f"sintomo({pid}, {mappa_sintomo_prolog(s)})")

    prolog.assertz(f"parametro({pid}, saturazione, {sat_val})")
    prolog.assertz(f"parametro({pid}, fc, {fc_val})")

    res = list(prolog.query(f"codice({pid}, C)"))
    if res:
        mapping = {
            "rosso": "Rosso",
            "giallo": "Giallo",
            "verde": "Verde",
            "bianco": "Bianco",
        }
        return mapping.get(str(res[0]["C"]), "Bianco")

    return "Bianco"


# -------------------------
# A*
# -------------------------
def mappa_sintomi_astar(sintomi_ids):
    sintomi = []

    if "DifficoltaRespiratoria1" in sintomi_ids:
        sintomi.append("dispnea")
    if "DoloreToracico1" in sintomi_ids:
        sintomi.append("dolore_toracico")
    if "Febbre1" in sintomi_ids:
        sintomi.append("febbre")
    if "Trauma1" in sintomi_ids:
        sintomi.append("trauma")

    return sintomi

def codice_astar(sintomi_ids, sat_val, fc_val):
    start_state = {
        "sat": sat_val,
        "fc": fc_val,
        "sintomi": mappa_sintomi_astar(sintomi_ids),
    }

    return a_star(start_state)


# -------------------------
# RICALCOLO POSIZIONI
# -------------------------
def ricalcola_posizioni(coda):
    for idx, p in enumerate(coda):
        p.setdefault("ordine_arrivo", idx)

    coda.sort(key=lambda p: (p["priorita"], p["ordine_arrivo"]))

    for i, p in enumerate(coda):
        p["persone_prima"] = 0 if p["codice"] == "Rosso" else i


# -------------------------
# IMPORTAZIONE XML
# -------------------------
def importa_pazienti_da_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for p in root.findall("Paziente"):
        nome = p.find("Nome").text

        sintomi = []
        for s in p.find("Sintomi").findall("Sintomo"):
            sintomi.append(s.text)

        sat_id = p.find("Saturazione").text
        fc_id = p.find("Frequenza").text

        aggiungi_paziente_backend(nome, sintomi, sat_id, fc_id)


# -------------------------
# AGGIUNTA PAZIENTE BACKEND
# -------------------------
def aggiungi_paziente_backend(nome, sintomi, sat_id, fc_id):
    codice_rule = codice_ontologia(sintomi, sat_id, fc_id)
    priorita = priorita_map[codice_rule]

    sat_val = mappa_saturazione_valore(sat_id)
    fc_val = mappa_fc_valore(fc_id)
    dt, dr, feb, tra, raf = mappa_sintomi_flags(sintomi)

    codice_ml_finale, codice_log, codice_rf = predici_codice_ml(
        sat_val, fc_val, dt, dr, feb, tra, raf
    )

    pid = normalizza_id(nome)
    codice_pl = codice_prolog(pid, sintomi, sat_val, fc_val)

    codice_a = codice_astar(sintomi, sat_val, fc_val)

    codice_naive = predici_codice_naive(sintomi, sat_id, fc_id)

    codice_bayes = predici_codice_bayes(sintomi, sat_id, fc_id)


    if (
        codice_ml_finale != codice_rule
        or codice_pl != codice_rule
        or codice_a != codice_rule
        or codice_naive != codice_rule
        or codice_bayes != codice_rule
    ):
        with open("conflitti.log", "a") as log:
            log.write(
                f"{nome} | OWL: {codice_rule} | ML: {codice_ml_finale} "
                f"(Log:{codice_log}, RF:{codice_rf}) | Prolog: {codice_pl} "
                f"| A*: {codice_a} | Naive: {codice_naive} | Bayes: {codice_bayes}\n"
            )


    coda = carica_coda()
    coda.append(
        {
            "nome": nome,
            "sintomi": sintomi,
            "saturazione": sat_id,
            "frequenza": fc_id,
            "codice": codice_rule,
            "codice_ml": codice_ml_finale,
            "codice_log": codice_log,
            "codice_rf": codice_rf,
            "codice_prolog": codice_pl,
            "codice_astar": codice_a,
            "codice_naive": codice_naive,
            "codice_bayes": codice_bayes,
            "priorita": priorita,
            "ordine_arrivo": len(coda),
            "persone_prima": 0,
        }
    )

    ricalcola_posizioni(coda)
    salva_coda(coda)


# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    coda = carica_coda()
    prossimo = carica_prossimo()

    conteggi = {"Rosso": 0, "Giallo": 0, "Verde": 0, "Bianco": 0}
    for p in coda:
        conteggi[p["codice"]] += 1

    conflitti = sum(
        1
        for p in coda
        if p.get("codice_ml")
        and p.get("codice_prolog")
        and p.get("codice_astar")
        and p.get("codice_naive")
        and p.get("codice_bayes")
        and (
            p["codice_ml"] != p["codice"]
            or p["codice_prolog"] != p["codice"]
            or p["codice_astar"] != p["codice"]
            or p["codice_naive"] != p["codice"]
            or p["codice_bayes"] != p["codice"]
        )
    )

    return render_template(
        "dashboard.html",
        coda=coda,
        prossimo=prossimo,
        conteggi=conteggi,
        conflitti=conflitti,
        sintomi_label=sintomi_label,
        saturazione_label=saturazione_label,
        fc_label=fc_label,
    )


@app.route("/aggiungi_paziente", methods=["POST"])
def aggiungi_paziente():
    nome = request.form.get("nome")
    sintomi = request.form.getlist("sintomi[]") or []
    sat_id = request.form.get("saturazione") or ""
    fc_id = request.form.get("fc") or ""

    aggiungi_paziente_backend(nome, sintomi, sat_id, fc_id)

    return redirect(url_for("dashboard"))


@app.route("/elimina_paziente/<nome>", methods=["POST"])
def elimina_paziente(nome):
    coda = carica_coda()
    coda = [p for p in coda if p["nome"] != nome]
    ricalcola_posizioni(coda)
    salva_coda(coda)
    return redirect(url_for("dashboard"))


@app.route("/prossimo_paziente", methods=["POST"])
def prossimo_paziente():
    coda = carica_coda()
    if not coda:
        return redirect(url_for("dashboard"))

    ricalcola_posizioni(coda)
    prossimo = coda.pop(0)
    salva_prossimo(prossimo)
    ricalcola_posizioni(coda)
    salva_coda(coda)

    return redirect(url_for("dashboard"))


@app.route("/importa_xml", methods=["POST"])
def importa_xml():
    file = request.files["file"]
    importa_pazienti_da_xml(file)

    coda = carica_coda()
    ricalcola_posizioni(coda)
    salva_coda(coda)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
