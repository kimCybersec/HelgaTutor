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
        level = data.get("level", []) 
        sessionId = data.get("sessionId", "anonymous")
        history = getChatHistory(sessionId)
        all_messages = history + messages        
        result = generateResponse(all_messages, level)
        saveChat(
            sessionId, 
            messages[-1]['content'] if messages else "", 
            result['reply']
        )
        
        return jsonify({
            "reply": result['reply'],
            "timestamp": result['timestamp']
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            "error": str(e),
            "reply": "Entschuldigung! Es gab ein Problem."
        }), 500  
    
@chat_bp.route('/history/<sessionId>', methods=['GET']) 
@limiter 
def history(sessionId): 
    try: 
        logger.info(f"Fetching history for session: {sessionId}")
        history = getChatHistory(sessionId) 
        logger.info(f"Session result: {history}")
        return jsonify({"history": history})  
    
    except Exception as e: 
        logger.error(f"History error for session {sessionId}: {str(e)}") 
        return jsonify({"error": str(e)}), 500

