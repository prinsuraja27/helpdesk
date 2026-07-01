const API_BASE = "https://helpdesk-f8n9.onrender.com";
const ADMIN_KEY_VALUE = "campus-admin-123";

let adminKey = "";
let currentRequests = [];

const loginSection = document.getElementById("loginSection");
const dashboardSection = document.getElementById("dashboardSection");
const adminKeyInput = document.getElementById("adminKey");
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");
const loginMessage = document.getElementById("loginMessage");
const adminMessage = document.getElementById("adminMessage");
const requestsTableBody = document.getElementById("requestsTableBody");
const refreshBtn = document.getElementById("refreshBtn");
const detailModal = document.getElementById("detailModal");
const detailBox = document.getElementById("detailBox");
const closeModal = document.getElementById("closeModal");

function setMessage(element, text, isSuccess = true) {
    if (!element) return;
    element.textContent = text;
    element.style.color = isSuccess ? "#16a34a" : "#dc2626";
}

function adminHeaders() {
    return {
        "Content-Type": "application/json",
        "x-admin-key": adminKey
    };
}

if (loginBtn) {
    loginBtn.addEventListener("click", async () => {
        adminKey = adminKeyInput.value.trim();

        if (!adminKey) {
            setMessage(loginMessage, "Please enter admin key.", false);
            return;
        }

        if (adminKey !== ADMIN_KEY_VALUE) {
            setMessage(loginMessage, "Invalid admin key.", false);
            return;
        }

        setMessage(loginMessage, "", true);

        loginSection.classList.add("hidden");
        dashboardSection.classList.remove("hidden");

        await loadDashboard();
        await loadRequests();
    });
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        adminKey = "";
        adminKeyInput.value = "";
        dashboardSection.classList.add("hidden");
        loginSection.classList.remove("hidden");
        setMessage(adminMessage, "", true);
    });
}

if (refreshBtn) {
    refreshBtn.addEventListener("click", async () => {
        await loadDashboard();
        await loadRequests();
    });
}

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`, {
            method: "GET",
            headers: adminHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load dashboard");
        }

        document.getElementById("totalCount").textContent = data.total_requests || 0;
        document.getElementById("pendingCount").textContent = data.pending_requests || 0;
        document.getElementById("progressCount").textContent = data.progress_requests || 0;
        document.getElementById("solvedCount").textContent = data.solved_requests || 0;
        document.getElementById("rejectedCount").textContent = data.rejected_requests || 0;

    } catch (error) {
        console.error("Dashboard error:", error);
        setMessage(adminMessage, "Dashboard load failed: " + error.message, false);
    }
}

async function loadRequests() {
    try {
        const response = await fetch(`${API_BASE}/requests`, {
            method: "GET",
            headers: adminHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load requests");
        }

        currentRequests = Array.isArray(data) ? data : [];
        renderRequests(currentRequests);

    } catch (error) {
        console.error("Requests error:", error);
        setMessage(adminMessage, "Requests load failed: " + error.message, false);
    }
}

function renderRequests(requests) {
    requestsTableBody.innerHTML = "";

    if (!requests || requests.length === 0) {
        requestsTableBody.innerHTML = `
            <tr>
                <td colspan="11" style="text-align:center;">No requests found.</td>
            </tr>
        `;
        return;
    }

    requests.forEach((request) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${request.request_id || "-"}</td>
            <td>${request.student_name || "-"}</td>
            <td>${request.enrollment || "-"}</td>
            <td>${request.department || "-"}</td>
            <td>${request.phone || "-"}</td>
            <td>${request.email || "-"}</td>
            <td>${request.request_type || "-"}</td>
            <td>${shortText(request.message || "", 60)}</td>
            <td><span class="status-pill status-${request.status || "pending"}">${request.status || "pending"}</span></td>
            <td>${request.created_at || "-"}</td>
            <td>
                <div class="action-buttons">
                    <button class="small-btn view-btn" onclick="viewDetails('${request.request_id}')">View</button>
                    <button class="small-btn progress-btn" onclick="updateStatus('${request.request_id}', 'progress')">Progress</button>
                    <button class="small-btn solved-btn" onclick="updateStatus('${request.request_id}', 'solved')">Solved</button>
                    <button class="small-btn rejected-btn" onclick="updateStatus('${request.request_id}', 'rejected')">Rejected</button>
                    <button class="small-btn delete-btn" onclick="deleteRequest('${request.request_id}')">Delete</button>
                </div>
            </td>
        `;

        requestsTableBody.appendChild(row);
    });
}

function shortText(text, limit) {
    if (!text) return "";
    return text.length > limit ? text.substring(0, limit) + "..." : text;
}

async function updateStatus(requestId, status) {
    try {
        const response = await fetch(`${API_BASE}/requests/${encodeURIComponent(requestId)}/status`, {
            method: "PUT",
            headers: adminHeaders(),
            body: JSON.stringify({ status: status })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Status update failed");
        }

        setMessage(adminMessage, "Status updated successfully.", true);

        await loadDashboard();
        await loadRequests();

    } catch (error) {
        console.error("Status update error:", error);
        setMessage(adminMessage, "Status update failed: " + error.message, false);
    }
}

async function deleteRequest(requestId) {
    const confirmDelete = confirm("Are you sure you want to delete this request?");
    if (!confirmDelete) return;

    try {
        const response = await fetch(`${API_BASE}/requests/${encodeURIComponent(requestId)}`, {
            method: "DELETE",
            headers: adminHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Delete failed");
        }

        setMessage(adminMessage, "Request deleted successfully.", true);

        await loadDashboard();
        await loadRequests();

    } catch (error) {
        console.error("Delete error:", error);
        setMessage(adminMessage, "Delete failed: " + error.message, false);
    }
}

function viewDetails(requestId) {
    const request = currentRequests.find((item) => item.request_id === requestId);

    if (!request) {
        setMessage(adminMessage, "Request not found.", false);
        return;
    }

    detailBox.innerHTML = `
        <div class="detail-row"><strong>Request ID:</strong> ${request.request_id || "-"}</div>
        <div class="detail-row"><strong>Student Name:</strong> ${request.student_name || "-"}</div>
        <div class="detail-row"><strong>Enrollment Number:</strong> ${request.enrollment || "-"}</div>
        <div class="detail-row"><strong>Department:</strong> ${request.department || "-"}</div>
        <div class="detail-row"><strong>Phone Number:</strong> ${request.phone || "-"}</div>
        <div class="detail-row"><strong>Email:</strong> ${request.email || "-"}</div>
        <div class="detail-row"><strong>Request Type:</strong> ${request.request_type || "-"}</div>
        <div class="detail-row"><strong>Status:</strong> <span class="status-pill status-${request.status || "pending"}">${request.status || "pending"}</span></div>
        <div class="detail-row"><strong>Submitted Date/Time:</strong> ${request.created_at || "-"}</div>
        <div class="detail-row"><strong>Problem Message:</strong><br>${request.message || "-"}</div>
    `;

    detailModal.classList.remove("hidden");
}

if (closeModal) {
    closeModal.addEventListener("click", () => {
        detailModal.classList.add("hidden");
    });
}

if (detailModal) {
    detailModal.addEventListener("click", (event) => {
        if (event.target === detailModal) {
            detailModal.classList.add("hidden");
        }
    });
}
