const apiBase = "https://helgatutorapi.onrender.com/api/chat";
let sessionId = localStorage.getItem("session_id") || generateSessionId();
localStorage.setItem("session_id", sessionId);

// Generate a more unique session ID
function generateSessionId() {
    return 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

// Load conversation history with context
async function loadHistory() {
    try {
        const res = await fetch(`${apiBase}/history/${sessionId}`);
        const data = await res.json();

        if (Array.isArray(data.history)) {
            // Process history to maintain context
            data.history.forEach(msg => {
                if (msg.user) addMessage("user", msg.user);
                if (msg.bot) addMessage("assistant", msg.bot);
            });
            
            // If no history, start with a welcome message
            if (data.history.length === 0) {
                addMessage("assistant", "Hallo! Ich bin Helga, deine Deutschlehrerin. Wie kann ich dir heute helfen?");
            }
        } else {
            addMessage("assistant", "Willkommen! Lass uns Deutsch üben. Worüber möchtest du sprechen?");
        }
    } catch (err) {
        console.error("Failed to load chat history:", err);
        addMessage("assistant", "Hallo! Lass uns Deutsch lernen. Was möchtest du üben?");
    }
}

// Send message with context
async function sendMessage(msg) {
    if (!msg.trim()) return;
    
    addMessage("user", msg);
    input.value = "";
    showTypingIndicator();
    
    try {
        // Get current conversation for context
        const conversation = getCurrentConversation();
        
        const res = await fetch(apiBase, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                messages: [
                    ...conversation,
                    { role: "user", content: msg }
                ],
                level: levelSelect.value,
                session_id: sessionId
            })
        });

        const data = await res.json();
        hideTypingIndicator();
        addMessage("assistant", data.reply);
    } catch (err) {
        hideTypingIndicator();
        console.error("Fetch error:", err);
        addMessage("assistant", "⚠️ Es gab ein Problem mit der Verbindung. Bitte versuche es erneut.");
    }
}

// Get current conversation from DOM
function getCurrentConversation() {
    const messages = [];
    const messageElements = document.querySelectorAll('.message');
    
    messageElements.forEach(el => {
        const role = el.classList.contains('user') ? 'user' : 'assistant';
        const content = el.querySelector('.bubble').innerText;
        messages.push({ role, content });
    });
    
    return messages;
}

// Clear session properly
clearBtn.onclick = () => {
    if (confirm("Möchtest du wirklich eine neue Sitzung starten? Der gesamte Chat-Verlauf wird gelöscht.")) {
        localStorage.removeItem("session_id");
        sessionId = generateSessionId();
        localStorage.setItem("session_id", sessionId);
        chatBox.innerHTML = '';
        addMessage("assistant", "Hallo! Ich bin Helga. Lass uns eine neue Deutschstunde beginnen!");
    }
};