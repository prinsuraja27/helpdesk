const API_BASE = "http://127.0.0.1:8000";

const studentRequestForm = document.getElementById("studentRequestForm");
const formMessage = document.getElementById("formMessage");
const checkStatusBtn = document.getElementById("checkStatusBtn");
const statusRequestId = document.getElementById("statusRequestId");
const statusResult = document.getElementById("statusResult");

function setMessage(element, text, isSuccess = true) {
    element.textContent = text;
    element.style.color = isSuccess ? "#16a34a" : "#dc2626";
}

studentRequestForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        request_id: document.getElementById("request_id").value.trim(),
        student_name: document.getElementById("student_name").value.trim(),
        enrollment: document.getElementById("enrollment").value.trim(),
        department: document.getElementById("department").value.trim(),
        phone: document.getElementById("phone").value.trim(),
	email: document.getElementById("email").value,
        request_type: document.getElementById("request_type").value,
        message: document.getElementById("message").value.trim(),
    };

    try {
        const response = await fetch(`${API_BASE}/requests`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        setMessage(formMessage, "Request submitted successfully. Please save your Request ID.", true);
        studentRequestForm.reset();
    } catch (error) {
        setMessage(formMessage, error.message, false);
    }
});

checkStatusBtn.addEventListener("click", async () => {
    const requestId = statusRequestId.value.trim();

    if (!requestId) {
        statusResult.style.display = "block";
        statusResult.innerHTML = `<strong style="color:#dc2626;">Please enter Request ID.</strong>`;
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/requests/${encodeURIComponent(requestId)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request not found");
        }

        statusResult.style.display = "block";
        statusResult.innerHTML = `
            <h3>Request Status</h3>
            <p><strong>Request ID:</strong> ${data.request_id}</p>
            <p><strong>Student Name:</strong> ${data.student_name}</p>
            <p><strong>Request Type:</strong> ${data.request_type}</p>
            <p><strong>Status:</strong> <span class="status-pill status-${data.status}">${data.status}</span></p>
            <p><strong>Submitted:</strong> ${data.created_at}</p>
        `;
    } catch (error) {
        statusResult.style.display = "block";
        statusResult.innerHTML = `<strong style="color:#dc2626;">${error.message}</strong>`;
    }
});
