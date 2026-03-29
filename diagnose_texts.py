import inspect

def diagnose_text(muster, kontext="Organisation", ton="reflexiv"):
    texte = {
        "Anpassung": {
            "Organisation":
            """In Ihrer Organisation gibt es Hinweise auf ein Anpassungsmuster: Spannungen werden eher still getragen als offen geklärt, Verantwortung bleibt häufig ungeklärt. Das ist kein Zeichen von schlechtem Willen – es ist ein Muster, das sich über Zeit eingeschlichen hat.

Erste Anzeichen:
- Zuständigkeiten werden stillschweigend vorausgesetzt statt klar geregelt
- Konflikte werden eher umgangen als direkt angesprochen
- Loyalität steht häufig vor offener Klärung

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken.""",

            "Führungsteam":
            """In Ihrem Führungsteam gibt es Hinweise auf ein Anpassungsmuster: Erwartungen bleiben oft implizit, Spannungen werden durch Anpassung bewältigt statt durch Klärung. Das ist kein Versagen einzelner Personen – es ist ein Muster, das sich über Zeit entwickelt hat.

Erste Anzeichen:
- Erwartungen bleiben implizit statt ausgesprochen
- Themen werden besprochen, aber selten wirklich abgeschlossen
- Harmonie wird manchmal über Klarheit gestellt

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken."""
        },

        "Schutz und Inkonsistenz": {
            "Organisation":
            """Ihre Organisation zeigt Hinweise auf ein Muster aus Schutz und Inkonsistenz: Führungssignale kommen nicht einheitlich an, und gleichzeitig wird nicht alles nach oben kommuniziert. Das erzeugt Unklarheit darüber, was wirklich erwartet wird – kein Versagen einzelner Personen, sondern ein strukturelles Zusammenspiel.

Erste Anzeichen:
- Probleme werden wahrgenommen, aber selten direkt nach oben kommuniziert
- Prioritäten wirken von oben nicht immer einheitlich
- Zwischen Führung und Organisation entsteht zunehmend Distanz

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken.""",

            "Führungsteam":
            """Ihr Führungsteam zeigt Hinweise auf ein Muster aus Schutz und Inkonsistenz: Nicht alles wird offen angesprochen, und die gemeinsame Ausrichtung wirkt nicht durchgängig stabil. Das führt dazu, dass vorsichtiges Handeln Klarheit ersetzt – kein Versagen einzelner Personen, sondern ein Muster, das sich über Zeit entwickelt hat.

Erste Anzeichen:
- Kritische Themen werden im Team eher umgangen als angesprochen
- Erwartungen werden unterschiedlich interpretiert
- Die gemeinsame Ausrichtung wirkt situativ, nicht durchgängig

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken."""
        },

        "Strukturproblem": {
            "Organisation":
            """Ihre Organisation zeigt Hinweise auf ein strukturelles Muster: Verantwortung und Entscheidungswege sind nicht klar genug geregelt, Themen wandern zwischen Rollen ohne Abschluss. Das ist kein Zeichen von mangelndem Engagement – es ist ein Muster, das sich strukturell klären lässt.

Erste Anzeichen:
- Es ist nicht immer klar, wer Entscheidungen treffen darf oder soll
- Verantwortung wird übergeben, ohne dass Mandat und Rückendeckung gesichert sind
- Themen werden mehrfach besprochen ohne verbindlichen Abschluss

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken.""",

            "Führungsteam":
            """Ihr Führungsteam zeigt Hinweise auf ein strukturelles Muster: Rollen, Mandate und Entscheidungswege sind nicht durchgängig klar, was verbindliche Zusammenarbeit erschwert. Das ist kein Zeichen von mangelndem Engagement – es ist ein Muster, das sich strukturell klären lässt.

Erste Anzeichen:
- Zuständigkeiten überlappen oder bleiben ungeklärt
- Entscheidungen werden mehrfach aufgerufen ohne Abschluss
- Einzelne tragen Verantwortung ohne ausreichende Rückendeckung

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken."""
        },

        "Stabil": {
            "Organisation":
            """Ihre Organisation zeigt in allen drei Bereichen grundsätzlich tragfähige Strukturen. Verantwortung wird übernommen, Spannungen können angesprochen werden, Führung gibt Orientierung. Das sind gute Voraussetzungen – und gleichzeitig der Punkt, an dem sich zeigt, wo das nächste Entwicklungsniveau liegt.

Erste Anzeichen:
- Entscheidungen werden getroffen und auch umgesetzt
- Spannungen können offen angesprochen werden
- Strategische Orientierung ist im Alltag erkennbar

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken.""",

            "Führungsteam":
            """Ihr Führungsteam zeigt in allen drei Bereichen grundsätzlich tragfähige Strukturen. Verantwortung ist klar, Spannungen können angesprochen werden, Orientierung ist spürbar. Das sind gute Voraussetzungen – und gleichzeitig der Punkt, an dem sich zeigt, wo das nächste Entwicklungsniveau liegt.

Erste Anzeichen:
- Gemeinsame Ausrichtung ist erkennbar und stabil
- Konflikte werden konstruktiv bearbeitet
- Das Team kann gemeinsam Führung übernehmen

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken."""
        },

        "Gemischtes Muster": {
            "Organisation":
            """Ihre Organisation zeigt ein gemischtes Bild: Einige Bereiche funktionieren gut, in anderen gibt es noch Klärungsbedarf. Das ist häufiger als man denkt – und die Unterschiede selbst geben oft wichtige Hinweise darauf, was das System zusammenhält.

Erste Anzeichen:
- Manche Entscheidungen laufen reibungslos, andere stocken
- Psychologische Sicherheit ist situativ vorhanden, aber nicht überall gleich
- Führung wirkt in Teilen klar, in anderen Bereichen uneinheitlich

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken.""",

            "Führungsteam":
            """Ihr Führungsteam zeigt ein gemischtes Bild: Einige Bereiche funktionieren gut, in anderen gibt es noch Klärungsbedarf. Das ist häufiger als man denkt – und die Unterschiede selbst geben oft wichtige Hinweise darauf, was das Team zusammenhält.

Erste Anzeichen:
- In manchen Situationen läuft die Zusammenarbeit reibungslos, in anderen nicht
- Verantwortung und Orientierung sind teilweise klar, teilweise noch offen
- Das Team schöpft sein gemeinsames Potenzial noch nicht voll aus

Entscheidend ist jedoch nicht das Muster selbst – sondern wodurch es in Ihrer Organisation stabil bleibt. Genau hier unterscheiden sich Organisationen oft deutlich.

Im ausführlichen Bericht sehen Sie: welche Dynamiken Ihr Ergebnis konkret antreiben, warum sich das Muster im Alltag stabilisiert und welche Ansatzpunkte erfahrungsgemäß tatsächlich wirken."""
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
