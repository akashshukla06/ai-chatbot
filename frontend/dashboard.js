// =========================================================
// ABES Student Support AI Portal - Dashboard Controller
// =========================================================

const API_BASE = "http://127.0.0.1:8000";

let currentStudent = null;
let token = localStorage.getItem("abes_token");

// =========================================================
// 1. INITIALIZATION & AUTHENTICATION CHECK
// =========================================================

document.addEventListener("DOMContentLoaded", async () => {
    initTheme();

    // Verify token
    if (!token) {
        window.location.replace("login.html");
        return;
    }

    // Attach explicit click event listeners to buttons
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            handleLogout();
        });
    }

    const clearChatBtn = document.getElementById("clearChatBtn");
    if (clearChatBtn) {
        clearChatBtn.addEventListener("click", (e) => {
            e.preventDefault();
            clearConversation();
        });
    }

    try {
        await loadStudentProfile();
        await loadQuickStats();
        await loadChatHistory();
    } catch (err) {
        console.error("Initialization error:", err);
    }

    // Enter key listener on chat input
    const userInput = document.getElementById("userInput");
    if (userInput) {
        userInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendClick();
            }
        });
    }
});

// =========================================================
// 2. THEME MANAGEMENT (LIGHT / DARK)
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

// =========================================================
// 3. LOAD STUDENT PROFILE & STATS
// =========================================================

async function loadStudentProfile() {
    const res = await fetch(`${API_BASE}/student/profile`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.status === 401 || res.status === 403) {
        handleLogout();
        return;
    }

    if (!res.ok) throw new Error("Failed to load profile");

    currentStudent = await res.json();

    // Populate Welcome Banner & Meta Bar
    const heading = document.getElementById("welcomeHeading");
    if (heading) heading.textContent = `👋 Welcome back, ${currentStudent.name}!`;

    const mId = document.getElementById("metaStudentId");
    if (mId) mId.textContent = `ID: ${currentStudent.student_id}`;

    const mCourse = document.getElementById("metaCourse");
    if (mCourse) mCourse.textContent = `Course: ${currentStudent.course}`;

    const mBranch = document.getElementById("metaBranch");
    if (mBranch) mBranch.textContent = `Branch: ${currentStudent.branch}`;

    const mSem = document.getElementById("metaSemester");
    if (mSem) mSem.textContent = `Sem: ${currentStudent.semester}`;

    const mSec = document.getElementById("metaSection");
    if (mSec) mSec.textContent = `Sec: ${currentStudent.section}`;
}

