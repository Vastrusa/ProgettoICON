% ---------------------------------------------------------
% BASE DI CONOSCENZA PROLOG PER IL TRIAGE
% ---------------------------------------------------------

:- dynamic sintomo/2.
:- dynamic parametro/3.

% ---------------------------------------------------------
% CODICE ROSSO
% ---------------------------------------------------------

% Difficoltà respiratoria → Rosso
codice(P, rosso) :-
    sintomo(P, difficolta_respiratoria), !.

% Dolore toracico → Rosso
codice(P, rosso) :-
    sintomo(P, dolore_toracico), !.

% Saturazione < 90 → Rosso
codice(P, rosso) :-
    parametro(P, saturazione, V),
    V < 90, !.

% Frequenza cardiaca > 140 → Rosso
codice(P, rosso) :-
    parametro(P, fc, V),
    V > 140, !.

% Frequenza cardiaca < 40 → Rosso
codice(P, rosso) :-
    parametro(P, fc, V),
    V < 40, !.

% ---------------------------------------------------------
% CODICE GIALLO
% ---------------------------------------------------------

% Trauma → Giallo
codice(P, giallo) :-
    sintomo(P, trauma), !.

% Saturazione 90–94 → Giallo
codice(P, giallo) :-
    parametro(P, saturazione, V),
    V >= 90, V =< 94, !.

% Frequenza cardiaca 121–140 → Giallo
codice(P, giallo) :-
    parametro(P, fc, V),
    V >= 121, V =< 140, !.

% Frequenza cardiaca 40–49 → Giallo
codice(P, giallo) :-
    parametro(P, fc, V),
    V >= 40, V =< 49, !.

% ---------------------------------------------------------
% CODICE VERDE
% ---------------------------------------------------------

% Febbre → Verde
codice(P, verde) :-
    sintomo(P, febbre), !.

% Saturazione > 94 → Verde
codice(P, verde) :-
    parametro(P, saturazione, V),
    V > 94, !.

% Frequenza cardiaca 50–59 → Verde
codice(P, verde) :-
    parametro(P, fc, V),
    V >= 50, V =< 59, !.

% Frequenza cardiaca 100–120 → Verde
codice(P, verde) :-
    parametro(P, fc, V),
    V >= 100, V =< 120, !.

% ---------------------------------------------------------
% CODICE BIANCO
% ---------------------------------------------------------

% Raffreddore → Bianco
codice(P, bianco) :-
    sintomo(P, raffreddore), !.

% Frequenza cardiaca 60–100 → Bianco
codice(P, bianco) :-
    parametro(P, fc, V),
    V >= 60, V =< 100, !.

% Default → Bianco
codice(_, bianco).
