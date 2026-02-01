from heapq import heappush, heappop

def state_key(state):
    return (
        state["sat"],
        state["fc"],
        tuple(sorted(state["sintomi"])),
        state["step"]
    )

def is_goal_state(state):
    return state["step"] == "done"

def heuristic(state):
    # Heuristica semplice: più grave = più vicino al goal
    if state["step"] == "check_rosso":
        return 0
    if state["step"] == "check_giallo":
        return 1
    if state["step"] == "check_verde":
        return 2
    return 3

def get_neighbors(state):
    sat = state["sat"]
    fc = state["fc"]
    sintomi = state["sintomi"]
    step = state["step"]

    neighbors = []

    # -------------------------
    # STEP 1: ROSSO
    # -------------------------
    if step == "check_rosso":
        if "dispnea" in sintomi or "dolore_toracico" in sintomi or sat < 90 or fc > 140 or fc < 40:
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "done", "codice": "Rosso"},
                1
            ))
        else:
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "check_giallo"},
                1
            ))

    # -------------------------
    # STEP 2: GIALLO
    # -------------------------
    elif step == "check_giallo":
        if "trauma" in sintomi or (90 <= sat <= 94) or (121 <= fc <= 140) or (40 <= fc <= 49):
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "done", "codice": "Giallo"},
                1
            ))
        else:
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "check_verde"},
                1
            ))

    # -------------------------
    # STEP 3: VERDE
    # -------------------------
    elif step == "check_verde":
        if "febbre" in sintomi or sat > 94 or (50 <= fc <= 59) or (100 <= fc <= 120):
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "done", "codice": "Verde"},
                1
            ))
        else:
            neighbors.append((
                {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "check_bianco"},
                1
            ))

    # -------------------------
    # STEP 4: BIANCO
    # -------------------------
    elif step == "check_bianco":
        neighbors.append((
            {"sat": sat, "fc": fc, "sintomi": sintomi, "step": "done", "codice": "Bianco"},
            1
        ))

    return neighbors

def a_star(start_state):
    start_state["step"] = "check_rosso"

    open_set = []
    heappush(open_set, (0, start_state))

    g_score = {state_key(start_state): 0}

    while open_set:
        _, current = heappop(open_set)

        if is_goal_state(current):
            return current["codice"]

        for neighbor, cost in get_neighbors(current):
            nk = state_key(neighbor)
            tentative = g_score[state_key(current)] + cost

            if nk not in g_score or tentative < g_score[nk]:
                g_score[nk] = tentative
                f = tentative + heuristic(neighbor)
                heappush(open_set, (f, neighbor))

    return "Bianco"
