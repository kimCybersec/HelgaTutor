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
        
        # Use datetime.now() instead of SERVER_TIMESTAMP
        timestamp = datetime.now()
        
        # Prepare the new message data
        new_message = {
            "user": user_msg,
            "bot": helga_msg,
            "timestamp": timestamp
        }
        
        # Update the document
        session_ref.set({
            "session": firestore.ArrayUnion([new_message]),
            "last_updated": timestamp,
            "level": "A1"  # Default level, can be updated from chat.py
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
            # Sort messages by timestamp if needed
            messages = data.get("session", [])
            return sorted(messages, key=lambda x: x.get('timestamp', ''))
        return []
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        raise RuntimeError(f"Failed to get chat history: {str(e)}")