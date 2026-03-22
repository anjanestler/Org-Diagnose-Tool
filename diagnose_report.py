"""
diagnose_report.py
Generiert einen PDF-Ergebnisbericht fuer die Systemische Organisationsdiagnose.
Wird von der Streamlit-App aufgerufen, nachdem die Mail-Adresse eingegeben wurde.
"""

from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)


# -------------------------
# Farben
# -------------------------

DUNKELBLAU = colors.HexColor("#1B2A4A")
MITTELBLAU = colors.HexColor("#2E5090")
HELLGRAU   = colors.HexColor("#F4F4F4")
TEXTGRAU   = colors.HexColor("#333333")


# -------------------------
# Styles
# -------------------------

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
        "einladend": ParagraphStyle(
            "Einladend",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=MITTELBLAU,
            spaceAfter=6,
            leading=15,
        ),
        "footer": ParagraphStyle(
            "Footer",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=4,
            leading=12,
        ),
    }
    return styles


# -------------------------
# Hilfsfunktionen
# -------------------------

def score_einordnung(score):
    if score >= 4:
        return "hoch"
    elif score >= 3:
        return "mittel"
    else:
        return "niedrig"


def bullet(text, styles):
    return Paragraph(f"&#8226; &nbsp; {text}", styles["bullet"])


def hr():
    return HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.HexColor("#CCCCCC"),
        spaceAfter=8,
        spaceBefore=4,
    )


# -------------------------
# Inhaltliche Texte
# -------------------------

def einordnung_im_kontext(muster, kontext):
    texte = {
        "Anpassung": {
            "Fuehrungsteam": [
                "In Ihrem Führungsteam ist nicht immer klar, wer Verantwortung tatsächlich trägt. Spannungen werden eher still bewältigt als offen geklärt.",
                "Verantwortung liegt häufig bei Einzelnen, ohne dass das strukturell so vereinbart wäre.",
                "So entsteht Zurückhaltung statt Klärung, und Themen bleiben länger offen als nötig.",
            ],
            "Organisation": [
                "In Ihrer Organisation ist nicht immer klar, wer Verantwortung tatsächlich trägt. Spannungen werden eher still bewältigt als offen geklärt.",
                "Verantwortung liegt häufig bei Einzelnen, ohne dass das strukturell so vereinbart wäre.",
                "So entsteht Zurückhaltung statt Klärung, und Themen bleiben länger offen als nötig.",
            ],
        },
        "Schutz und Inkonsistenz": {
            "Fuehrungsteam": [
                "In Ihrem Führungsteam wird nicht alles offen angesprochen, und die Signale, die Führung sendet, kommen nicht immer einheitlich an.",
                "Erwartungen bleiben teilweise unklar oder werden unterschiedlich verstanden.",
                "Das führt zu Vorsicht und Zurückhaltung statt zu klarer gemeinsamer Ausrichtung.",
            ],
            "Organisation": [
                "In Ihrer Organisation wird nicht alles offen angesprochen. Führung gibt nicht immer konsistente Orientierung.",
                "Erwartungen bleiben teilweise unklar oder werden unterschiedlich verstanden.",
                "Das führt zu Vorsicht und Zurückhaltung statt zu klarer gemeinsamer Ausrichtung.",
            ],
        },
        "Strukturproblem": {
            "Fuehrungsteam": [
                "In Ihrem Führungsteam sind Rollen, Mandate und Entscheidungswege nicht durchgängig geklärt.",
                "Das führt dazu, dass Entscheidungen mehrfach aufgerufen werden und Themen keinen verbindlichen Abschluss finden.",
                "Einzelne tragen Verantwortung ohne ausreichende Rückendeckung. Das kostet Energie und bremst die Umsetzung.",
            ],
            "Organisation": [
                "In Ihrer Organisation sind Verantwortlichkeiten und Entscheidungswege nicht durchgängig geklärt.",
                "Das führt dazu, dass Themen zwischen Rollen wandern und keinen verbindlichen Abschluss finden.",
                "Initiativen verlieren unterwegs an Verbindlichkeit. Frustration entsteht, wo Klärung ausbleibt.",
            ],
        },
        "Stabil": {
            "Fuehrungsteam": [
                "Ihr Führungsteam zeigt in allen drei Bereichen eine grundsätzlich tragfähige Zusammenarbeit.",
                "Verantwortung ist klar, Spannungen können angesprochen werden und Orientierung ist spürbar.",
            ],
            "Organisation": [
                "Ihre Organisation zeigt in allen drei Bereichen grundsätzlich tragfähige Strukturen.",
                "Verantwortung wird übernommen, Spannungen können angesprochen werden und Führung gibt Orientierung.",
            ],
        },
        "Gemischtes Muster": {
            "Fuehrungsteam": [
                "Ihr Führungsteam zeigt ein gemischtes Bild: Einige Bereiche laufen gut, in anderen gibt es noch Klärungsbedarf.",
                "Das Team schöpft sein gemeinsames Potenzial noch nicht voll aus.",
            ],
            "Organisation": [
                "Ihre Organisation zeigt ein gemischtes Bild: Einige Bereiche funktionieren gut, in anderen gibt es noch Klärungsbedarf.",
                "Unterschiedliche Dynamiken wirken parallel. Dies führt zu inkonsistenter Orientierung und Umsetzung.",
            ],
        },
    }
    return texte.get(muster, {}).get(kontext, [])


