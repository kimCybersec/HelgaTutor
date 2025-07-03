import os
import json
import base64
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app

credData = os.environ.get("GOOGLE_CREDENTIALS")

if credData:
    decoded = base64.b64decode(credData).decode("utf-8")
    credJson = json.loads(decoded)
    cred = credentials.Certificate(credJson)
else:
    cred = credentials.Certificate("mensmentalhealth.json")

initialize_app(cred)

db = firestore.client()

def saveChat(session_id, user_msg, helga_msg):
    try:
        session_ref = db.collection('helgaSessions').document(session_id)
        timestamp = datetime.now()
        
        # Get existing messages
        existing_data = session_ref.get().to_dict() or {}
        existing_messages = existing_data.get("messages", [])
        
        # Add new message pair
        new_messages = existing_messages + [
            {"role": "user", "content": user_msg, "timestamp": timestamp},
            {"role": "assistant", "content": helga_msg, "timestamp": timestamp}
        ]
        
        # Update document with all messages
        session_ref.set({
            "messages": new_messages[-20:],  # Keep last 20 messages (10 exchanges)
            "last_updated": timestamp,
            "level": "A1"  # Default, can be updated
        }, merge=True)
        
    except Exception as e:
        print(f"Error saving chat: {str(e)}")
        raise RuntimeError(f"Failed to save chat: {str(e)}")

def getChatHistory(session_id):
    try:
        session_ref = db.collection('helgaSessions').document(session_id)
        session_doc = session_ref.get()
        
        if session_doc.exists:
            data = session_doc.to_dict()
            messages = data.get("messages", [])
            # Return sorted by timestamp and formatted for Gemini
            return sorted(messages, key=lambda x: x.get('timestamp', ''))
        return []
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        raise RuntimeError(f"Failed to get chat history: {str(e)}")