"""
diagnose_report.py
Generiert einen PDF-Ergebnisbericht fuer die Systemische Organisationsdiagnose.
Wird von der Streamlit-App aufgerufen, nachdem die Mail-Adresse eingegeben wurde.
"""

from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)

# ———————––
# Farben
# ———————––

DUNKELBLAU = colors.HexColor("#1B2A4A")
MITTELBLAU = colors.HexColor("#2E5090")
HELLGRAU   = colors.HexColor("#F4F4F4")
TEXTGRAU   = colors.HexColor("#333333")

# ———————––
# Styles
# ———————––

def erstelle_styles():
    styles = {
        "titel": ParagraphStyle(
            "Titel",
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=DUNKELBLAU,
            spaceAfter=6,
            leading=24,
        ),
        "untertitel": ParagraphStyle(
            "Untertitel",
            fontName="Helvetica",
            fontSize=11,
            textColor=MITTELBLAU,
            spaceAfter=18,
            leading=16,
        ),
        "section": ParagraphStyle(
            "Section",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=DUNKELBLAU,
            spaceBefore=18,
            spaceAfter=6,
            leading=16,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXTGRAU,
            spaceAfter=6,
            leading=15,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXTGRAU,
            spaceAfter=4,
            leading=14,
            leftIndent=14,
            bulletIndent=0,
        ),
        "footer": ParagraphStyle(
            "Footer",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=4,
            leading=12,
        ),
        "score_label": ParagraphStyle(
            "ScoreLabel",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=DUNKELBLAU,
            leading=14,
        ),
        "score_value": ParagraphStyle(
            "ScoreValue",
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXTGRAU,
            leading=14,
        ),
    }
    return styles

# ———————––
# Hilfsfunktionen
# ———————––

def score_einordnung(score):
    if score >= 4:
        return "hoch"
    elif score >= 3:
        return "mittel"
    else:
        return "niedrig"

def bullet(text, styles):
    return Paragraph(f"•   {text}", styles["bullet"])

def hr():
    return HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.HexColor("#CCCCCC"),
        spaceAfter=8,
        spaceBefore=4,
    )

# ———————––
# Inhaltliche Texte je Muster
# ———————––

def einordnung_im_kontext(muster, kontext):
    texte = {
        "Anpassung": {
            "Fuehrungsteam": [
                "Im Fuehrungsteam ist im Alltag nicht immer klar, wer Verantwortung tatsaechlich uebernimmt. Gleichzeitig wird nicht jede Situation als ausreichend sicher erlebt, um Spannungen offen anzusprechen.",
                "Verantwortung wird haeufig individuell getragen, ohne durchgaengig klar strukturell verankert zu sein.",
                "So entsteht eher Zurueckhaltung als offene Klaerung, wodurch Spannungen bestehen bleiben koennen.",
            ],
            "Organisation": [
                "In der Organisation ist im Alltag nicht immer klar, wer Verantwortung tatsaechlich uebernimmt. Gleichzeitig wird nicht jede Situation als ausreichend sicher erlebt, um Spannungen offen anzusprechen.",
                "Verantwortung wird haeufig individuell getragen, ohne durchgaengig klar strukturell verankert zu sein.",
                "So entsteht eher Zurueckhaltung als offene Klaerung, wodurch Spannungen bestehen bleiben koennen.",
            ],
        },
        "Schutz und Inkonsistenz": {
            "Fuehrungsteam": [
                "Im Fuehrungsteam wird nicht jede Situation als ausreichend sicher erlebt, um offen zu sprechen. Gleichzeitig wirkt Orientierung nicht immer konsistent.",
                "Erwartungen bleiben teilweise unklar oder werden unterschiedlich interpretiert.",
                "So entsteht eher Vorsicht als gestaltende Verantwortung im Alltag.",
            ],
            "Organisation": [
                "In der Organisation wird nicht jede Situation als ausreichend sicher erlebt, um offen zu sprechen. Gleichzeitig wirkt Orientierung nicht immer konsistent.",
                "Erwartungen bleiben teilweise unklar oder werden unterschiedlich interpretiert.",
                "So entsteht eher Vorsicht als gestaltende Verantwortung im Alltag.",
            ],
        },
        "Strukturproblem": {
            "Fuehrungsteam": [
                "Im Fuehrungsteam sind Verantwortung und Orientierung im Alltag nicht immer eindeutig geklaert.",
                "Entscheidungen koennen sich dadurch verzoegern oder werden mehrfach aufgegriffen.",
                "Resultierende Zielkonflikte bleiben teilweise unausgesprochen und werden nicht systematisch bearbeitet.",
            ],
            "Organisation": [
                "In der Organisation sind Verantwortung und Orientierung im Alltag nicht immer eindeutig geklaert.",
                "Entscheidungen koennen sich dadurch verzoegern oder werden mehrfach aufgegriffen.",
                "Resultierende Zielkonflikte bleiben teilweise unausgesprochen und werden nicht systematisch bearbeitet.",
            ],
        },
        "Stabil": {
            "Fuehrungsteam": [
                "Im Fuehrungsteam sind Verantwortung, Sicherheit und Fuehrung grundsaetzlich tragfaehig ausgepraegt.",
                "Zusammenarbeit ermoeglicht offene Klaerung und gemeinsame Wirksamkeit.",
            ],
            "Organisation": [
                "In der Organisation sind Verantwortung, Sicherheit und Fuehrung grundsaetzlich tragfaehig ausgepraegt.",
                "Zusammenarbeit ermoeglicht offene Klaerung und bereichsuebergreifende Zusammenarbeit.",
            ],
        },
        "Gemischtes Muster": {
            "Fuehrungsteam": [
                "Im Fuehrungsteam zeigen sich sowohl stabile als auch spannungsanfaellige Muster.",
                "Einzelne Bereiche funktionieren gut, waehrend andere inkonsistent oder klaerungsbeduerftig wirken.",
            ],
            "Organisation": [
                "In der Organisation zeigen sich sowohl stabile als auch spannungsanfaellige Muster.",
                "Einzelne Bereiche funktionieren gut, waehrend andere inkonsistent oder klaerungsbeduerftig wirken.",
            ],
        },
    }
    return texte.get(muster, {}).get(kontext, [])