def systemische_muster_texte(muster):
    texte = {
        "Anpassung": [
            "Verantwortung wird im Alltag oft einzelnen Personen zugeschrieben, ohne dass klar ist wie sie strukturell verankert ist.",
            "Probleme werden eher einzelnen angelastet, als im Zusammenspiel von Rollen und Rahmenbedingungen betrachtet.",
            "Konflikte bleiben häufig unausgesprochen, Loyalität steht vor offener Klärung.",
            "Strategische Themen kommen langsamer voran, weil Zuständigkeiten nicht eindeutig benannt sind.",
        ],
        "Schutz und Inkonsistenz": [
            "Führung gibt im Alltag nicht immer eindeutige Orientierung, Erwartungen bleiben teilweise unausgesprochen.",
            "Mitarbeitende agieren daher eher vorsichtig und vermeiden es, Risiken offen anzusprechen.",
            "Unklare Kommunikation führt zu Zurückhaltung statt zu Verantwortung.",
            "Entscheidungen werden formal getroffen, aber nicht immer wirklich gemeinsam getragen.",
        ],
        "Strukturproblem": [
            "Es ist nicht immer klar, wer Entscheidungen treffen darf oder soll.",
            "Verantwortung wird übergeben, ohne dass Mandat und Rückendeckung vollständig gesichert sind.",
            "Themen wandern zwischen Rollen, ohne verbindlich abgeschlossen zu werden.",
            "Einzelinteressen stehen gelegentlich stärker im Vordergrund als die gemeinsame Verantwortung.",
        ],
        "Stabil": [
            "Verantwortung ist klar zugeordnet und wird im Alltag sichtbar übernommen.",
            "Spannungen können offen angesprochen und konstruktiv bearbeitet werden.",
            "Führung gibt Orientierung, ohne in Mikromanagement zu verfallen.",
            "Die Zusammenarbeit richtet sich erkennbar an gemeinsamen Zielen aus.",
        ],
        "Gemischtes Muster": [
            "Einige Bereiche wirken klar und stabil, andere eher unklar oder spannungsanfällig.",
            "Psychologische Sicherheit ist situativ vorhanden, aber nicht überall gleich ausgeprägt.",
            "Führung wirkt in Teilen orientierend, in anderen Bereichen uneinheitlich.",
            "Entwicklungspotenzial liegt darin, diese unterschiedlichen Muster bewusster zu integrieren.",
        ],
    }
    return texte.get(muster, [])


def entwicklungshebel(vd, ps, fw):
    hebel = []
    if vd < 3:
        hebel += [
            "Klären Sie gemeinsam, wer welche Entscheidungen trifft und wer die Umsetzung trägt.",
            "Machen Sie gegenseitige Erwartungen explizit, statt sie stillschweigend vorauszusetzen.",
            "Verankern Sie Verantwortung strukturell und nicht nur personenbezogen.",
        ]
    if ps < 3:
        hebel += [
            "Sprechen Sie als Führung Unsicherheiten und Fehler offen an. Das gibt anderen die Erlaubnis, es auch zu tun.",
            "Schaffen Sie Räume, in denen kritische Themen ohne Konsequenzen benannt werden können.",
            "Vertrauen entsteht durch konsequentes Verhalten, nicht durch Worte.",
        ]
    if fw < 3:
        hebel += [
            "Formulieren Sie klare Erwartungen und setzen Sie sichtbar Prioritäten.",
            "Reflektieren Sie gemeinsam, wo Anspruch und gelebte Praxis auseinanderfallen.",
            "Prüfen Sie regelmäßig, ob Ihre gemeinsamen Ziele noch zum Alltag passen.",
        ]
    if vd >= 3 and ps >= 3 and fw >= 3:
        hebel += [
            "Nutzen Sie die vorhandene Stabilität gezielt für Weiterentwicklung statt nur für Erhalt.",
            "Vertiefen Sie bereichsübergreifende Zusammenarbeit und gemeinsames Lernen.",
        ]
    return hebel


