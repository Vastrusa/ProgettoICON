from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "chiave_super_segreta"

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
# LABEL PER VISUALIZZAZIONE
# -------------------------
sintomi_label = {
    "DoloreToracico1": "Dolore toracico",
    "DifficoltaRespiratoria1": "Difficoltà respiratoria",
    "Febbre1": "Febbre",
    "Raffreddore1": "Raffreddore",
    "Trauma1": "Trauma"
}

saturazione_label = {
    "Saturazione1": "<90",
    "Saturazione2": "90-94",
    "Saturazione3": ">94"
}

fc_label = {
    "FC60-100": "60-100",
    "FC101-120": "101-120",
    "FC121-140": "121-140",
    "FCMaggiore140": ">140",
    "FC50-59": "50-59",
    "FC40-49": "40-49",
    "FCminore40": "<40"
}

# -------------------------
# CALCOLO TRIAGE
# -------------------------
def calcola_triage(sintomi_ids, sat_id, fc_id):
    triage_finale = "Bianco"

    triage_sintomi = {
        "DifficoltaRespiratoria1": "Rosso",
        "DoloreToracico1": "Rosso",
        "Febbre1": "Giallo",
        "Raffreddore1": "Bianco",
        "Trauma1": "Giallo"
    }

    triage_saturazione = {
        "Saturazione1": "Rosso",
        "Saturazione2": "Giallo",
        "Saturazione3": "Verde"
    }

    triage_fc = {
        "FCminore40": "Rosso",
        "FC40-49": "Giallo",
        "FC50-59": "Verde",
        "FC60-100": "Bianco",
        "FC101-120": "Verde",
        "FC121-140": "Giallo",
        "FCMaggiore140": "Rosso"
    }

    # Sintomi
    for s in sintomi_ids:
        if s in triage_sintomi:
            if priorita_map[triage_sintomi[s]] < priorita_map[triage_finale]:
                triage_finale = triage_sintomi[s]

    # Saturazione
    if sat_id and sat_id in triage_saturazione:
        if priorita_map[triage_saturazione[sat_id]] < priorita_map[triage_finale]:
            triage_finale = triage_saturazione[sat_id]

    # Frequenza cardiaca
    if fc_id and fc_id in triage_fc:
        if priorita_map[triage_fc[fc_id]] < priorita_map[triage_finale]:
            triage_finale = triage_fc[fc_id]

    return triage_finale

# -------------------------
# RICALCOLO POSIZIONI
# -------------------------
def ricalcola_posizioni(coda):
    for idx, p in enumerate(coda):
        if "ordine_arrivo" not in p:
            p["ordine_arrivo"] = idx

    coda.sort(key=lambda p: (p["priorita"], p["ordine_arrivo"]))

    for i, p in enumerate(coda):
        if p["codice"] == "Rosso":
            p["persone_prima"] = 0
        else:
            p["persone_prima"] = sum(1 for _ in coda[:i])

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

    return render_template(
        "dashboard.html",
        coda=coda,
        prossimo=prossimo,
        conteggi=conteggi,
        sintomi_label=sintomi_label,
        saturazione_label=saturazione_label,
        fc_label=fc_label
    )

@app.route("/aggiungi_paziente", methods=["POST"])
def aggiungi_paziente():
    nome = request.form.get("nome")

    sintomi = request.form.getlist("sintomi[]")
    if isinstance(sintomi, str):
        sintomi = [sintomi] if sintomi else []
    if sintomi is None:
        sintomi = []

    sat = request.form.get("saturazione") or ""
    fc = request.form.get("fc") or ""

    codice = calcola_triage(sintomi, sat, fc)
    priorita = priorita_map[codice]

    coda = carica_coda()

    coda.append({
        "nome": nome,
        "sintomi": sintomi,
        "saturazione": sat,
        "frequenza": fc,
        "codice": codice,
        "priorita": priorita,
        "ordine_arrivo": len(coda),
        "persone_prima": 0
    })

    ricalcola_posizioni(coda)
    salva_coda(coda)

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
    prossimo = coda[0]
    salva_prossimo(prossimo)

    coda = coda[1:]
    ricalcola_posizioni(coda)
    salva_coda(coda)

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
