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

        # Generate response
        result = generateResponse(messages, level)
        
        # Save to Firestore
        saveChat(
            session_id, 
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
    
@chat_bp.route('/history/<session_id>', methods=['GET']) 
@limiter 
def history(session_id): 
    try: 
        logger.info(f"Fetching history for session: {session_id}")
        history = getChatHistory(session_id) 
        logger.info(f"Session result: {history}")
        return jsonify({"history": history})  
    
    except Exception as e: 
        logger.error(f"History error for session {session_id}: {str(e)}") 
        return jsonify({"error": str(e)}), 500