def gesamtbild_texte(muster, kontext, auspraegung):
    texte = {
        "Stabil": {
            "Fuehrungsteam": [
                "Ihr Führungsteam arbeitet auf einer tragfähigen Grundlage.",
                "Gemeinsame Orientierung und klare Verantwortung machen das Team handlungsfähig.",
                "Der nächste Schritt liegt darin, vorhandene Stärken bewusst zu nutzen und gezielt weiterzuentwickeln.",
            ],
            "Organisation": [
                "Ihre Organisation arbeitet auf einer tragfähigen Grundlage.",
                "Verantwortung, Orientierung und offene Klärung tragen zur gemeinsamen Wirksamkeit bei.",
                "Der nächste Schritt liegt darin, vorhandene Stärken bewusst zu nutzen und gezielt weiterzuentwickeln.",
            ],
        },
        "Anpassung": {
            "Fuehrungsteam": [
                "Ihr Führungsteam stabilisiert sich derzeit eher durch Anpassung als durch offene Klärung.",
                "Unklare Erwartungen und implizite Verantwortung bremsen die gemeinsame Ausrichtung.",
                "Entwicklung setzt dort an, wo Verantwortung, Erwartungen und offene Klärung gestärkt werden.",
            ],
            "Organisation": [
                "Ihre Organisation stabilisiert sich derzeit eher durch Anpassung als durch offene Klärung.",
                "Unklare Verantwortung und zurückhaltende Kommunikation bremsen die gemeinsame Wirksamkeit.",
                "Entwicklung setzt dort an, wo Verantwortung, Erwartungen und offene Klärung bewusster gestärkt werden.",
            ],
        },
        "Schutz und Inkonsistenz": {
            "Fuehrungsteam": [
                "In Ihrem Führungsteam entsteht durch mangelnde Offenheit und widersprüchliche Signale ein Muster, das gemeinsames Handeln erschwert.",
                "Wenn Führung unterschiedliche Signale sendet, warten Mitarbeitende lieber ab – statt Verantwortung zu übernehmen.",
                "Entwicklung setzt dort an, wo Orientierung, Konsistenz und offene Rückmeldung gestärkt werden.",
            ],
            "Organisation": [
                "In Ihrer Organisation entsteht durch fehlende Sicherheit und inkonsistente Führung ein Muster, das gemeinsame Wirksamkeit einschränkt.",
                "Wechselnde Prioritäten und unklare Ansagen führen dazu, dass Mitarbeitende abwarten statt eigenständig zu handeln.",
                "Entwicklung setzt dort an, wo Orientierung, Konsistenz und offene Rückmeldung bewusster gestärkt werden.",
            ],
        },
        "Strukturproblem": {
            "Fuehrungsteam": [
                "Ihr Führungsteam arbeitet unter struktureller Unklarheit, die kollektive Verantwortung und Umsetzung erschwert.",
                "Fehlende Klarheit über Rollen und Entscheidungswege verhindert durchgängige Verbindlichkeit.",
                "Entwicklung setzt dort an, wo Mandate, Entscheidungswege und gemeinsame Verantwortung geklärt werden.",
            ],
            "Organisation": [
                "Ihre Organisation arbeitet unter struktureller Unklarheit, die Verantwortung und Umsetzung erschwert.",
                "Fehlende Klarheit über Rollen und Entscheidungswege führt dazu, dass Themen nicht verbindlich vorankommen.",
                "Entwicklung setzt dort an, wo Verantwortung, Entscheidungslogik und strukturelle Klarheit bewusst gestärkt werden.",
            ],
        },
        "Gemischtes Muster": {
            "Fuehrungsteam": [
                "Ihr Führungsteam zeigt ein gemischtes Bild mit stabilen und klärungsbedürftigen Bereichen.",
                "Verschiedene Bereiche ziehen nicht immer am selben Strang.",
                "Entwicklung setzt dort an, wo diese Muster bewusster wahrgenommen und gemeinsam integriert werden.",
            ],
            "Organisation": [
                "Ihre Organisation zeigt ein gemischtes Bild mit stabilen und klärungsbedürftigen Bereichen.",
                "Verschiedene Bereiche ziehen nicht immer am selben Strang.",
                "Entwicklung setzt dort an, wo diese Muster bewusster wahrgenommen und gemeinsam geklärt werden.",
            ],
        },
    }

    zeilen = texte.get(muster, {}).get(kontext, [])

    auspraegung_satz = {
        "stark": "Diese Muster sind derzeit stark ausgeprägt und wirken sich spürbar auf den Alltag aus.",
        "deutlich": "Diese Muster sind aktuell deutlich ausgeprägt.",
        "punktuell": "Diese Muster zeigen sich bisher eher punktuell.",
        "grundsaetzlich": "Die tragfähigen Muster sind insgesamt gut ausgeprägt.",
        "gemischt": "",
    }
    satz = auspraegung_satz.get(auspraegung, "")
    if satz:
        zeilen = zeilen + [satz]
    return zeilen


