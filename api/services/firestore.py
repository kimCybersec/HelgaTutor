import os
import json
import base64
from api.utils.logger import logger
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
        
        existing_data = session_ref.get().to_dict() or {}
        existing_messages = existing_data.get("session", [])
        
        new_messages = existing_messages + [{
            "user": user_msg,
            "bot": helga_msg,
            "timestamp": firestore.SERVER_TIMESTAMP
        }]
        
        session_ref.set({
            "session": new_messages[-20:],
            "last_updated": firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        logger.error(f"Error saving chat: {e}")
        raise

def getChatHistory(session_id):
    try:
        session_ref = db.collection('helgaSessions').document(session_id)
        session_doc = session_ref.get()
        if session_doc.exists:
            data = session_doc.to_dict()
            return data.get("session", [])
        else:
            return []
    except Exception as e:
        raise RuntimeError(f"Failed to get chat history for {session_id}: {e}")

