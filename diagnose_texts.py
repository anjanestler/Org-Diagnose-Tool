import inspect

def diagnose_text(muster, kontext="Organisation", ton="reflexiv"):
    texte = {
        "Anpassung": {
            "Organisation":
            """In Ihrer Organisation gibt es Hinweise darauf, dass Verantwortung oft nicht klar geregelt ist – und dass Spannungen eher still getragen als offen geklärt werden. Das Ergebnis: Entscheidungen verzögern sich, Themen bleiben ohne Abschluss.

Das ist kein Zeichen von schlechtem Willen. Es ist ein Muster das sich eingeschlichen hat – und das sich verändern lässt.

Typische Anzeichen:
- Zuständigkeiten sind unklar oder werden stillschweigend vorausgesetzt
- Konflikte werden eher umgangen als direkt angesprochen
- Loyalität steht oft vor offener Klärung

Was das im Alltag bedeutet:
- Einzelne tragen überproportional viel Verantwortung
- Themen kommen immer wieder auf den Tisch ohne echten Abschluss
- Die Umsetzung von Entscheidungen stockt

Wie diese Muster in Ihrer konkreten Situation zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an.""",

            "Fuehrungsteam":
            """In Ihrem Führungsteam gibt es Hinweise darauf, dass Verantwortung nicht immer klar abgestimmt ist – und dass Spannungen eher durch Anpassung als durch offene Klärung bewältigt werden.

Das ist kein Versagen einzelner Personen. Es ist ein Muster das sich über Zeit entwickelt – und das sich verändern lässt.

Typische Anzeichen:
- Erwartungen bleiben implizit statt ausgesprochen
- Themen werden besprochen aber selten wirklich abgeschlossen
- Im Team wird Harmonie manchmal über Klarheit gestellt

Was das im Alltag bedeutet:
- Entscheidungen verzögern sich oder werden mehrfach neu aufgerollt
- Die gemeinsame Ausrichtung leidet
- Einzelne fühlen sich mit Verantwortung allein gelassen

Wie diese Muster in Ihrem Führungsteam zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an."""
        },

        "Schutz und Inkonsistenz": {
            "Organisation":
            """In Ihrer Organisation gibt es Hinweise darauf, dass wichtige Themen nicht immer offen angesprochen werden – und dass Führung nicht durchgängig klare Orientierung gibt. Beides zusammen führt dazu, dass Mitarbeitende und mittlere Führungskräfte oft im Unklaren bleiben, was wirklich erwartet wird.

Das ist kein Versagen einzelner Personen. Es ist ein Muster das sich über Zeit entwickelt – und das sich verändern lässt.

Typische Anzeichen:
- Probleme werden wahrgenommen, aber selten direkt angesprochen
- Prioritäten wirken von oben nicht immer einheitlich
- Zwischen Führung und Organisation entsteht zunehmend Distanz

Was das im Alltag bedeutet:
- Entscheidungen werden getroffen, aber nicht von allen mitgetragen
- Erwartungen werden unterschiedlich verstanden
- Themen kommen immer wieder auf den Tisch ohne wirklichen Abschluss

Wie diese Muster in Ihrer konkreten Situation zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an.""",

            "Fuehrungsteam":
            """In Ihrem Führungsteam gibt es Hinweise darauf, dass nicht alles offen angesprochen wird – und dass die Signale die Führung sendet nicht immer einheitlich ankommen. Das verunsichert und führt zu Vorsicht statt Klarheit.

Das ist kein Versagen einzelner Personen. Es ist ein Muster das sich über Zeit entwickelt – und das sich verändern lässt.

Typische Anzeichen:
- Kritische Themen werden im Team eher umgangen
- Erwartungen werden unterschiedlich interpretiert
- Die gemeinsame Ausrichtung wirkt nicht immer stabil

Was das im Alltag bedeutet:
- Entscheidungen werden formal getroffen aber nicht wirklich gemeinsam getragen
- Einzelne ziehen sich zurück oder agieren auf Sicherheit
- Die kollektive Wirksamkeit des Teams leidet

Wie diese Muster in Ihrem Führungsteam zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an."""
        },

        "Strukturproblem": {
            "Organisation":
            """In Ihrer Organisation gibt es Hinweise darauf, dass Verantwortung und Entscheidungswege nicht klar genug geregelt sind. Themen wandern zwischen Rollen, Zuständigkeiten bleiben unklar – und die Umsetzung stockt.

Das ist kein Zeichen von mangelndem Engagement. Es ist ein strukturelles Muster – und das lässt sich klären.

Typische Anzeichen:
- Es ist nicht immer klar wer Entscheidungen treffen darf oder soll
- Verantwortung wird übergeben ohne dass Mandat und Rückendeckung gesichert sind
- Themen werden mehrfach besprochen ohne verbindlichen Abschluss

Was das im Alltag bedeutet:
- Initiativen verlieren unterwegs an Verbindlichkeit
- Frustration entsteht weil Klärung ausbleibt
- Einzelne fühlen sich verantwortlich ohne wirklich entscheiden zu können

Wie diese Muster in Ihrer konkreten Situation zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an.""",

            "Fuehrungsteam":
            """In Ihrem Führungsteam gibt es Hinweise darauf, dass Rollen, Mandate und Entscheidungswege nicht durchgängig klar sind. Das erschwert verbindliche Zusammenarbeit – und kostet Energie die anderswo fehlt.

Das ist kein Zeichen von mangelndem Engagement. Es ist ein strukturelles Muster – und das lässt sich klären.

Typische Anzeichen:
- Zuständigkeiten überlappen oder bleiben ungeklärt
- Entscheidungen werden mehrfach aufgerufen ohne Abschluss
- Einzelne tragen Verantwortung ohne ausreichende Rückendeckung

Was das im Alltag bedeutet:
- Die kollektive Führungswirksamkeit ist eingeschränkt
- Themen zirkulieren im Team ohne voranzukommen
- Verbindlichkeit entsteht nicht verlässlich

Wie diese Muster in Ihrem Führungsteam zusammenwirken – und wo sinnvolle Ansatzpunkte liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an."""
        },

        "Stabil": {
            "Organisation":
            """Ihre Organisation zeigt in allen drei Bereichen grundsätzlich tragfähige Strukturen. Verantwortung wird übernommen, Spannungen können angesprochen werden und Führung gibt Orientierung.

Das sind gute Voraussetzungen – und ein solides Fundament für gezielte Weiterentwicklung.

Was das im Alltag bedeutet:
- Entscheidungen kommen zu einem Abschluss
- Themen werden offen und konstruktiv besprochen
- Die Zusammenarbeit ist auf gemeinsame Ziele ausgerichtet

Wo liegen die nächsten Entwicklungsschritte? Und wie lassen sich die vorhandenen Stärken noch bewusster nutzen? Das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an.""",

            "Fuehrungsteam":
            """Ihr Führungsteam zeigt in allen drei Bereichen grundsätzlich tragfähige Strukturen. Verantwortung ist klar, Spannungen können angesprochen werden und Orientierung ist spürbar.

Das sind gute Voraussetzungen – und ein solides Fundament für gezielte Weiterentwicklung.

Was das im Alltag bedeutet:
- Gemeinsame Ausrichtung ist erkennbar
- Konflikte werden konstruktiv bearbeitet
- Das Team kann als kollektive Führungskraft wirken

Wo liegen die nächsten Entwicklungsschritte? Und wie lassen sich die vorhandenen Stärken noch bewusster nutzen? Das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an."""
        },

        "Gemischtes Muster": {
            "Organisation":
            """Ihre Organisation zeigt ein gemischtes Bild: Einige Bereiche funktionieren gut, in anderen gibt es noch Klärungsbedarf. Das ist häufiger als man denkt – und ein guter Ausgangspunkt für gezielte Entwicklung.

Typische Anzeichen:
- Manche Entscheidungen laufen reibungslos, andere stocken
- Psychologische Sicherheit ist situativ vorhanden aber nicht überall gleich
- Führung wirkt in Teilen klar, in anderen Bereichen uneinheitlich

Was das im Alltag bedeutet:
- Die Zusammenarbeit ist von Bereich zu Bereich unterschiedlich
- Potenzial liegt darin, die stabilen Muster bewusster zu nutzen
- Klärungsbedarf in einzelnen Bereichen bremst das Gesamtsystem

Wie diese Muster in Ihrer konkreten Situation zusammenwirken – und wo die wichtigsten Hebel liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an.""",

            "Fuehrungsteam":
            """Ihr Führungsteam zeigt ein gemischtes Bild: Einige Bereiche funktionieren gut, in anderen gibt es noch Klärungsbedarf. Das ist häufiger als man denkt – und ein guter Ausgangspunkt für gezielte Entwicklung.

Typische Anzeichen:
- In manchen Situationen läuft die Zusammenarbeit reibungslos, in anderen nicht
- Verantwortung und Orientierung sind teilweise klar, teilweise noch offen
- Die kollektive Wirksamkeit des Teams ist noch nicht voll ausgeschöpft

Was das im Alltag bedeutet:
- Unterschiedliche Dynamiken wirken parallel und führen zu inkonsistenter Ausrichtung
- Einzelne Stärken werden noch nicht durchgängig genutzt
- Gezielte Klärung könnte die Teamwirksamkeit deutlich steigern

Wie diese Muster in Ihrem Führungsteam zusammenwirken – und wo die wichtigsten Hebel liegen – das lässt sich am besten im gemeinsamen Gespräch herausarbeiten.

Fordern Sie jetzt den ausführlichen Bericht an."""
        }
    }

    eintrag = texte.get(muster, "")

    if isinstance(eintrag, dict):
        text = eintrag.get(kontext, eintrag.get("Organisation", ""))
    else:
        text = eintrag

    text = inspect.cleandoc(text)

    if ton == "reflexiv":
        return text
    elif ton == "knapp":
        return text.split(".")[0] + "."
    else:
        return text