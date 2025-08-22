document.addEventListener('DOMContentLoaded', function() {
    // Initialize all UI elements with null checks
    const chatBox = document.getElementById('chat-box');
    const form = document.getElementById('chat-form');
    const clearBtn = document.getElementById('clear-session');
    const levelSelect = document.getElementById('level');
    const voiceBtn = document.getElementById('voice-btn');
    const input = document.getElementById('message');
    const sendBtn = document.querySelector('#chat-form button[type="submit"]');

    // Debug: Verify elements exist
    if (!chatBox || !form || !clearBtn || !levelSelect || !voiceBtn || !input || !sendBtn) {
        console.error('Missing required elements:', {
            chatBox, form, clearBtn, levelSelect, voiceBtn, input, sendBtn
        });
        return;
    }

    const apiBase = "https://helgatutorapi.onrender.com/api/chat";
    let sessionId = localStorage.getItem("sessionId") || generateSessionId();
    localStorage.setItem("sessionId", sessionId);
    let isListening = false;
    let recognition;

    // Helper functions
    function generateSessionId() {
        return 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }

    function setLoading(state) {
        sendBtn.disabled = state;
        sendBtn.innerHTML = state 
            ? '<i class="fas fa-spinner fa-spin"></i>' 
            : '<i class="fas fa-paper-plane"></i>';
    }

    function showSystemMessage(text, type = 'info') {
        const msg = document.createElement('div');
        msg.className = `system-message ${type}`;
        msg.innerHTML = `<i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i> ${text}`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Main chat functions
    function addMessage(role, content) {
        try {
            const msg = document.createElement('div');
            msg.className = `message ${role}`;

            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.innerHTML = role === 'user' 
                ? '<i class="fas fa-user"></i>' 
                : '<i class="fas fa-robot"></i>';

            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            bubble.innerHTML = role === 'assistant' 
                ? marked.parse(content) 
                : document.createTextNode(content).textContent;

            const time = document.createElement('div');
            time.className = 'timestamp';
            time.textContent = new Date().toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
            });

            msg.appendChild(avatar);
            msg.appendChild(bubble);
            msg.appendChild(time);
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (err) {
            console.error('Error adding message:', err);
            showSystemMessage('Error displaying message', 'error');
        }
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const typingBubble = document.createElement('div');
        typingBubble.className = 'bubble typing-indicator';
        typingBubble.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(typingBubble);
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    // Voice recognition functions
    function initializeVoiceRecognition() {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "de-DE";

        recognition.onstart = () => {
            isListening = true;
            voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
            voiceBtn.style.backgroundColor = 'var(--danger)';
            voiceBtn.classList.add('listening');
            showSystemMessage('Voice recognition activated. Speak now...');
        };

        recognition.onerror = (event) => {
            console.error("Voice error:", event.error);
            resetVoiceUI();
            showSystemMessage(`Voice error: ${event.error}`, 'error');
        };

        recognition.onend = () => {
            if (isListening) recognition.start();
            else resetVoiceUI();
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            input.value = finalTranscript + interimTranscript;
        };
    }

    function resetVoiceUI() {
        isListening = false;
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceBtn.style.backgroundColor = 'var(--primary)';
        voiceBtn.classList.remove('listening');
    }

    function handleVoiceInput() {
        if (!isListening) {
            if (!recognition) initializeVoiceRecognition();
            recognition.start();
        } else {
            isListening = false;
            recognition.stop();
        }
    }

    // API communication functions
    async function loadHistory() {
        try {
            showTypingIndicator();
            const res = await fetch(`${apiBase}/history/${sessionId}`);
            
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();
            hideTypingIndicator();

            if (Array.isArray(data.history)) {
                data.history.forEach(msg => {
                    // Check for the correct keys
                    if (msg.role === "user") {
                        addMessage("user", msg.content);
                    } else if (msg.role === "assistant") {
                        addMessage("assistant", msg.content);
                    }
                });
                
                if (data.history.length === 0) {
                    addMessage("assistant", "Hallo! Ich bin Helga, deine Deutschlehrerin. Wie kann ich dir heute helfen?");
                }
            } else {
                addMessage("assistant", "Willkommen! Lass uns Deutsch üben. Worüber möchtest du sprechen?");
            }
        } catch (err) {
            console.error("Failed to load chat history:", err);
            hideTypingIndicator();
            showSystemMessage("Couldn't load chat history", 'error');
            addMessage("assistant", "Hallo! Lass uns Deutsch lernen. Was möchtest du üben?");
        }
    }

    async function sendMessage(msg) {
        if (!msg.trim()) return;

        addMessage("user", msg);
        input.value = "";
        setLoading(true);
        showTypingIndicator();

        try {
            // Get current conversation from DOM for context, filter out empty content
            const conversation = Array.from(document.querySelectorAll('.message'))
                .map(el => {
                    return {
                        role: el.classList.contains('user') ? 'user' : 'assistant',
                        content: el.querySelector('.bubble').innerText
                    };
                })
                .filter(m => m.content && m.content.trim().length > 0); // <-- filter out empty

            const payload = {
                messages: conversation,
                level: levelSelect.value,
                sessionId: sessionId
            };

            const res = await fetch(apiBase, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error(`Server responded with ${res.status}`);
            }

            const data = await res.json();
            addMessage("assistant", data.reply);
        } catch (err) {
            console.error("Error sending message:", err);
            showSystemMessage(`Error: ${err.message}`, 'error');
            addMessage("assistant", "Entschuldigung! Es gab ein Problem. Bitte versuche es erneut.");
        } finally {
            setLoading(false);
            hideTypingIndicator();
        }
    }

    // Event listeners
    form.onsubmit = async (e) => {
        e.preventDefault();
        const msg = input.value.trim();
        if (!msg) return;
        await sendMessage(msg);
    };

    clearBtn.onclick = () => {
        if (confirm("Möchtest du wirklich eine neue Sitzung starten? Der gesamte Chat-Verlauf wird gelöscht.")) {
            localStorage.removeItem("sessionId");
            sessionId = generateSessionId();
            localStorage.setItem("sessionId", sessionId);
            chatBox.innerHTML = '';
            addMessage("assistant", "Hallo! Ich bin Helga. Lass uns eine neue Deutschstunde beginnen!");
        }
    };

    voiceBtn.onclick = handleVoiceInput;

    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Initialize
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        voiceBtn.style.display = 'block';
    } else {
        voiceBtn.style.display = 'none';
    }

    loadHistory();
});