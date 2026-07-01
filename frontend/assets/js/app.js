const API_BASE = "https://helpdesk-f8n9.onrender.com";

const requestForm = document.getElementById("requestForm");
const formMessage = document.getElementById("formMessage");

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
                formMessage.style.color = "red";
                formMessage.textContent = data.detail || "Request submit failed";
                return;
            }

            formMessage.style.color = "green";
            formMessage.textContent = "Request submitted successfully";

            // Form only success ke baad clear hoga
            requestForm.reset();

        } catch (error) {
            console.error("Submit error:", error);
            formMessage.style.color = "red";
            formMessage.textContent = "Backend connection failed. Please try again.";

            // Error me form clear nahi hoga
            return;
        }
    });
}
