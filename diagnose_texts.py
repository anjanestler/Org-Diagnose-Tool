import inspect

def diagnose_text(muster, kontext="Organisation", ton="reflexiv"):
    texte = {
        "Anpassung": {
            "Organisation":
            """Im System zeigen sich Hinweise auf eine Anpassungsdynamik.
            In solchen Situationen bleibt Verantwortung haeufig implizit,
            waehrend Spannungen selten offen geklaert werden. Das System
            stabilisiert sich eher durch Anpassung als durch offene Klaerung
            von Erwartungen und Zustaendigkeiten.

            Typische Anzeichen koennen sein:
            - Verantwortung bleibt implizit oder diffus
            - Klaerungsgespraeche fuehren zu abstrakten Kompromissen
            - Entscheidungen und Umsetzung verzoegern sich

            Wenn diese Dynamik laenger besteht, zeigen sich haeufig:
            - Ueberlastung einzelner
            - Rueckzug oder vorsichtiges Verhalten anderer
            - Verlust von Leistungstraeger_innen

            Organisationen reagieren in dieser Situation haeufig mit
            Aktionismus (z. B. neue Projekte oder Regeln). Diese Reaktionen
            sind verstaendlich, veraendern jedoch meist nicht die
            zugrunde liegende Dynamik. 

            Ein erster sinnvoller Entwicklungsschritt kann darin bestehen, 
            unterschiedliche Perspektiven sichtbar zu machen und Vertrauen
            fuer offene Klaerung zu staerken. 
            """,

            "Fuehrungsteam":
            """Im Fuehrungsteam zeigen sich Hinweise auf eine Anpassungsdynamik.

            Verantwortung wird teilweise individuell getragen, ohne
            durchgaengig klar abgestimmt zu sein. Spannungen werden
            haeufig eher durch Anpassung als durch offene Klaerung
            verarbeitet.

            Typische Anzeichen koennen sein:
            - Themen bleiben ohne klaren Abschluss
            - Erwartungen bleiben implizit
            - Entscheidungen verzoegern sich

            Ein erster sinnvoller Schritt kann darin bestehen,
            unterschiedliche Perspektiven sichtbar zu machen und
            Vertrauen fuer offene Klaerung zu staerken.
            """
        },
        
        "Schutz und Inkonsistenz":
            """Die Diagnose weist auf eine Dynamik von Schutz und inkonsistenter 
            Orientierung hin.


            In solchen Situationen wird nicht jede Spannung offen
            angesprochen, waehrend Fuehrung gleichzeitig unterschiedliche 
            oder wechselnde Signale sendet.

            Typische Anzeichen koennen sein:
            - offensichtliche Probleme werden selten offen angesprochen
            - zwischen Organisation und oberster Leitung entsteht Distanz
            - Prioritaeten wirken wechselhaft oder unklar

            Diese Dynamik kann dazu fuehren, dass mittlere Fuehrungsebenen 
            unter hoher Dissonanzbelastung stehen und Orientierung verlieren.

            Ein erster Entwicklungsschritt kann darin bestehen,
            Rueckmeldeschleifen zwischen Organisation und Fuehrung zu
            staerken und widerspruechliche Erwartungen sichtbar zu machen. 
            """,

        "Strukturproblem":
            """Die Ergebnisse deuten auf strukturelle Unklarheit in
            Verantwortungs- und Entscheidungslogiken hin.
        
            Typische Anzeichen koennen sein:
            - Entscheidungen werden mehrfach adressiert
            - Themen zirkulieren zwischen Rollen
            - Verantwortlichkeiten bleiben unklar
        
            Diese Dynamik erschwert verbindliche Umsetzung und kann
            zu Frustration oder Verzoegerungen fuehren.
        
            Ein sinnvoller erster Schritt kann darin bestehen,
            Entscheidungswege und Verantwortungslogiken gemeinsam
            zu klaeren.
            """,

        "Stabil":
            """Die Ergebnisse weisen auf grundsaetzlich tragfaehige
            Strukturen in Verantwortung, psychologischer Sicherheit und 
            Fuehrung hin.
        
            Prioritaeten sind meist klar, Spannungen koennen
            angesprochen werden und Verantwortung wird uebernommen.

            Dies schafft gute Voraussetzungen fuer gezielte
            Weiterentwicklung.

            """,

        "Gemischtes Muster":
            """Die Ergebnisse zeigen eine Mischung aus stabilen
            und spannungsanfaelligen Dynamiken.

            Einige Bereiche funktionieren gut, waehrend andere
            noch Klaerungsbedarf aufweisen.

            Eine gemeinsame Reflexion der unterschiedlichen 
            Perspektiven kann helfen, diese Muster besser
            zu verstehen.
            """
    }
    
    
    eintrag = texte.get(muster, "")

    if isinstance(eintrag, dict):
        text = eintrag.get(kontext, "")
    else:
        text = eintrag

    # Jede einzelne Zeile von Whitespace befreien
    zeilen = [z.strip() for z in text.splitlines()]
    text = "\n".join(zeilen)
    # Mehrfache Leerzeilen auf eine reduzieren
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    text = text.strip()

    if ton == "reflexiv":
        return text
    elif ton == "knapp":
        return text.split(".")[0] + "."
    else:
        return text