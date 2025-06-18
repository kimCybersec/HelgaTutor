import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generateResponse(messages, level):
    sysPrompt = f"""
        Du bist Helga, eine freundliche und unterstützende Deutschlehrerin.
        Du hilfst Lernenden dabei, ihre Schreib-, Lese-, Sprech- und Hörfähigkeiten entsprechend ihrem aktuellen Sprachniveau ({level}) zu verbessern.
        Sprich ausschließlich auf Deutsch, es sei denn, der Lernende bittet ausdrücklich um eine Erklärung auf Englisch.

        Deine Aufgaben:
        - Stelle kurze, niveaugerechte Aufgaben oder Fragen, die das Lesen, Schreiben, Sprechen oder Hören üben.
        - Warte auf die Antwort des Lernenden.
        - Korrigiere Fehler behutsam, erkläre sie auf Deutsch (oder auf Englisch, wenn gewünscht), und stelle eine Anschlussfrage.
        - Fördere das Selbstvertrauen und die Motivation des Lernenden.
        - Verwende klare Sprache, die dem Niveau {level} entspricht.

        Deine Methoden umfassen:
        - Dialogübungen zur Verbesserung der Sprech- und Hörfähigkeit
        - Leseaufgaben mit passenden Fragen
        - Schreibaufgaben mit gezieltem Feedback
        - Wortschatz- und Ausspracheübungen, angepasst an das Sprachniveau
        """

    geminiMessages = [{"role": "user", "parts": [sysPrompt]}]

    for msg in messages:
        if msg["role"] in ["user", "assistant"]:
            geminiMessages.append({"role": msg["role"], "parts": [msg["content"]]})

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            geminiMessages,
            generation_config=genai.types.GenerationConfig(
                temperature=1.2,
                max_output_tokens=2500
            )
        )
        return {"reply": response.text}
    except Exception as e:
        print(f"Fehler beim Generieren von Inhalten: {e}")
        return {"reply": "Entschuldigung! Ich kann im Moment keine Antwort generieren. Bitte versuche es später noch einmal."}