def systemische_muster_texte(muster):
    texte = {
        "Anpassung": [
            "Im Alltag wird Verantwortung haeufig einzelnen Personen zugeschrieben, ohne dass immer klar ist, wie sie strukturell verankert ist.",
            "Auch Probleme werden eher einzelnen individuell zugerechnet als im Zusammenspiel von Rollen und Rahmenbedingungen betrachtet.",
            "Konflikte bleiben oft unausgesprochen, waehrend Loyalitaet wichtiger erscheint als offene Klaerung.",
            "Inhaltliche Themen und strategische Zielstellungen kommen langsamer voran, weil Zustaendigkeiten nicht immer eindeutig benannt sind.",
        ],
        "Schutz und Inkonsistenz": [
            "Orientierung wirkt im Alltag nicht immer eindeutig. Erwartungen bleiben teilweise unausgesprochen.",
            "Mitarbeitende agieren daher eher vorsichtig und vermeiden es, Risiken offen anzusprechen.",
            "Unklare oder ambivalente Kommunikation fuehrt eher zu Zurueckhaltung als zu Verantwortung.",
            "Entscheidungen werden formal getroffen, aber nicht immer von allen innerlich mitgetragen.",
        ],
        "Strukturproblem": [
            "Nicht immer ist klar, wer Entscheidungen treffen darf oder soll.",
            "Verantwortung wird uebertragen, ohne dass Mandat oder Rueckendeckung vollstaendig gesichert sind.",
            "Manche Themen wandern zwischen Rollen hin und her, ohne verbindlich abgeschlossen zu werden.",
            "Partikularinteressen stehen gelegentlich staerker im Vordergrund als die gemeinsame Gesamtverantwortung.",
        ],
        "Stabil": [
            "Verantwortung ist klar zugeordnet und wird im Alltag sichtbar uebernommen.",
            "Spannungen koennen offen angesprochen und konstruktiv bearbeitet werden.",
            "Fuehrung gibt Orientierung, ohne in Mikromanagement zu verfallen.",
            "Zusammenarbeit richtet sich erkennbar an gemeinsamen Zielen aus.",
        ],
        "Gemischtes Muster": [
            "Einige Bereiche wirken klar und stabil, andere eher unklar oder spannungsanfaellig.",
            "Psychologische Sicherheit ist situativ vorhanden, aber nicht ueberall gleich ausgepraegt.",
            "Fuehrung wirkt in Teilen orientierend, in anderen Bereichen uneinheitlich.",
            "Entwicklungspotenzial liegt darin, diese unterschiedlichen Muster bewusster zu integrieren.",
        ],
    }
    return texte.get(muster, [])

