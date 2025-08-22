from flask import Flask
from flask_cors import CORS
from api.routes.chat import chat_bp


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://helgatutor.onrender.com",
    "https://helgatutorapi.onrender.com"
]}})

app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return {"message": "Helga the tutor is running perfectly fine!"}