def muster_staerke(vd, ps, fw):
    abweichung = abs(vd - 3) + abs(ps - 3) + abs(fw - 3)
    if abweichung < 1:
        return "schwach ausgeprägt"
    elif abweichung < 2:
        return "moderat ausgeprägt"
    else:
        return "deutlich ausgeprägt"


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


# -------------------------
# PDF-Generierung
# -------------------------

def erstelle_pdf(vd, ps, fw, muster, kontext, sekundaer=None):
    """
    Gibt ein BytesIO-Objekt mit dem fertigen PDF zurück.
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
    story.append(Paragraph("Ihr persönlicher Ergebnisbericht", styles["untertitel"]))
    story.append(hr())

    # Metadaten
    meta_data = [
        ["Kontext:", kontext],
        ["Datum:", datetime.now().strftime("%d.%m.%Y")],
        ["Erkanntes Muster:", muster],
        ["Ausprägung:", muster_staerke(vd, ps, fw)],
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
    story.append(Paragraph("Ihre Ergebnisse im Überblick", styles["section"]))

    score_data = [
        ["Bereich", "Score (1–5)", "Einordnung"],
        ["Verantwortungslogik", str(round(vd, 2)), score_einordnung(vd)],
        ["Psychologische Sicherheit", str(round(ps, 2)), score_einordnung(ps)],
        ["Führungswirksamkeit", str(round(fw, 2)), score_einordnung(fw)],
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
    story.append(Paragraph("Was die Ergebnisse bedeuten", styles["section"]))
    for zeile in einordnung_im_kontext(muster, kontext):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Systemische Muster ----
    story.append(Paragraph("Wie sich das Muster im Alltag zeigt", styles["section"]))
    for zeile in systemische_muster_texte(muster):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Sekundäres Muster ----
    if sekundaer:
        story.append(Paragraph("Ergänzender Hinweis", styles["section"]))
        story.append(Paragraph(
            f"Neben dem Hauptmuster zeigen sich ergänzend Hinweise auf: <b>{sekundaer}</b>. "
            "Dieses Muster tritt weniger stark auf, kann aber das Gesamtbild beeinflussen "
            "und sollte bei der weiteren Entwicklung nicht außer Acht gelassen werden.",
            styles["body"]
        ))
        story.append(Spacer(1, 0.2 * cm))

    # ---- Entwicklungshebel ----
    story.append(Paragraph("Mögliche Ansatzpunkte", styles["section"]))
    for zeile in entwicklungshebel(vd, ps, fw):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.2 * cm))

    # ---- Gesamtbild ----
    story.append(Paragraph("Gesamtbild", styles["section"]))
    for zeile in gesamtbild_texte(muster, kontext, auspraegung):
        story.append(bullet(zeile, styles))
    story.append(Spacer(1, 0.4 * cm))

    # ---- Trennlinie ----
    story.append(hr())

    # ---- Einladender Abschluss ----
    story.append(Paragraph("Wie geht es weiter?", styles["section"]))
    story.append(Paragraph(
        "Dieser Bericht zeigt erste Muster, aber die eigentliche Wirkung entsteht "
        "im gemeinsamen Gespräch. Was steckt wirklich hinter diesen Ergebnissen? "
        "Wo liegen die konkreten Hebel für Ihre Situation?",
        styles["body"]
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Ich begleite Führungsteams und Organisationen dabei, genau das herauszufinden – "
        "und konkrete Schritte abzuleiten, die wirklich zur Situation passen.",
        styles["einladend"]
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Ich freue mich auf das Gespräch mit Ihnen.",
        styles["einladend"]
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Anja Nestler – Systemische Organisationsberaterin &amp; Business Coach",
        styles["body"]
    ))
    story.append(Spacer(1, 0.1 * cm))
    story.append(Paragraph(
        "&#8594; <a href='https://calendly.com/anja-nestler/30min' color='#2E5090'>"
        "Jetzt Einordnungsgespräch buchen</a>",
        styles["body"]
    ))

    # ---- Footer ----
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        "Dieser Bericht basiert auf Ihrer Selbsteinschätzung und dient der ersten Orientierung. "
        "Er ersetzt keine umfassende Organisationsanalyse.",
        styles["footer"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer