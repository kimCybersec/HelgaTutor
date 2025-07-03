import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generateResponse(messages, level):
    sysPrompt = f"""
    You are Helga, an AI German chatbot and tutor. Your main goal is to help students improve their German skills.
    Current user level: {level}
    
    Guidelines:
    1. Maintain context of the ongoing conversation
    2. Adapt responses to the user's language level
    3. Be patient and encouraging
    4. Provide corrections when appropriate
    5. Keep responses natural and conversational
    
    Current conversation context:
    {json.dumps(messages[-6:], indent=2) if messages else "New conversation"}
    """
    
    try:
        gemini_messages = []
        for msg in messages[-10:]:  
            if msg['role'] == 'system':
                continue
            gemini_messages.append({
                'role': 'user' if msg['role'] == 'user' else 'model',
                'parts': [msg['content']]
            })
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            {"contents": gemini_messages},
            generation_config=genai.types.GenerationConfig(
                temperature=0.7 if level in ["A1", "A2"] else 1.0,
                max_output_tokens=1000
            )
        )
        
        return {"reply": response.text}
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"reply": "Entschuldigung! Ich habe ein Problem. Bitte versuche es später noch einmal."}