def entwicklungshebel(vd, ps, fw):
    hebel = []
    if vd < 3:
        hebel += [
            "Verantwortungsdialog zwischen Rollen fuehren: wer entscheidet final, wer traegt die Umsetzung?",
            "Gegenseitige Erwartungen explizit machen statt implizit voraussetzen.",
            "Verantwortung strukturell verankern, nicht personalisieren.",
        ]
    if ps < 3:
        hebel += [
            "Fuehrung spricht Unsicherheiten, Fehler und Spannungen sichtbar an.",
            "Implizite Risiken und Zielkonflikte koennen besprechbar gemacht werden.",
            "Psychologische Sicherheit durch konsistentes Verhalten, nicht nur durch Appelle staerken.",
        ]
    if fw < 3:
        hebel += [
            "Fuehrung formuliert klare Erwartungen und priorisiert sichtbar.",
            "Inkonsistenzen zwischen Anspruch und gelebter Praxis koennen gemeinsam reflektiert werden.",
            "Gemeinsames Zielbild regelmaessig mit operativer Realitaet in Verbindung bringen.",
        ]
    if vd >= 3 and ps >= 3 and fw >= 3:
        hebel += [
            "Bestehende Wirksamkeit gezielt weiterentwickeln statt nur stabilisieren.",
            "Lernfaehigkeit und bereichsuebergreifende Zusammenarbeit weiter vertiefen.",
        ]
    return hebel

