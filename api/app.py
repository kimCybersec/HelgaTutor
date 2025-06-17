from flask import Flask
from flask_cors import CORS
from api.routes.chat import chat_bp
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://mentalhealthbuddy-1.onrender.com",
    "http://mentalhealthbuddy-1.onrender.com"
]}})

app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return {"message": "Mental Health Chatbot API is running!"}
