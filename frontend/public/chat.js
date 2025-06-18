const apiBase = "https://helgatutorapi.onrender.com/api/chat";
let sessionId = localStorage.getItem("session_id") || Date.now().toString();
localStorage.setItem("session_id", sessionId);

const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const clearBtn = document.getElementById("clear-session");
const langSelect = document.getElementById("language-select");
const levelSelect = document.getElementById("level");
const voiceBtn = document.getElementById("voice-btn");
const input = document.getElementById("message");

function addMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = role === "user" ? "user.png" : "bot.png";
  avatar.alt = `${role} avatar`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (role === "assistant") {
    bubble.innerHTML = marked.parse(content);
    speak(content); 
  } else {
    bubble.innerText = content;
  }

  const time = document.createElement("div");
  time.className = "timestamp";
  time.innerText = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  msg.appendChild(time);
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadHistory() {
  try {
    const res = await fetch(`${apiBase}/history/${sessionId}`);
    const data = await res.json();

    if (Array.isArray(data.history)) {
      data.history.forEach(m => {
        if (m.user || m.student) addMessage("user", m.user || m.student);
        if (m.bot || m.Helga) addMessage("assistant", m.bot || m.Helga);

      });
    } else {
      addMessage("assistant", "⚠️ Invalid chat history format.");
    }
  } catch (err) {
    console.error("Failed to load chat history:", err);
    addMessage("assistant", "⚠️ Could not load chat history.");
  }
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const msg = input.value.trim();
  if (!msg) return;
  await sendMessage(msg);
};

clearBtn.onclick = () => {
  localStorage.removeItem("session_id");
  location.reload();
};

voiceBtn.onclick = () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "de-DE";
  recognition.interimResults = false;

  recognition.onstart = () => {
    voiceBtn.innerText = "🎙️ Listening...";
  };

  recognition.onerror = (event) => {
    console.error("Voice error:", event.error);
    voiceBtn.innerText = "🎤 Voice Input";
  };

  recognition.onend = () => {
    voiceBtn.innerText = "🎤 Voice Input";
  };

  recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    await sendMessage(transcript);
  };

  recognition.start();
};

async function sendMessage(msg) {
  addMessage("user", msg);
  input.value = "";

  try {
    const res = await fetch(apiBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: msg }],
        lang: langSelect?.value || "de",
        level: levelSelect?.value || "A1",
        session_id: sessionId
      })
    });

    const data = await res.json();
    addMessage("assistant", data.reply);
  } catch (err) {
    console.error("Fetch error:", err);
    addMessage("assistant", "⚠️ Error reaching the server.");
  }
}

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "de-DE";
  speechSynthesis.speak(utterance);
}

window.onload = loadHistory;