def gesamtbild(muster, kontext, auspraegung):
    texte = {
        "Stabil": {
            "Fuehrungsteam": [
                "Das Fuehrungsteam wirkt insgesamt stabil mit guten Voraussetzungen fuer Weiterentwicklung.",
                "Gemeinsame Orientierung und Verantwortung tragen zur kollektiven Fuehrungswirksamkeit bei.",
                "Entwicklung kann dort ansetzen, wo vorhandene Staerken bewusst genutzt und weiter vertieft werden.",
            ],
            "Organisation": [
                "Das System wirkt insgesamt stabil mit guten Voraussetzungen fuer Weiterentwicklung.",
                "Verantwortung, Orientierung und Klaerung tragen zur gemeinsamen Wirksamkeit bei.",
                "Entwicklung kann dort ansetzen, wo vorhandene Staerken bewusst genutzt und weiter vertieft werden.",
            ],
        },
        "Anpassung": {
            "Fuehrungsteam": [
                "Das Fuehrungsteam wirkt eher spannungsgebunden und stabilisiert sich durch Anpassung statt Klaerung.",
                "Unklare Erwartungshaltungen verlangsamen gemeinsame Ausrichtung und Wirksamkeit.",
                "Entwicklung kann dort ansetzen, wo Verantwortung, Erwartungen und offene Klaerung im Fuehrungsteam gestaerkt werden.",
            ],
            "Organisation": [
                "Das System wirkt eher spannungsgebunden und stabilisiert sich durch Anpassung statt Klaerung.",
                "Unklare Verantwortung und zurueckhaltende Klaerung behindern gemeinsame Wirksamkeit.",
                "Entwicklung kann dort ansetzen, wo Verantwortung, Erwartungen und offene Klaerung bewusster gestaerkt werden.",
            ],
        },
        "Schutz und Inkonsistenz": {
            "Fuehrungsteam": [
                "Das Fuehrungsteam zeigt Unsicherheit und inkonsistente Orientierung, wodurch kollektive Fuehrungswirksamkeit begrenzt bleibt.",
                "Widerspruechliche Signale im Fuehrungshandeln foerdern eher Reaktivitaet als gemeinsame Ausrichtung.",
                "Entwicklung kann dort ansetzen, wo Orientierung, Konsistenz und offene Rueckmeldung im Fuehrungsteam gestaerkt werden.",
            ],
            "Organisation": [
                "Das System zeigt Unsicherheit und inkonsistente Orientierung, wodurch kollektive Wirksamkeit begrenzt bleibt.",
                "Widerspruechliche Signale und wechselnde Prioritaeten foerdern eher Reaktivitaet als gemeinsame Ausrichtung.",
                "Entwicklung kann dort ansetzen, wo Orientierung, Konsistenz und offene Rueckmeldung bewusster gestaerkt werden.",
            ],
        },
        "Strukturproblem": {
            "Fuehrungsteam": [
                "Das Fuehrungsteam wirkt strukturell unklar, was kollektive Verantwortung und Umsetzung erschwert.",
                "Unklare Rollen- und Entscheidungslogiken verhindern durchgaengige Verbindlichkeit.",
                "Entwicklung kann dort ansetzen, wo Mandate, Entscheidungswege und kollektive Verantwortung geklaert werden.",
            ],
            "Organisation": [
                "Das System wirkt strukturell unklar, was Verantwortung und Umsetzung erschwert.",
                "Unklare Rollen, Mandate und Entscheidungswege fuehren dazu, dass Themen nicht durchgaengig verbindlich vorankommen.",
                "Entwicklung kann dort ansetzen, wo Verantwortung, Entscheidungslogik und strukturelle Klarheit bewusst gestaerkt werden.",
            ],
        },
        "Gemischtes Muster": {
            "Fuehrungsteam": [
                "Das Fuehrungsteam zeigt ein gemischtes Bild mit stabilen und spannungsanfaelligen Bereichen.",
                "Unterschiedliche Fuehrungsdynamiken wirken parallel und fuehren zu inkonsistenter Ausrichtung.",
                "Entwicklung kann dort ansetzen, wo diese Muster im Fuehrungsteam bewusster integriert werden.",
            ],
            "Organisation": [
                "Das System zeigt ein gemischtes Bild mit stabilen und spannungsanfaelligen Bereichen.",
                "Unterschiedliche Dynamiken wirken parallel und fuehren zu inkonsistenter Orientierung und Wirksamkeit.",
                "Entwicklung kann dort ansetzen, wo diese Muster bewusster integriert und gemeinsam geklaert werden.",
            ],
        },
    }

    zeilen = texte.get(muster, {}).get(kontext, [])

    auspraegung_satz = {
        "stark": "Insgesamt wirken diese Muster derzeit stark ausgepraegt.",
        "deutlich": "Insgesamt wirken diese Muster aktuell deutlich ausgepraegt.",
        "punktuell": "Insgesamt zeigen sich diese Muster eher punktuell.",
        "grundsaetzlich": "Insgesamt sind die tragfaehigen Muster gut ausgepraegt.",
        "gemischt": "",
    }
    satz = auspraegung_satz.get(auspraegung, "")
    if satz:
        zeilen = zeilen + [satz]
    return zeilen

def muster_staerke(vd, ps, fw):
    abweichung = abs(vd - 3) + abs(ps - 3) + abs(fw - 3)
    if abweichung < 1:
        return "schwach ausgepraegt"
    elif abweichung < 2:
        return "moderat ausgepraegt"
    else:
        return "deutlich ausgepraegt"

def auspraegung_bestimmen(muster, vd, ps, fw):
    if muster == "Anpassung":
        if vd <= 1 and ps <= 1:
            return "stark"
        elif vd <= 2 and ps <= 2:
            return "deutlich"
        else:
            return "punktuell"
    elif muster == "Schutz und Inkonsistenz":
        if ps <= 1 and fw <= 1:
            return "stark"
        elif ps <= 2 and fw <= 2:
            return "deutlich"
        else:
            return "punktuell"
    elif muster == "Strukturproblem":
        if vd <= 1 and fw <= 1:
            return "stark"
        elif vd <= 2 and fw <= 2:
            return "deutlich"
        else:
            return "punktuell"
    elif muster == "Stabil":
        if vd >= 4 and ps >= 4 and fw >= 4:
            return "stark"
        else:
            return "grundsaetzlich"
    else:
        return "gemischt"

# ———————––
# PDF-Generierung
# ———————––

