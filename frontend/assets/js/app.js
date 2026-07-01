const API_BASE = "https://helpdesk-f8n9.onrender.com";

const requestForm = document.getElementById("studentRequestForm");
const formMessage = document.getElementById("formMessage");

const checkStatusBtn = document.getElementById("checkStatusBtn");
const statusRequestId = document.getElementById("statusRequestId");
const statusResult = document.getElementById("statusResult");

function showMessage(element, text, isSuccess = true) {
    if (!element) return;
    element.textContent = text;
    element.style.color = isSuccess ? "#16a34a" : "#dc2626";
}

if (requestForm) {
    requestForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const requestData = {
            request_id: document.getElementById("request_id").value.trim(),
            student_name: document.getElementById("student_name").value.trim(),
            enrollment: document.getElementById("enrollment").value.trim(),
            department: document.getElementById("department").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            email: document.getElementById("email").value.trim(),
            request_type: document.getElementById("request_type").value,
            message: document.getElementById("message").value.trim()
        };

        try {
            const response = await fetch(`${API_BASE}/requests`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage(formMessage, data.detail || "Request submit failed", false);
                return;
            }

            showMessage(formMessage, "Request submitted successfully. Admin can now view it.", true);

            // Form only success ke baad clear hoga
            requestForm.reset();

        } catch (error) {
            console.error("Submit error:", error);
            showMessage(formMessage, "Backend connection failed. Please try again.", false);
        }
    });
}

if (checkStatusBtn) {
    checkStatusBtn.addEventListener("click", async function () {
        const requestId = statusRequestId.value.trim();

        if (!requestId) {
            statusResult.innerHTML = `<p style="color:#dc2626;">Please enter Request ID.</p>`;
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/requests/${encodeURIComponent(requestId)}`);
            const data = await response.json();

            if (!response.ok) {
                statusResult.innerHTML = `<p style="color:#dc2626;">${data.detail || "Request not found"}</p>`;
                return;
            }

            statusResult.innerHTML = `
                <div class="card">
                    <h3>Request Status</h3>
                    <p><strong>Request ID:</strong> ${data.request_id || "-"}</p>
                    <p><strong>Student Name:</strong> ${data.student_name || "-"}</p>
                    <p><strong>Enrollment:</strong> ${data.enrollment || "-"}</p>
                    <p><strong>Department:</strong> ${data.department || "-"}</p>
                    <p><strong>Request Type:</strong> ${data.request_type || "-"}</p>
                    <p><strong>Status:</strong> <span class="status-pill status-${data.status || "pending"}">${data.status || "pending"}</span></p>
                    <p><strong>Submitted At:</strong> ${data.created_at || "-"}</p>
                    <p><strong>Message:</strong> ${data.message || "-"}</p>
                </div>
            `;

        } catch (error) {
            console.error("Status check error:", error);
            statusResult.innerHTML = `<p style="color:#dc2626;">Backend connection failed. Please try again.</p>`;
        }
    });
}
