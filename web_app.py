import streamlit as st

from diagnose_engine import (

    berechne_diagnose,
    score_einordnung,
    typische_auswirkungen,
    einordnung_text

)

# -------------------------
# Session State INIT
# -------------------------

if "gestartet" not in st.session_state:
    st.session_state.gestartet = False

if "frage_index" not in st.session_state:

    st.session_state.frage_index = 0

if "bereich_index" not in st.session_state:

    st.session_state.bereich_index = 0
if "antworten" not in st.session_state:

    st.session_state.antworten = []


# -------------------------
# Daten
# -------------------------

bereiche = [

   {

        "name": "Verantwortungslogik",
       "fragen": [

            {"text": "Entscheidungen haben klare Verantwortlichkeiten.", "reverse": False},

           {"text": "Zustaendigkeiten sind eindeutig geklaert.", "reverse": False},

            {"text": "Themen bleiben oft ohne Abschluss.", "reverse": True}

        ]

    },

    {

        "name": "Psychologische Sicherheit",

        "fragen": [

            {"text": "Schwierigkeiten werden stets offen angesprochen.", "reverse": False},

            {"text": "In Meetings sagen oft viele nicht, was sie wirklich denken.", "reverse": True},

            {"text": "Fehler koennen ohne negative Konsequenzen benannt werden.", "reverse": False}

        ]

    },

    {

        "name": "Fuehrungswirksamkeit",

        "fragen": [

            {"text": "Strategische Orientierung ist im Alltag klar erkennbar.", "reverse": False},

            {"text": "Fuehrung kommuniziert Erwartungen klar und konsistent.", "reverse": False},

            {"text": "Strategie und taegliche Arbeit sind oft entkoppelt.", "reverse": True}

        ]

    }

]
# -------------------------

# STARTSCREEN

# -------------------------

st.title("Systemische Organisationsdiagnose")

if not st.session_state.gestartet:

    st.write("""

    Diese Diagnose macht sichtbar, wie Verantwortung, psychologische Sicherheit 
    und Fuehrungswirksamkeit im Alltag Ihres Fuehrungsteams zusammenwirken 
    und welche Auswirkungen das auf Entscheidung und Umsetzung hat.

    """)



    kontext = st.radio(

        "Kontext der Diagnose:",

        ["Organisation", "Fuehrungsteam"]

    )
    if st.button("Diagnose starten"):

        st.session_state.gestartet = True

        st.session_state.kontext = kontext

        st.rerun()

    st.stop()
# -------------------------
# ERGEBNIS (wenn fertig)
# -------------------------

if st.session_state.bereich_index >= len(bereiche):
    st.success("Diagnose abgeschlossen")

    idx = 0

    bereich_scores = []

    for bereich in bereiche:

        werte = []

        for frage in bereich["fragen"]:

            werte.append(st.session_state.antworten[idx])

            idx += 1

        bereich_scores.append(sum(werte) / len(werte))

    vd, ps, fw = bereich_scores

    diagnose = berechne_diagnose(

        vd, ps, fw,

        kontext=st.session_state.get("kontext", "Organisation"),

        ton="reflexiv"

    )
    muster = diagnose["muster"]
    st.header("Ergebnis")
    st.subheader("Systemische Einordnung")
    zeilen = [zeile.strip() for zeile in diagnose["summary"].splitlines()]
    bereinigt = "\n".join(zeilen)
    for absatz in bereinigt.split("\n\n"):
        st.write(absatz.strip())
    auswirkungen = typische_auswirkungen(muster)

    if auswirkungen:

        st.subheader("Typische Auswirkungen im Alltag")

        st.markdown("\n".join(f"- {punkt}" for punkt in auswirkungen))

    st.subheader("Einordnung")

    st.write(einordnung_text())

    st.subheader("Detailwerte")

    labels = [

        "Verantwortungslogik",
        "Psychologische Sicherheit",
        "Fuehrungswirksamkeit"
    ]

    for name, score in zip(labels, bereich_scores):

        st.write(f"{name}: {round(score,2)} ({score_einordnung(score)})")

    st.markdown("---")
    st.subheader("Weiterführende Einordnung")
    st.write("""

    Die Ergebnisse geben erste Hinweise auf zugrunde liegende Dynamiken. 
    Erfahrungsgemaess zeigt sich die eigentliche Wirkung jedoch erst im gemeinsamen
    Blick des Fuehrungsteams auf konkrete Situationen. 
    Ich unterstütze Sie gern dabei, die Ergebnisse einzuordnen und konkrete Ansatzpunkte für Ihre Organisation abzuleiten.

    """)

    if st.button("Ergebnisse gemeinsam einordnen"):

        st.markdown("[Termin für Einordnungsgespräch buchen](https://calendly.com/anja-nestler/30min)")
    st.stop()

# -------------------------
# FRAGENLOGIK
# -------------------------

bereich = bereiche[st.session_state.bereich_index]
frage = bereich["fragen"][st.session_state.frage_index]
gesamt_fragen = sum(len(b["fragen"]) for b in bereiche)

beantwortet = len(st.session_state.antworten)

st.progress(beantwortet / gesamt_fragen)

st.subheader(bereich["name"])

wert = st.slider(

    frage["text"],

    1,
    5,
    3,

    key=f"slider_{st.session_state.bereich_index}_{st.session_state.frage_index}"

)


if st.button("Weiter"):
    if frage["reverse"]:

        wert = 6 - wert
    st.session_state.antworten.append(wert)

    st.session_state.frage_index += 1

    if st.session_state.frage_index >= len(bereich["fragen"]):

        st.session_state.frage_index = 0

        st.session_state.bereich_index += 1

    st.rerun()