def erstelle_pdf(vd, ps, fw, muster, kontext, sekundaer=None):
    """
    Gibt ein BytesIO-Objekt mit dem fertigen PDF zurueck.
    Kann direkt als Download in Streamlit genutzt werden.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = erstelle_styles()
    story = []
    auspraegung = auspraegung_bestimmen(muster, vd, ps, fw)

    # ---- Kopf ----
    story.append(Paragraph("Systemische Organisationsdiagnose", styles["titel"]))
    story.append(Paragraph("Ergebnisbericht", styles["untertitel"]))
    story.append(hr())

    # Metadaten
    meta_data = [
        ["Kontext:", kontext],
        ["Datum:", datetime.now().strftime("%d.%m.%Y")],
        ["Systemmuster:", muster],
        ["Auspraegung:", muster_staerke(vd, ps, fw)],
    ]
    meta_table = Table(meta_data, colWidths=[5 * cm, 11 * cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXTGRAU),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.4 * cm))

    # ---- Scores ----
    story.append(hr())
    story.append(Paragraph("Detailwerte", styles["section"]))

    score_data = [
        ["Bereich", "Score (1–5)", "Einordnung"],
        ["Verantwortungslogik", str(round(vd, 2)), score_einordnung(vd)],
        ["Psychologische Sicherheit", str(round(ps, 2)), score_einordnung(ps)],
        ["Fuehrungswirksamkeit", str(round(fw, 2)), score_einordnung(fw)],
    ]
    score_table = Table(score_data, colWidths=[7 * cm, 4 * cm, 5 * cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DUNKELBLAU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HELLGRAU, colors.white]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.3 * cm))

    # ---- Einordnung im Kontext ----
    story.append(Paragraph("Einordnung im Kontext", styles["section"]))
    for zeile in einordnung_im_kontext(muster, kontext):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Systemische Muster ----
    story.append(Paragraph("Systemische Muster", styles["section"]))
    for zeile in systemische_muster_texte(muster):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Sekundaeres Muster ----
    if sekundaer:
        story.append(Paragraph("Sekundaeres Muster", styles["section"]))
        story.append(Paragraph(
            f"Neben dem Hauptmuster zeigen sich ergaenzend Hinweise auf: <b>{sekundaer}</b>. "
            "Dieses tritt weniger dominant auf, kann aber die Gesamtdynamik mitpraegen.",
            styles["body"]
        ))
        story.append(Spacer(1, 0.2 * cm))

    # ---- Entwicklungshebel ----
    story.append(Paragraph("Moegliche Entwicklungshebel", styles["section"]))
    for zeile in entwicklungshebel(vd, ps, fw):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Gesamtbild ----
    story.append(Paragraph("Gesamtbild", styles["section"]))
    for zeile in gesamtbild(muster, kontext, auspraegung):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Weiteres Vorgehen ----
    story.append(Paragraph("Weiteres Vorgehen", styles["section"]))
    story.append(Paragraph(
        "Der Bericht kann als Ausgangspunkt fuer gezielte Klaerung, Fuehrungsdialog oder "
        "strukturelle Weiterentwicklung genutzt werden. Entscheidend ist, implizite Muster "
        "sichtbar und besprechbar zu machen.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.4 * cm))

    # ---- Trennlinie ----
    story.append(hr())

    # ---- Ueber die Beraterin ----
    story.append(Paragraph("Ueber die Beraterin", styles["section"]))
    story.append(Paragraph(
        "Anja Nestler ist systemische Organisationsberaterin und Business Coach. "
        "Sie unterstuetzt Fuehrungsteams dabei, implizite Muster sichtbar zu machen "
        "und konkrete Ansatzpunkte fuer Klaerung und Weiterentwicklung zu finden.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Die Ergebnisse dieses Berichts geben erste Hinweise auf zugrunde liegende Dynamiken. "
        "Die eigentliche Wirkung zeigt sich erfahrungsgemaess erst im gemeinsamen Blick "
        "auf konkrete Situationen.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "&#8594; <a href='https://calendly.com/anja-nestler/30min' color='#2E5090'>"
        "Jetzt Einordnungsgespraech buchen</a>",
        styles["body"]
    ))

    # ---- Footer-Hinweis ----
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        "Diese Diagnose ersetzt keine umfassende Organisationsanalyse. "
        "Sie dient der ersten Orientierung und Reflexion.",
        styles["footer"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
