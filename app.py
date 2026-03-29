import tkinter as tk
from tkinter import ttk
from reportlab.pdfgen import canvas
from diagnose_engine import berechne_diagnose, score_einordnung



KONTEXT = "Organisation"
TON = "reflexiv"
# Beispiel-Fragen
bereiche = [
{

    "name": "Verantwortungslogik",
     "fragen":[
         {"text": "Entscheidungen haben klare Verantwortlichkeiten.", "reverse": False},
         {"text": "Zustaendigkeiten sind eindeutig geklaert.", "reverse": False},
         {"text": "Themen bleiben oft ohne Abschluss.", "reverse": True}
     ]
},
{
    "name": "Psychologische Sicherheit",
    "fragen":[
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

gesamt_fragen = sum(len(b["fragen"]) for b in bereiche)

bereich_index = 0
frage_index = 0
antworten = []

bereich_scores = []
bereich_antworten = []
reflexion_text = ""

beantwortete_fragen = 0

#Logik

def berechne_score(werte):
    return sum(werte) / len(werte)

def update_progress():
    fortschritt = int((beantwortete_fragen / gesamt_fragen) * 100)
    if beantwortete_fragen >= gesamt_fragen:
        fortschritt = 100
    progress_bar["value"] = fortschritt

    progress_label.config(
        text=f"Fortschritt: {beantwortete_fragen} / {gesamt_fragen}"
    )

def set_text(text):
    frage_label.config(state="normal")
    frage_label.delete("1.0", tk.END)
    frage_label.insert("1.0", text)
    frage_label.config(state="disabled")

def aktuelle_frage_text():
    return bereiche[bereich_index]["fragen"][frage_index]["text"]


def antwort_gewaehlt(wert):
    global frage_index, bereich_index
    global beantwortete_fragen

    beantwortete_fragen += 1
    update_progress()
    update_bereich_label()

    frage = bereiche[bereich_index]["fragen"][frage_index]

    #Reverse-Logik
    if frage["reverse"]:
        wert = 6 - wert
    antworten.append(wert)
    bereich_antworten.append(wert)
    zeige_status()

    frage_index += 1

    # Naechste Frage im gleichen Bereich
    if frage_index < len(bereiche[bereich_index]["fragen"]):
        update_bereich_label()
        set_text(aktuelle_frage_text())

    else:
        #Score fuer aktuellen Bereich berechnen
        score = berechne_score(bereich_antworten)
        bereich_scores.append(score)
        bereich_antworten.clear()

        set_text(
            f"Vielen Dank.\n\nDer Bereich '{bereiche[bereich_index]['name']}' "
            "ist abgeschlossen.\n\nDer naechste Abschnitt beginnt."
        )
        fenster.after(1200, lambda: None)

        #naechster Bereich
        bereich_index += 1
        frage_index = 0

        if bereich_index < len(bereiche):
            bereich_label.config(
                text=f"Bereich {bereich_index+1} von {len(bereiche)} - {bereiche[bereich_index]['name']}"
            )
            set_text(
                f"Vielen Dank.\n\nDer Bereich '{bereiche[bereich_index-1]['name']}' "
                "ist abgeschlossen.\n\nDer naechste Abschnitt beginnt."
            )

            fenster.after(1200, starte_naechsten_bereich)
        else:
            button_frame.pack_forget()
            update_progress()

            zeige_reflexionsfrage()
    
def update_bereich_label():
    gesamt_bereiche = len(bereiche)
    gesamt_fragen_bereich = len(bereiche[bereich_index]["fragen"])
    fortschritt = int(progress_bar["value"])


    bereich_label.config(
        text=(
            f"Bereich {bereich_index+1} von {gesamt_bereiche} - {bereiche[bereich_index]['name']}\n"
            f"Frage {frage_index+1} von {gesamt_fragen_bereich}\n"
            f"Fortschritt: {fortschritt}%"

        )
    )

def starte_naechsten_bereich():
    global frage_index

    frage_index = 0
    update_bereich_label()
    set_text(aktuelle_frage_text())

def zeige_status ():
    if frage_index >= len(bereiche[bereich_index]["fragen"]) - 1:
        if bereich_index + 1 < len(bereiche):
            bereich_name = bereiche[bereich_index + 1]["name"]
        else:
            bereich_name = bereiche[bereich_index]["name"]
    else: 
        bereich_name = bereiche[bereich_index]["name"]

    texte = {
        "Verantwortungslogik":
        "Danke - weiter zur naechsten Einschaetzung bzgl. Verantwortung.",
        "Psychologische Sicherheit":
        "Danke - weiter zur naechsten Einschaetzung bzgl. Zusammenarbeit",
        "Fuehrungswirksamkeit":
        "Danke - weiter zur naechsten Einschaetzung bzgl. Fuehrung."
    }

    text = texte.get(
        bereich_name,
        "Danke - weiter zur naechsten Einschaetzung."

    )

    status_label.config(text=text)
    fenster.after(900, lambda: status_label.config(text=""))

def zeige_reflexionsfrage():
    button_frame.pack_forget()

    frage = (
        "Welche konkrete Situation aus Ihrem Arbeitsalltag "
        "passt zu dieser Diagnose?\n\n"
        "Beschreiben Sie kurz ein Beispiel."
    )

    set_text(frage)
    reflexion_eingabe.focus_set()
    frage_label.config(height=8)
    reflexion_frame.pack(pady=10)


def speichere_reflexion():
    global reflexion_text

    reflexion_text = reflexion_eingabe.get("1.0", tk.END).strip()

    reflexion_frame.pack_forget()

    zeige_ergebnis()

def export_pdf(text):
    file_name = "diagnosebericht.pdf"

    c = canvas.Canvas(file_name)

    y = 800

    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15

        if y < 50:
            c.showPage()
            y = 800

    c.save()

def zeige_ergebnis():
    

    vd, ps, fw = bereich_scores
    diagnose = berechne_diagnose (vd, ps, fw, KONTEXT, TON)

    muster = diagnose["muster"]
    sekundaer = diagnose["sekundaeres_muster"]
    staerke = diagnose["staerke"]

    ergebnis_text = "EXECUTIVE SUMMARY\n\n"
    ergebnis_text += f"Kontext der Diagnose: {KONTEXT}\n\n"

    ergebnis_text += f"Dominantes Systemmuster: {muster} ({staerke})\n\n"
    if sekundaer and sekundaer != muster:
        ergebnis_text += f"Sekundaeres Muster: {sekundaer}\n"

    ergebnis_text += "\n"
    ergebnis_text += diagnose["summary"]

    ergebnis_text += "\n\n---\n\nDETAILERGEBNISSE\n\n"
    
    ergebnis_text += (
        "Die folgenden Werte dienen lediglich als Orientierung.\n"
        "Entscheidend ist, welche Situationen aus Ihrem organisationalen "
        "Alltag Sie wiedererkennen.\n\n"
    )
    sekundaer = diagnose["sekundaeres_muster"]

    if sekundaer and sekundaer != muster:
        ergebnis_text += f"\nSekundaeres Muster: {sekundaer}\n"
    for i, score in enumerate(bereich_scores):
        name = bereiche[i]["name"]
        einordnung = score_einordnung(score)
        ergebnis_text += f"{name}: {round(score, 2)} ({einordnung})\n"

    if reflexion_text:
        ergebnis_text += "\n\n---\n\nIhre Reflexion:\n"
        ergebnis_text += reflexion_text

    ergebnis_text += (
        "\n\n---\n\n"
        "Diagnose abgeschlossen.\n"
        "Sie koennen das Fenster nun schliessen "
        "oder eine neue Diagnose starten."
    )

    set_text(ergebnis_text)
    restart_button.pack(pady=10)
    export_button.pack(pady=5)

#------------------------------
# GUI
#------------------------------

fenster = tk.Tk()
fenster.title("Systemische Organisationsdiagnose")
fenster.geometry("600x500")

fenster.resizable(True, True)

def show_error(self, exc, val, tb):
    import traceback
    message = "".join(traceback.format_exception(exc, val, tb))
    set_text("Ein technischer Fehler ist aufgetreten:\n\n" + message)
fenster.report_callback_exception = show_error

titel = tk.Label(
    fenster,
    text="Systemische Organisationsdiagnose",
    font=("Helvetica", 16)
)
titel.pack(pady=20)

progress_label = tk.Label(
    fenster,
    text="Fortschritt: 0 / 9",
    font=("Helvetica", 10)
)
progress_label.pack()

progress_bar = ttk.Progressbar(
    fenster,
    orient="horizontal",
    length=300,
    mode="determinate"
)

progress_bar.pack(pady=5)

start_text = tk.Label(
    fenster,
    text=(
        "Diese Diagnose hilft dabei, systemische Muster in Verantwortung,\n"
        "psychologischer Sicherheit und Fuehrungswirksamkeit sichtbar zu machen.\n\n"
        "Sie dient der Reflexion organisationaler Dynamiken\n"
        "und stellt keine Bewertung einzelner Personen dar."
    ),
    font=("Helvetica", 12),
    justify="center"
)
start_text.pack(pady=30)

kontext_frame = tk.Frame(fenster)
kontext_frame.pack()

kontext_var = tk.StringVar(value="Organisation")

text_label = tk.Label(
    kontext_frame,
    text="Kontext der Diagnose:",
    font=("Helvetica", 12)
)
text_label.pack(pady=(10,5))

tk.Radiobutton(
    kontext_frame,
    text="Gesamtorganisation",
    variable=kontext_var,
    value="Organisation"
).pack()

tk.Radiobutton(
    kontext_frame,
    text="Führungsteam",
    variable=kontext_var,
    value="Führungsteam"

).pack()

def diagnose_starten():
    global KONTEXT
    KONTEXT = kontext_var.get()

    weiter_button.pack_forget()
    start_text.pack_forget()
    start_button.pack_forget()
    kontext_frame.pack_forget()
    

    update_bereich_label()
    bereich_label.pack()
    text_frame.pack(pady=20)
    button_frame.pack()

    set_text(aktuelle_frage_text())

def reset_diagnose():
    global bereich_index, frage_index
    global antworten, bereich_scores, bereich_antworten
    global beantwortete_fragen
    beantwortete_fragen = 0

    progress_label.config(text="Fortschritt: 0 / 9")
    progress_bar["value"] = 0

    #Werte zuruecksetzen
    bereich_index = 0
    frage_index = 0

    antworten.clear()
    bereich_scores.clear()
    bereich_antworten.clear()

    #Diagnose-UI ausblenden
    restart_button.pack_forget()
    bereich_label.pack_forget()
    text_frame.pack_forget()
    button_frame.pack_forget()
    
    # Startscreen wieder anzeigen
    start_text.pack(pady=30)
    kontext_frame.pack()
    start_button.pack()

def diagnose_einfuehrung():
    #Startscreen ausblenden
    start_text.pack_forget()
    start_button.pack_forget()
    kontext_frame.pack_forget()

    #Textbereich sichtbar machen
    text_frame.pack(pady=20)
    einfuehrung_text = (
        "Die Diagnose beginnt jetzt.\n\n"
        "Beantworten Sie bitte im Folgenden kurze Aussagen zu\n"
        "Verantwortung, psychologischer Sicherheit und Fuehrung.\n\n"
        "Es gibt keine richtigen oder falschen Antworten.\n"
        "Entscheidend ist Ihre aktuelle Wahrnehmung.\n\n"
        "Klicken Sie auf 'Weiter', um zu starten."
    )

    set_text(einfuehrung_text)

    weiter_button.pack(pady=10)

start_button = tk.Button(
    fenster,
    text="Diagnose starten",
    font=("Helvetica", 12),
    command=diagnose_einfuehrung
)
start_button.pack()

restart_button = tk.Button(
    fenster,
    text="Neue Diagnose starten",
    font=("Helvetica", 11),
    command=reset_diagnose
)
weiter_button = tk.Button(
    fenster,
    text="Weiter",
    font=("Helvetica", 11),
    command=diagnose_starten
)

export_button = tk.Button(
    fenster,
    text="Bericht als PDF speichern",
    font=("Helvetica", 11),
    command=lambda: export_pdf(frage_label.get("1.0", tk.END))
)

bereich_label = tk.Label(
    fenster,
    text=f"Bereich 1 von {len(bereiche)} - {bereiche[0]['name']}",
    font=("Helvetica", 11)
)
# bereich_label.pack()

text_frame = tk.Frame(fenster)
 # text_frame.pack(pady=20)

scrollbar = tk.Scrollbar(text_frame)

frage_label = tk.Text(
    text_frame,
    wrap="word",
    font=("Helvetica", 12),
    height=10,
    width=70,
    yscrollcommand=scrollbar.set
)

reflexion_frame = tk.Frame(fenster)

reflexion_eingabe = tk.Text(
    reflexion_frame,
    height=4,
    width=60
)

reflexion_eingabe.pack()

reflexion_button = tk.Button(
    reflexion_frame,
    text="Weiter zur Auswertung",
    command=speichere_reflexion
)

reflexion_button.pack(pady=5)

status_label = tk.Label(
    fenster,
    text="",
    font=("Helvetica", 10),
    fg="gray"
)
status_label.pack()

scrollbar.config(command=frage_label.yview)

scrollbar.pack(side="right", fill="y")
frage_label.pack(side="left")

frage_label.insert("1.0", aktuelle_frage_text())
frage_label.config(state="disabled")

button_frame = tk.Frame(fenster)
# button_frame.pack()

for i in range(1, 6):
    btn = tk.Button(
        button_frame,
        text=str(i),
        width=5,
        command=lambda wert=i: antwort_gewaehlt(wert)
    )
    btn.grid(row=0, column=i-1, padx=5)
fenster.mainloop()
