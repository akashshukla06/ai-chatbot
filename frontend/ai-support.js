// =========================================================
// ABES Engineering College - AI Student Support Desk Controller
// Dedicated Q&A Interface connected to FastAPI /chat endpoint
// Conversation flow: User Question -> AI Answer -> Input at Bottom
// =========================================================

const API_BASE = "http://127.0.0.1:8000";

let token = localStorage.getItem("abes_token");

document.addEventListener("DOMContentLoaded", async () => {
    initTheme();

    const userInput = document.getElementById("userInput");
    if (userInput) {
        userInput.focus();
        userInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                submitInquiry();
            }
        });
    }

    // Load past chat history if user is authenticated
    if (token) {
        await loadExistingHistory();
    }
});

// =========================================================
// 1. THEME & NAVIGATION
// =========================================================

function initTheme() {
    const savedTheme = localStorage.getItem("abes_theme") || "theme-light";
    document.body.className = savedTheme;
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const isDark = document.body.classList.contains("theme-dark");
    const newTheme = isDark ? "theme-light" : "theme-dark";
    document.body.className = newTheme;
    localStorage.setItem("abes_theme", newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById("themeIcon");
    if (icon) {
        icon.textContent = theme === "theme-dark" ? "☀️" : "🌙";
    }
}

function toggleMobileNav() {
    const nav = document.getElementById("navMenu");
    if (nav) {
        nav.classList.toggle("open");
    }
}

function handleLogout() {
    localStorage.removeItem("abes_token");
    localStorage.removeItem("abes_role");
    localStorage.removeItem("abes_user");
    window.location.href = "login.html";
}

// =========================================================
// 2. CHAT HISTORY MANAGEMENT & CLEAR
// =========================================================

async function loadExistingHistory() {
    try {
        const res = await fetch(`${API_BASE}/chat/history`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            if (data.history && data.history.length > 0) {
                const streamBox = document.getElementById("chatBox");
                if (streamBox) {
                    streamBox.innerHTML = "";
                    data.history.forEach(item => {
                        renderRecord(item.question, "user");
                        renderRecord(item.answer, "bot", item.source, "");
                    });
                    scrollToLatest();
                }
            }
        }
    } catch (e) {
        console.warn("Could not load consultation history:", e);
    }
}

async function clearInquiries() {
    const streamBox = document.getElementById("chatBox");
    if (streamBox) {
        streamBox.innerHTML = `
            <div class="response-record bot-record">
                <div class="record-meta">
                    <span class="responder-tag">🤖 ABES Student Support</span>
                    <span class="response-time">Official Desk</span>
                </div>
                <div class="record-body">
                    <p>Ask a question about ABES, academics, examinations or student services.</p>
                </div>
            </div>
        `;
        streamBox.scrollTop = 0;
    }

    if (token) {
        try {
            await fetch(`${API_BASE}/chat/history`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
        } catch (e) {
            console.warn("Server history clear warning:", e);
        }
    }
}

// =========================================================
// 3. SUBMIT INQUIRY (USER QUESTION -> AI ANSWER -> AUTO-SCROLL)
// =========================================================

function askQuickQuestion(question) {
    const input = document.getElementById("userInput");
    if (input) input.value = question;
    submitInquiry(question);
}

async function submitInquiry(overrideText = null) {
    const input = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendButton");
    const question = (overrideText !== null ? overrideText : (input ? input.value : "")).trim();

    if (!question) return;

    if (input) input.value = "";
    
    // 1. Render user question above input area
    renderRecord(question, "user");
    
    // 2. Show loading/typing indicator immediately below user question
    showConsultationTyping();
    scrollToLatest();

    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.textContent = "Processing...";
    }

    const headers = { "Content-Type": "application/json" };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ question: question })
        });

        removeConsultationTyping();

        if (!response.ok) {
            renderRecord(
                "The Student Support server is temporarily unavailable. Please verify the FastAPI service is active.",
                "bot",
                "System Error"
            );
            scrollToLatest();
            return;
        }

        const data = await response.json();
        
        // 3. Render AI answer directly below that question
        renderRecord(data.answer, "bot", data.source, data.source_url);
        
        // 4. Smooth auto-scroll only within conversation container
        scrollToLatest();

    } catch (err) {
        console.error("Consultation fetch error:", err);
        removeConsultationTyping();
        renderRecord(
            "Unable to connect to the ABES Student Support backend. Please check network connectivity or ensure FastAPI is running on http://127.0.0.1:8000.",
            "bot",
            "Connection Error"
        );
        scrollToLatest();
    } finally {
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.textContent = "Ask Question ➤";
        }
        if (input) input.focus();
    }
}

// =========================================================
// 4. RECORD RENDERING & INTERNAL SCROLLING
// =========================================================

function renderRecord(text, sender, source = "", sourceUrl = "") {
    const streamBox = document.getElementById("chatBox");
    if (!streamBox) return;

    const record = document.createElement("div");
    record.className = `response-record ${sender === "user" ? "user-record" : "bot-record"}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const meta = document.createElement("div");
    meta.className = "record-meta";
    meta.innerHTML = `
        <span class="responder-tag">${sender === "user" ? "👤 You" : "🤖 ABES Student Support"}</span>
        <span class="response-time">${timeStr}</span>
    `;
    record.appendChild(meta);

    const body = document.createElement("div");
    body.className = "record-body";
    const formatted = escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
    body.innerHTML = formatted;
    record.appendChild(body);

    if (sender === "bot" && source) {
        const sourceDiv = document.createElement("div");
        sourceDiv.className = "record-source";
        if (sourceUrl) {
            sourceDiv.innerHTML = `🏛️ Source: <a href="${sourceUrl}" target="_blank" rel="noopener noreferrer">${escapeHtml(source)} ↗</a>`;
        } else {
            sourceDiv.innerHTML = `🏛️ Source: ${escapeHtml(source)}`;
        }
        record.appendChild(sourceDiv);
    }

    streamBox.appendChild(record);
}

function showConsultationTyping() {
    const streamBox = document.getElementById("chatBox");
    if (!streamBox) return;

    // Remove any lingering indicator
    removeConsultationTyping();

    const record = document.createElement("div");
    record.className = "response-record bot-record";
    record.id = "inquiryTypingIndicator";

    record.innerHTML = `
        <div class="record-meta">
            <span class="responder-tag">🤖 ABES Student Support</span>
            <span class="response-time">Consulting Knowledge Base</span>
        </div>
        <div class="typing-box">
            <span>Searching official college records & Gemini AI</span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;

    streamBox.appendChild(record);
}

function removeConsultationTyping() {
    const el = document.getElementById("inquiryTypingIndicator");
    if (el) el.remove();
}

function scrollToLatest() {
    const streamBox = document.getElementById("chatBox");
    if (streamBox) {
        streamBox.scrollTop = streamBox.scrollHeight;
    }
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

// Global bindings
window.submitInquiry = submitInquiry;
window.askQuickQuestion = askQuickQuestion;
window.clearInquiries = clearInquiries;
window.toggleTheme = toggleTheme;
window.toggleMobileNav = toggleMobileNav;
window.handleLogout = handleLogout;
