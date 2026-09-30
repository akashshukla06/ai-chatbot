// =========================================================
// ABES Engineering College Portal - Authentication Controller
// =========================================================

const loginForm = document.getElementById("loginForm");
const studentIdInput = document.getElementById("studentId");
const passwordInput = document.getElementById("password");
const submitBtn = document.getElementById("submitBtn");
const messageBox = document.getElementById("message");

const API_BASE = "http://127.0.0.1:8000";

// Helper to quick-fill credentials for demonstration / testing
function fillCredentials(id, pass) {
    studentIdInput.value = id;
    passwordInput.value = pass;
    studentIdInput.focus();
}

function showMessage(text, type = "error") {
    messageBox.style.display = "block";
    messageBox.className = `message-box ${type}`;
    messageBox.textContent = text;
}

function hideMessage() {
    messageBox.style.display = "none";
    messageBox.textContent = "";
}

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideMessage();

    const usernameOrId = studentIdInput.value.trim();
    const password = passwordInput.value;

    if (!usernameOrId || !password) {
        showMessage("Please enter your Student ID and password.", "error");
        return;
    }

    // Set loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = "<span>Authenticating...</span>";

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username_or_id: usernameOrId,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            // Friendly error message returned by backend or fallback
            const errorMsg = data.detail || "Invalid Student ID or password.";
            showMessage(errorMsg, "error");
            submitBtn.disabled = false;
            submitBtn.innerHTML = "<span>Sign In to Portal</span>";
            return;
        }

        // Successful authentication
        showMessage("Login successful! Redirecting to student portal...", "success");

        // Securely store token and profile in localStorage
        localStorage.setItem("abes_token", data.access_token);
        localStorage.setItem("abes_role", data.role);
        localStorage.setItem("abes_user", JSON.stringify(data.user));

        setTimeout(() => {
            if (data.role === "admin") {
                window.location.href = "admin.html";
            } else {
                // If dashboard.html exists, go to dashboard; otherwise index.html
                window.location.href = "dashboard.html";
            }
        }, 800);

    } catch (error) {
        console.error("Login communication error:", error);
        showMessage("Unable to connect to the portal backend. Please ensure FastAPI server is running.", "error");
        submitBtn.disabled = false;
        submitBtn.innerHTML = "<span>Sign In to Portal</span>";
    }
});