async function loadQuickStats() {
    // 1. Attendance
    try {
        const attRes = await fetch(`${API_BASE}/student/attendance`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (attRes.ok) {
            const data = await attRes.json();
            const pct = data.overall_percentage || 0;
            const m = document.getElementById("cardAttendanceMetric");
            if (m) m.textContent = `${pct}%`;

            const fill = document.getElementById("cardAttendanceFill");
            if (fill) fill.style.width = `${Math.min(pct, 100)}%;`;

            const statusTxt = pct >= 75 ? "Eligible (Above 75%)" : "Shortage Warning (< 75%)";
            const s = document.getElementById("cardAttendanceStatus");
            if (s) s.textContent = `${data.total_attended || 0}/${data.total_classes || 0} classes • ${statusTxt}`;
        }
    } catch (e) {
        console.warn("Could not load attendance stat:", e);
    }

    // 2. Subjects
    try {
        const subRes = await fetch(`${API_BASE}/student/subjects`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (subRes.ok) {
            const data = await subRes.json();
            const count = data.subjects ? data.subjects.length : 0;
            const m = document.getElementById("cardSubjectsMetric");
            if (m) m.textContent = `${count} Subjects`;

            const s = document.getElementById("cardSubjectsStatus");
            if (s) s.textContent = `Enrolled for Sem ${currentStudent?.semester || 6}`;
        }
    } catch (e) {
        console.warn("Could not load subjects stat:", e);
    }

    // 3. Exams
    try {
        const examRes = await fetch(`${API_BASE}/student/exams`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (examRes.ok) {
            const data = await examRes.json();
            const m = document.getElementById("cardExamsMetric");
            const s = document.getElementById("cardExamsStatus");
            if (data.exams && data.exams.length > 0) {
                const nextEx = data.exams[0];
                if (m) m.textContent = `Next: ${nextEx.subject_code}`;
                const countdown = nextEx.days_left > 0 ? `in ${nextEx.days_left} days` : "scheduled";
                if (s) s.textContent = `${nextEx.exam_date} (${countdown})`;
            } else {
                if (m) m.textContent = "None";
                if (s) s.textContent = "No upcoming exams";
            }
        }
    } catch (e) {
        console.warn("Could not load exams stat:", e);
    }

    // 4. Notices
    try {
        const notRes = await fetch(`${API_BASE}/student/notices`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (notRes.ok) {
            const data = await notRes.json();
            const count = data.notices ? data.notices.length : 0;
            const m = document.getElementById("cardNoticesMetric");
            if (m) m.textContent = `${count} Updates`;

            const s = document.getElementById("cardNoticesStatus");
            if (s) s.textContent = "Official circulars posted";
        }
    } catch (e) {
        console.warn("Could not load notices stat:", e);
    }
}

// =========================================================
// 4. CHAT HISTORY & MESSAGE RENDERING
// =========================================================

async function loadChatHistory() {
    try {
        const res = await fetch(`${API_BASE}/chat/history`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            if (data.history && data.history.length > 0) {
                const chatBox = document.getElementById("chatBox");
                if (chatBox) {
                    chatBox.innerHTML = "";
                    data.history.forEach(item => {
                        appendMessage(item.question, "user");
                        appendMessage(item.answer, "bot", item.source, "");
                    });
                }
            }
        }
    } catch (e) {
        console.warn("Could not load chat history:", e);
    }
}

function appendMessage(text, sender, source = "", sourceUrl = "") {
    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;

    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}-message`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    if (sender === "bot") {
        const header = document.createElement("div");
        header.className = "message-header";
        header.textContent = "🤖 ABES Support Assistant";
        bubble.appendChild(header);
    }

    const textDiv = document.createElement("div");
    textDiv.className = "message-text";
    const formatted = escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
    textDiv.innerHTML = formatted;
    bubble.appendChild(textDiv);

    if (sender === "bot" && source) {
        const sourceBadge = document.createElement("div");
        sourceBadge.className = "source-badge";
        if (sourceUrl) {
            sourceBadge.innerHTML = `🏛️ Source: <a href="${sourceUrl}" target="_blank" rel="noopener noreferrer">${escapeHtml(source)} ↗</a>`;
        } else {
            sourceBadge.innerHTML = `🏛️ Source: ${escapeHtml(source)}`;
        }
        bubble.appendChild(sourceBadge);
    }

    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;

    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message";
    typingDiv.id = "typingIndicator";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

    bubble.appendChild(dots);
    typingDiv.appendChild(bubble);
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const el = document.getElementById("typingIndicator");
    if (el) el.remove();
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

// =========================================================
// 5. SEND QUESTION CONTROLLER
// =========================================================

async function handleSendClick() {
    const input = document.getElementById("userInput");
    if (!input) return;
    const question = input.value.trim();
    if (!question) return;

    input.value = "";
    await sendQuestion(question);
}

function sendQuickQuestion(question) {
    sendQuestion(question);
}

async function sendQuestion(question) {
    appendMessage(question, "user");
    showTypingIndicator();

    const sendBtn = document.getElementById("sendBtn");
    if (sendBtn) sendBtn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ question: question })
        });

        removeTypingIndicator();

        if (!res.ok) {
            appendMessage("I apologize, but I encountered a server issue. Please try again.", "bot");
            return;
        }

        const data = await res.json();
        appendMessage(data.answer, "bot", data.source, data.source_url);

    } catch (err) {
        removeTypingIndicator();
        console.error("Chat error:", err);
        appendMessage("Unable to reach the assistant server. Please verify the FastAPI backend is running.", "bot");
    } finally {
        if (sendBtn) sendBtn.disabled = false;
        const input = document.getElementById("userInput");
        if (input) input.focus();
    }
}

// =========================================================
// 6. CLEAR CHAT (IMMEDIATE UI RESET + DATABASE PURGE)
// =========================================================

async function clearConversation() {
    console.log("Clearing conversation...");
    const activeToken = localStorage.getItem("abes_token") || token;

    // 1. Immediately reset the chatbox DOM
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        chatBox.innerHTML = `
            <div class="message bot-message">
                <div class="message-bubble">
                    <div class="message-header">🤖 ABES Support Assistant</div>
                    <div class="message-text">
                        Chat history cleared! 👋<br><br>
                        How can I help you? You can ask about ABES or your attendance, subjects, and exams.
                    </div>
                </div>
            </div>
        `;
    }

    // 2. Asynchronously delete from MySQL
    if (activeToken) {
        try {
            await fetch(`${API_BASE}/chat/history`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${activeToken}` }
            });
            console.log("Database chat history successfully cleared.");
        } catch (err) {
            console.warn("Could not delete chat history on server:", err);
        }
    }
}

