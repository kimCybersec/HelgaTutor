import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generateResponse(messages, level):
    sysPrompt = f"""
        You are Helga an AI german chatbot and tutor, your main goal is to help students better their german sprechen, hören, lesen und schreiben you can do this by engaging in conversations with the user based on their level {level} and also offer lessons whenever requested
        You are patient and respectful and always ready to proceed with a conversation
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
                temperature=1.5,
                max_output_tokens=1000
            )
        )
        return {"reply": response.text}
    except Exception as e:
        print(f"Fehler beim Generieren von Inhalten: {e}")
        return {"reply": "Entschuldigung! Ich kann im Moment keine Antwort generieren. Bitte versuche es später noch einmal."}


