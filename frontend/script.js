const API_BASE = "http://localhost:8000";

const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const sendChatBtn = document.getElementById('send-chat-btn');

function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user-message');
    chatInput.value = '';
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    typingDiv.id = 'current-typing-indicator';
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        
        document.getElementById('current-typing-indicator')?.remove();

        if (response.ok && data.response) {
            appendMessage(data.response, 'bot-message');
            
            const intentBadge = document.getElementById('meta-intent');
            const complexBadge = document.getElementById('meta-complexity');
            const cacheBadge = document.getElementById('meta-cached');
            const timeBadge = document.getElementById('meta-time');
            const tokensBadge = document.getElementById('meta-tokens');
            const contextBox = document.getElementById('retrieved-context-box');
            
            if (intentBadge) intentBadge.textContent = "Intent: " + (data.intent || 'Unknown');
            if (complexBadge) complexBadge.textContent = "Complexity: " + (data.complexity || 'Unknown');
            if (cacheBadge) cacheBadge.textContent = "Cache Hit: " + (data.is_cached ? 'True' : 'False');
            if (timeBadge) timeBadge.textContent = "Gen Time: " + (data.generation_time || 0) + "s";
            if (tokensBadge) tokensBadge.textContent = "Tokens (est): " + (data.input_tokens_est || 0);
            
            if (contextBox) {
                if (data.context && data.context.length > 0) {
                    contextBox.textContent = JSON.stringify(data.context, null, 2);
                } else {
                    contextBox.textContent = "No relevant context found in Vector Database for this query.";
                }
            }
        } else {
            const errorMsg = data.message || "Could not get a proper response.";
            appendMessage(`Error: ${errorMsg}`, 'system-message');
            if (data.detail) {
                console.error("Error detail:", data.detail);
            }
        }
    } catch (err) {
        document.getElementById('current-typing-indicator')?.remove();
        appendMessage("Connection error: Is the backend running?", 'system-message');
    }
}

sendChatBtn.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMessage();
});

async function clearCache() {
    if (!confirm("Are you sure you want to delete the semantic _db_cache directory? This will remove all learned cache embeddings.")) return;
    try {
        const response = await fetch(`${API_BASE}/chat/clear_cache`, { method: 'DELETE' });
        const data = await response.json();
        alert(JSON.stringify(data));
    } catch (e) {
        alert("Failed to clear cache: " + e.message);
    }
}

