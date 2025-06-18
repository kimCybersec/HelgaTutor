# 🧠 Mental Health Buddy Chatbot

A supportive and multilingual mental health chatbot built with **Flask**, **OpenAI**, **Google Generative AI**, and **Firebase**. The bot is themed for **Men's Mental Health Month**, and provides a simple, comforting interface for expressing emotions and receiving AI-powered responses.


## 🌐 Live Demo

- Frontend: [https://mentalhealth-buddy.vercel.app](https://mentalhealth-buddy.vercel.app)
- Backend API: [https://mentalhealthbuddy.onrender.com](https://mentalhealthbuddy.onrender.com)


## 📦 Features

- 💬 Conversational AI with OpenAI and Gemini integration
- 🌍 Multilingual support: English, German, Swahili
- 💾 Persistent chat history with Firebase Firestore
- 📱 Responsive UI (desktop + mobile)
- 🎨 Soft, masculine design with avatars and timestamps
- 🧠 Designed for emotional comfort and user privacy

---

## 🛠️ Tech Stack

| Area          | Technology                     |
|---------------|--------------------------------|
| Frontend      | HTML, CSS, JavaScript          |
| Backend       | Flask (Python)                 |
| AI Models     | OpenAI GPT, Google Gemini 2.0  |
| Database      | Firebase Firestore             |
| Deployment    | Vercel (frontend), Render (API)|

## ⚙️ Setup Instructions

### 1. Clone the repo

bash
git clone https://github.com/yourusername/mentalHealthbuddy.git
cd mentalhealth-bot



Create a `.env` file with the following:

OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_google_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

 3. Install dependencies

```bash
pip install -r api/requirements.txt
```

### 4. Run locally

```bash
cd api
python app.py
```

Visit: `http://localhost:5000`


## 🚀 Deployment

* **Frontend**: Push the `/static` and `/templates` folder to Vercel.
* **Backend**: Deploy `/api` directory to Render or another Flask-compatible server.
* **Firebase**: Set up Firestore with a collection per `session_id` to store messages.


## 🧠 Credits

* Built with [Firebase](https://firebase.google.com), and [Gemini](https://ai.google.dev/).
* Designed for awareness and emotional wellness during **Men's Mental Health Month**.
* Developed with ❤️ by PH03N1X


## 📜 License

MIT License — free for personal and educational use.

# HelgaTutor
