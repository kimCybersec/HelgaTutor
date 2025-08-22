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

def saveChat(sessionId, user_msg, helga_msg, level):
    try:
        session_ref = db.collection('helgaSessions').document(sessionId)
        timestamp = datetime.now()
        
        # get messages
        existing_data = session_ref.get().to_dict() or {}
        existing_messages = existing_data.get("messages", [])
        
        # add message
        new_messages = existing_messages + [
            {"role": "user", "content": user_msg, "timestamp": timestamp},
            {"role": "assistant", "content": helga_msg, "timestamp": timestamp}
        ]
        
        # update document with all messages
        session_ref.set({
            "messages": new_messages[-20:],
            "last_updated": timestamp,
            "level": level
        }, merge=True)
        
    except Exception as e:
        print(f"Error saving chat: {str(e)}")
        raise RuntimeError(f"Failed to save chat: {str(e)}")

def getChatHistory(sessionId):
    try:
        session_ref = db.collection('helgaSessions').document(sessionId)
        session_doc = session_ref.get()
        
        if session_doc.exists:
            data = session_doc.to_dict()
            messages = data.get("messages", [])
            return sorted(messages, key=lambda x: x.get('timestamp', ''))
        return []
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        raise RuntimeError(f"Failed to get chat history: {str(e)}")