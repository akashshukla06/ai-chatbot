const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const logoutButton = document.getElementById("logoutButton");
const clearChatButton = document.getElementById("clearChatButton");
const themeButton = document.getElementById("themeButton");

const API_BASE = (window.location.protocol.startsWith("http")) 
    ? window.location.origin 
    : "http://127.0.0.1:8000";

// ==========================================
// 1. THEME TOGGLE FOR INDEX.HTML
// ==========================================

function initTheme() {
    const savedTheme = localStorage.getItem("abes_theme") || "light";
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        if (themeButton) themeButton.textContent = "☀️";
    } else {
        document.body.classList.remove("dark-mode");
        if (themeButton) themeButton.textContent = "🌙";
    }
}

if (themeButton) {
    themeButton.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        localStorage.setItem("abes_theme", isDark ? "dark" : "light");
        themeButton.textContent = isDark ? "☀️" : "🌙";
    });
}

// ==========================================
// 2. LOGOUT BUTTON FOR INDEX.HTML
// ==========================================

function handleLogout() {
    console.log("Logging out...");
    if (logoutButton) logoutButton.textContent = "Logging out...";
    try {
        localStorage.removeItem("abes_token");
        localStorage.removeItem("abes_role");
        localStorage.removeItem("abes_user");
        sessionStorage.clear();
        fetch(`${API_BASE}/logout`, { method: "POST" }).catch(() => {});
    } catch (e) {
        console.warn(e);
    }
    setTimeout(() => {
        window.location.replace("login.html");
    }, 150);
}

if (logoutButton) {
    logoutButton.addEventListener("click", (e) => {
        e.preventDefault();
        handleLogout();
    });
}

// ==========================================
// 3. CLEAR CHAT BUTTON FOR INDEX.HTML
// ==========================================

async function clearConversation() {
    console.log("Clearing conversation...");
    if (clearChatButton) {
        const orig = clearChatButton.textContent;
        clearChatButton.textContent = "✓ Cleared";
        setTimeout(() => { clearChatButton.textContent = orig; }, 1500);
    }

    if (chatBox) {
        chatBox.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <strong>ABES AI Assistant</strong>
                    <p>Hello! 👋</p>
                    <p>Chat history cleared. How can I help you today? You can ask about ABES courses, admissions, hostel, or your attendance and exams.</p>
                </div>
            </div>
        `;
    }

    const token = localStorage.getItem("abes_token");
    if (token) {
        try {
            await fetch(`${API_BASE}/chat/history`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
            console.log("Chat history cleared on server.");
        } catch (err) {
            console.warn("Server clear error:", err);
        }
    }
}

if (clearChatButton) {
    clearChatButton.addEventListener("click", (e) => {
        e.preventDefault();
        clearConversation();
    });
}

// ==========================================
// 4. ADD MESSAGE WITH SOURCE ATTRIBUTION
// ==========================================

function addMessage(message, sender, source = "", sourceUrl = "") {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }

    const avatarDiv = document.createElement("div");
    avatarDiv.classList.add("message-avatar");
    avatarDiv.textContent = sender === "user" ? "👨‍🎓" : "🤖";
    messageDiv.appendChild(avatarDiv);

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");

    if (sender === "bot") {
        const title = document.createElement("strong");
        title.textContent = "ABES AI Assistant";
        contentDiv.appendChild(title);
    }

    const textPara = document.createElement("p");
    let formatted = escapeHtml(message)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
    textPara.innerHTML = formatted;
    contentDiv.appendChild(textPara);

    // Source transparency badge
    if (sender === "bot" && source) {
        const sourceDiv = document.createElement("div");
        sourceDiv.style.marginTop = "8px";
        sourceDiv.style.fontSize = "11px";
        sourceDiv.style.opacity = "0.85";
        sourceDiv.style.borderTop = "1px solid rgba(0,0,0,0.1)";
        sourceDiv.style.paddingTop = "4px";

        if (sourceUrl) {
            sourceDiv.innerHTML = `🏛️ Source: <a href="${sourceUrl}" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline;">${escapeHtml(source)} ↗</a>`;
        } else {
            sourceDiv.innerHTML = `🏛️ Source: ${escapeHtml(source)}`;
        }
        contentDiv.appendChild(sourceDiv);
    }

    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ==========================================
// 5. SEND QUESTION TO FASTAPI
// ==========================================

async function sendMessage(questionText = null) {
    const question = (questionText !== null ? questionText : userInput.value).trim();

    if (question === "") return;

    addMessage(question, "user");
    if (userInput) userInput.value = "";

    if (sendButton) {
        sendButton.disabled = true;
        sendButton.textContent = "Thinking...";
    }

    const headers = { "Content-Type": "application/json" };
    const token = localStorage.getItem("abes_token");
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();
        addMessage(data.answer, "bot", data.source, data.source_url);

    } catch (error) {
        console.error("Error:", error);
        addMessage(
            "Sorry, I could not connect to the chatbot server. Please make sure FastAPI is running.",
            "bot"
        );
    } finally {
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.textContent = "Send ➤";
        }
        if (userInput) userInput.focus();
    }
}

if (sendButton) {
    sendButton.addEventListener("click", () => sendMessage());
}

if (userInput) {
    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
}

// ==========================================
// 6. QUICK QUESTIONS BUTTONS & CARDS
// ==========================================

document.querySelectorAll(".quick-question").forEach(btn => {
    btn.addEventListener("click", () => {
        const q = btn.getAttribute("data-question");
        if (q) sendMessage(q);
    });
});

document.querySelectorAll(".dashboard-card").forEach(card => {
    card.addEventListener("click", () => {
        const heading = card.querySelector("h3")?.textContent?.trim().toLowerCase();
        if (heading === "attendance") {
            sendMessage("What is my attendance?");
        } else if (heading === "subjects") {
            sendMessage("What subjects do I have?");
        } else if (heading === "examinations") {
            sendMessage("When is my next exam?");
        } else if (heading === "notices") {
            sendMessage("Where can I find ABES notices and circulars?");
        }
    });
});

// Load existing history if token exists
async function loadHistory() {
    const token = localStorage.getItem("abes_token");
    if (!token) return;
    try {
        const res = await fetch(`${API_BASE}/chat/history`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            if (data.history && data.history.length > 0) {
                chatBox.innerHTML = "";
                data.history.forEach(item => {
                    addMessage(item.question, "user");
                    addMessage(item.answer, "bot", item.source, "");
                });
            }
        }
    } catch (e) {
        console.warn("Could not load history on index:", e);
    }
}

initTheme();
loadHistory();

// Global exports
window.handleLogout = handleLogout;
window.clearConversation = clearConversation;