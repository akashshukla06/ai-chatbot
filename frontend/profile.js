// =========================================================
// ABES Engineering College - Student Profile Controller
// Fetches official student profile from FastAPI /student/profile
// =========================================================

const API_BASE = (window.location.protocol.startsWith("http")) 
    ? window.location.origin 
    : "http://127.0.0.1:8000";

let token = localStorage.getItem("abes_token");

document.addEventListener("DOMContentLoaded", async () => {
    initTheme();

    if (!token) {
        window.location.replace("login.html");
        return;
    }

    try {
        await loadStudentProfileData();
    } catch (err) {
        console.error("Profile load error:", err);
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
// 2. FETCH AND POPULATE STUDENT DOSSIER
// =========================================================

async function loadStudentProfileData() {
    const res = await fetch(`${API_BASE}/student/profile`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.status === 401 || res.status === 403) {
        handleLogout();
        return;
    }

    if (!res.ok) {
        throw new Error("Unable to retrieve official profile from server");
    }

    const student = await res.json();

    // Populate Dossier Elements
    setElementText("profStudentName", student.name || "Student Record");
    setElementText("profRollBadge", `Roll: ${student.student_id || "--"}`);

    setElementText("fieldFullName", student.name || "--");
    setElementText("fieldStudentId", student.student_id || "--");
    setElementText("fieldEmail", student.email || "--");
    setElementText("fieldCourse", student.course || "--");
    setElementText("fieldBranch", student.branch || "--");
    setElementText("fieldSemester", `Semester ${student.semester || "--"}`);
    setElementText("fieldSection", student.section ? `Section ${student.section}` : "--");
    setElementText("fieldYear", student.enrollment_year ? `Batch of ${student.enrollment_year}` : "--");
}

function setElementText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

// Global bindings
window.toggleTheme = toggleTheme;
window.toggleMobileNav = toggleMobileNav;
window.handleLogout = handleLogout;
