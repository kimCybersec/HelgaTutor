from flask import Blueprint, request, jsonify 
from api.middleware.rateLimiter import limiter 
from api.services.firestore import saveChat, getChatHistory 
from api.services.openaiHelper import generateResponse 
from api.utils.logger import logger

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('', methods=['POST']) 
@limiter 
def chat(): 
    try: 
        data = request.get_json() 
        messages = data.get("messages", []) 
        level = data.get("level", "A1") 
        session_id = data.get("session_id", "anonymous")

        result = generateResponse(messages, level)
        saveChat(session_id, messages[-1]['content'], result['reply'])
        return jsonify(result)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/history/<session_id>', methods=['GET']) 
@limiter 
def history(session_id): 
    try: 
        logger.info(f"Fetching history for session: {session_id}")
        history = getChatHistory(session_id) 
        logger.info(f"Session result: {history}")
        return jsonify({"history": history})  # ✅ FIXED
    
    except Exception as e: 
        logger.error(f"History error for session {session_id}: {str(e)}") 
        return jsonify({"error": str(e)}), 500

