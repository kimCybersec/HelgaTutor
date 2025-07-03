import google.generativeai as genai
import os
import json
from datetime import datetime

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
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare conversation history in correct format
        chat = model.start_chat(history=[])
        
        # Add system prompt first
        response = chat.send_message(sysPrompt)
        
        # Add conversation history
        for msg in messages[-6:]:  # Keep last 6 messages for context
            if msg['role'] == 'user':
                response = chat.send_message(msg['content'])
            elif msg['role'] == 'assistant':
                # For assistant messages, we need to add them to history
                chat.history.append({
                    'role': 'model',
                    'parts': [msg['content']]
                })
        
        return {
            "reply": response.text,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return {
            "reply": "Entschuldigung! Ich habe ein Problem. Bitte versuche es später noch einmal.",
            "timestamp": datetime.now().isoformat()
        }