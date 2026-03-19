from diagnose_texts import diagnose_text

def bestimme_systemmuster(vd, ps, fw):

    if vd < 3 and ps < 3 and fw >= 3:
        return "Anpassung"
    
    elif ps < 3 and fw < 3 and vd >= 3:
        return "Schutz und Inkonsistenz"
    
    elif vd < 3 and ps < 3 and fw < 3:
        if vd <= fw:
            return "Anpassung"
        else:
            return "Schutz und Inkonsistenz"
    elif vd < 3 and fw < 3:
        return "Strukturproblem"
    elif vd >= 3 and ps >= 3 and fw >= 3:
        return "Stabil"
    
    else:
        return "Gemischtes Muster"
    
def score_einordnung(score):
    if score < 2:
        return "niedrig"
    elif score < 3.5:
        return "mittel"
    else:
        return "hoch"
    
def berechne_diagnose(vd, ps, fw, kontext, ton):
    muster = bestimme_systemmuster(vd, ps, fw)
    staerke = muster_staerke(vd, ps, fw)
    sekundaer = sekundaeres_muster(vd, ps, fw)

    ergebnis = {
        "muster": muster,
        "staerke": staerke,
        "sekundaeres_muster": sekundaer,
        "summary": diagnose_text(muster, kontext, ton),
        "scores": {
            "Verantwortungslogik": vd,
            "Psychologische Sicherheit": ps,
            "Fuehrungswirksamkeit": fw
        }
    }
    
    return ergebnis

def muster_staerke(vd, ps, fw):

    abweichung = abs(vd-3) + abs(ps-3) + abs(fw-3)

    if abweichung < 1:
        return "schwach ausgepraegt"
    elif abweichung < 2:
        return "moderat ausgepraegt"
    else:
        return "deutlich ausgepraegt"
    
def sekundaeres_muster(vd, ps, fw):
    werte = {
        "Verantwortungslogik": vd,
        "Psychologische Sicherheit": ps,
        "Fuehrungswirksamkeit": fw
    }
    sortiert = sorted(werte.items(), key=lambda x: abs(x[1] - 3), reverse=True)

    zweit = sortiert[1][0]

    mapping = {
        "Verantwortungslogik": "Strukturproblem",
        "Psychologische Sicherheit": "Schutz und Inkonsistenz",
        "Fuehrungswirksamkeit": "Anpassung"
    }
    return mapping.get(zweit)

def typische_auswirkungen(muster):
    texte = {
        "Anpassung": [
            "Entscheidungen werden mehrfach diskutiert, ohne klaren Abschluss.",
            "Verantwortung wird teilweise uebernommen, aber nicht durchgaengig getragen.",
            "Themen werden eher vorsichtig behandelt statt klar geklaert."
        ],
        "Schutz und Inkonsistenz": [
            "Kritische Themen werden nicht durchgaengig offen angesprochen.",
            "Erwartungen werden unterschiedlich interpretiert.",
            "Entscheidungen sind formal getroffen, werden aber nicht einheitlich umgesetzt."
        ],
        "Strukturproblem": [
            "Unklarheit darueber, wer Entscheidungen tatsaechlich trifft oder verantwortet.",
            "Themen werden zwischen Rollen weitergegeben, ohne Abschluss.",
            "Initiativen verlieren im Verlauf an Verbindlichkeit oder werden nicht konsequent weitergefuehrt."
        ],
        "Stabil": [
            "Verantwortung wird klar uebernommen und umgesetzt.",
            "Themen werden offen angesprochen und geklaert.",
            "Zusammenarbeit ist auf gemeinsame Ziele ausgerichtet."
        ],
        "Gemischtes Muster": [
            "Einzelne Bereiche funktionieren gut, andere wirken hingegen unklar.",
            "Entscheidungen sind teilweise klar, teilweise jedoch widerspruechlich.",
            "Umsetzung variiert je nach Kontext und Beteiligten."
        ]
    }
    return texte.get(muster, [])

def einordnung_text():
    return (
        "Die dargestellten Dynamiken sind in vielen Organisationen nicht ungewoehnlich. "
        "Gleichzeitig zeigen Erfahrungen, dass sie sich selten allein durch individuelle Anpassung veraendern lassen. "
        "Entscheidend ist, wie diese Muster im Fuehrungsteam gemeinsam verstanden und geklaert werden."
    )