// =========================================================
// 7. LOGOUT FUNCTION (CLEARS STATE & REDIRECTS)
// =========================================================

function handleLogout() {
    console.log("Logging out of ABES portal...");
    try {
        localStorage.removeItem("abes_token");
        localStorage.removeItem("abes_role");
        localStorage.removeItem("abes_user");
        sessionStorage.clear();
        fetch(`${API_BASE}/logout`, { method: "POST" }).catch(() => {});
    } catch (err) {
        console.warn("Logout cleanup warning:", err);
    }

    // Redirect cleanly to login.html
    window.location.replace("login.html");
}

// =========================================================
// 8. MODALS CONTROLLER
// =========================================================

async function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add("active");

    if (modalId === "attendanceModal") await renderAttendanceModal();
    else if (modalId === "subjectsModal") await renderSubjectsModal();
    else if (modalId === "examsModal") await renderExamsModal();
    else if (modalId === "noticesModal") await renderNoticesModal();
    else if (modalId === "profileModal") renderProfileModal();
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("active");
}

function closeOnBackdrop(event, modalId) {
    if (event.target.id === modalId) {
        closeModal(modalId);
    }
}

async function renderAttendanceModal() {
    const body = document.getElementById("attendanceModalBody");
    if (!body) return;
    body.innerHTML = '<div class="modal-spinner">Loading verified attendance...</div>';

    try {
        const res = await fetch(`${API_BASE}/student/attendance`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        if (!data.records || data.records.length === 0) {
            body.innerHTML = `<p>${data.message || "Attendance data is not available yet."}</p>`;
            return;
        }

        const isGood = data.overall_percentage >= 75;
        let html = `
            <div class="att-meter-box">
                <div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 2px;">Overall Attendance</div>
                    <div class="att-meter-score">${data.overall_percentage}%</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">${data.total_attended} of ${data.total_classes} classes attended</div>
                </div>
                <div class="att-meter-pill" style="background: ${isGood ? 'var(--success-soft)' : 'var(--warning-soft)'}; color: ${isGood ? 'var(--success)' : 'var(--warning)'}; border: 1px solid currentColor;">
                    ${isGood ? '✅ Eligible for Exams' : '⚠️ Low Attendance Warning'}
                </div>
            </div>
            <h4 style="margin-bottom: 12px; font-size: 13px; text-transform: uppercase; color: var(--text-muted);">Subject-wise Breakdown:</h4>
        `;

        data.records.forEach(r => {
            const pct = r.attendance_percentage;
            const barColor = pct >= 75 ? 'var(--success)' : 'var(--warning)';
            html += `
                <div class="att-sub-item">
                    <div class="att-sub-header">
                        <span>${escapeHtml(r.subject_name)} <small style="color: var(--text-muted);">(${escapeHtml(r.subject_code)})</small></span>
                        <span style="color: ${barColor};">${pct}%</span>
                    </div>
                    <div class="card-progress-bar" style="height: 7px;">
                        <div class="card-progress-fill" style="width: ${Math.min(pct, 100)}%; background: ${barColor};"></div>
                    </div>
                    <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                        Attended ${r.attended_classes} of ${r.total_classes} lectures
                    </div>
                </div>
            `;
        });

        body.innerHTML = html;
    } catch (e) {
        body.innerHTML = '<p style="color: #dc2626;">Error loading attendance records.</p>';
    }
}

async function renderSubjectsModal() {
    const body = document.getElementById("subjectsModalBody");
    if (!body) return;
    body.innerHTML = '<div class="modal-spinner">Loading enrolled subjects...</div>';

    try {
        const res = await fetch(`${API_BASE}/student/subjects`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        if (!data.subjects || data.subjects.length === 0) {
            body.innerHTML = '<p>No enrolled subjects found.</p>';
            return;
        }

        let html = '<div style="display: flex; flex-direction: column; gap: 10px;">';
        data.subjects.forEach(s => {
            html += `
                <div class="att-sub-item">
                    <div style="font-weight: 600; font-size: 14px; color: var(--text-primary);">${escapeHtml(s.subject_name)}</div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
                        Code: <strong>${escapeHtml(s.subject_code)}</strong> • Semester: ${s.semester} • Branch: ${escapeHtml(s.branch)}
                    </div>
                </div>
            `;
        });
        html += '</div>';
        body.innerHTML = html;
    } catch (e) {
        body.innerHTML = '<p style="color: #dc2626;">Error loading subjects.</p>';
    }
}

async function renderExamsModal() {
    const body = document.getElementById("examsModalBody");
    if (!body) return;
    body.innerHTML = '<div class="modal-spinner">Loading examination timetable...</div>';

    try {
        const res = await fetch(`${API_BASE}/student/exams`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        if (!data.exams || data.exams.length === 0) {
            body.innerHTML = `<p>${data.message || "No upcoming examination data is available."}</p>`;
            return;
        }

        let html = '';
        data.exams.forEach(ex => {
            html += `
                <div class="exam-item-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                        <h4 style="font-size: 14px; font-weight: 700; color: var(--text-primary);">${escapeHtml(ex.subject_name)} (${escapeHtml(ex.subject_code)})</h4>
                        <span class="notice-cat-badge">${escapeHtml(ex.exam_type)}</span>
                    </div>
                    <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 4px;">
                        📅 Date: <strong>${ex.exam_date}</strong> (in ${ex.days_left} days)
                    </div>
                    <div style="font-size: 12px; color: var(--text-muted);">
                        ⏰ Time: ${ex.start_time} - ${ex.end_time} • 🏛️ Examination Room: <strong>${escapeHtml(ex.room)}</strong>
                    </div>
                </div>
            `;
        });
        body.innerHTML = html;
    } catch (e) {
        body.innerHTML = '<p style="color: #dc2626;">Error loading exam schedule.</p>';
    }
}

async function renderNoticesModal() {
    const body = document.getElementById("noticesModalBody");
    if (!body) return;
    body.innerHTML = '<div class="modal-spinner">Loading official notices...</div>';

    try {
        const res = await fetch(`${API_BASE}/student/notices`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        if (!data.notices || data.notices.length === 0) {
            body.innerHTML = '<p>No circulars available at this moment.</p>';
            return;
        }

        let html = '';
        data.notices.forEach(n => {
            html += `
                <div class="notice-item-card">
                    <span class="notice-cat-badge">${escapeHtml(n.category)}</span>
                    <h4 style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">${escapeHtml(n.title)}</h4>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">Date: ${n.notice_date}</p>
                    <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px;">${escapeHtml(n.description)}</p>
                    ${n.source_url ? `<a href="${n.source_url}" target="_blank" rel="noopener noreferrer" style="font-size: 12px; color: var(--primary); font-weight: 600; text-decoration: none;">View Official Notice ↗</a>` : ''}
                </div>
            `;
        });
        body.innerHTML = html;
    } catch (e) {
        body.innerHTML = '<p style="color: #dc2626;">Error loading notices.</p>';
    }
}

function renderProfileModal() {
    const body = document.getElementById("profileModalBody");
    if (!body) return;
    if (!currentStudent) {
        body.innerHTML = '<p>Profile data unavailable.</p>';
        return;
    }

    body.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Full Name</small>
                <strong>${escapeHtml(currentStudent.name)}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Student ID / Roll No</small>
                <strong>${escapeHtml(currentStudent.student_id)}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Official Email</small>
                <strong>${escapeHtml(currentStudent.email)}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Degree & Course</small>
                <strong>${escapeHtml(currentStudent.course)}</strong>
            </div>
            <div class="att-sub-item" style="grid-column: span 2;">
                <small style="color: var(--text-muted); display: block;">Department / Branch</small>
                <strong>${escapeHtml(currentStudent.branch)}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Semester</small>
                <strong>Semester ${currentStudent.semester}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Section</small>
                <strong>${escapeHtml(currentStudent.section)}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Enrollment Year</small>
                <strong>${currentStudent.enrollment_year}</strong>
            </div>
            <div class="att-sub-item">
                <small style="color: var(--text-muted); display: block;">Academic Affiliation</small>
                <strong>AKTU, Lucknow</strong>
            </div>
        </div>
    `;
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

// =========================================================
// 9. EXPLICIT GLOBAL WINDOW BINDINGS
// =========================================================

window.handleLogout = handleLogout;
window.clearConversation = clearConversation;
window.toggleTheme = toggleTheme;
window.openModal = openModal;
window.closeModal = closeModal;
window.closeOnBackdrop = closeOnBackdrop;
window.sendQuickQuestion = sendQuickQuestion;
window.handleSendClick = handleSendClick;
window.scrollToTop = scrollToTop;
