import os
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import RequestStatusUpdate, StudentRequest
from .security import verify_admin_key
from .storage import load_requests, save_requests
from app.mail import (
    send_email,
    send_admin_new_request_email,
    send_student_status_email,
)


app = FastAPI(
    title="Smart Campus Help Desk API",
    description="Secure FastAPI backend for student help desk requests.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Smart Campus Help Desk API is running successfully"}


@app.post("/requests", status_code=status.HTTP_201_CREATED)
def create_request(student_request: StudentRequest):
    requests = load_requests()

    if student_request.request_id in requests:
        raise HTTPException(status_code=400, detail="Request ID already exists")

    request_data = student_request.model_dump()
    request_data["status"] = "pending"
    request_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    requests[student_request.request_id] = request_data
    save_requests(requests)

    # Admin ko email bhejna.
    # Email fail ho to bhi request save rahegi, backend crash nahi hoga.
    try:
        send_admin_new_request_email(request_data)
    except Exception as e:
        print("Admin email failed:", repr(e))

    return {
        "message": "Request submitted successfully",
        "request": request_data,
    }


@app.get("/requests", dependencies=[Depends(verify_admin_key)])
def get_all_requests():
    requests = load_requests()
    return list(requests.values())


@app.get("/requests/{request_id}")
def get_request(request_id: str):
    requests = load_requests()

    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")

    return requests[request_id]


@app.put("/requests/{request_id}/status", dependencies=[Depends(verify_admin_key)])
def update_request_status(request_id: str, status_update: RequestStatusUpdate):
    requests = load_requests()

    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")

    requests[request_id]["status"] = status_update.status
    save_requests(requests)

    # Student ko status update email bhejna.
    # Email fail ho to bhi status update successful rahega.
    try:
        send_student_status_email(requests[request_id])
    except Exception as e:
        print("Student email failed:", repr(e))

    return {
        "message": "Request status updated successfully",
        "request": requests[request_id],
    }


@app.delete("/requests/{request_id}", dependencies=[Depends(verify_admin_key)])
def delete_request(request_id: str):
    requests = load_requests()

    if request_id not in requests:
        raise HTTPException(status_code=404, detail="Request not found")

    deleted_request = requests.pop(request_id)
    save_requests(requests)

    return {
        "message": "Request deleted successfully",
        "request": deleted_request,
    }


@app.get("/dashboard", dependencies=[Depends(verify_admin_key)])
def get_dashboard():
    requests = load_requests()
    values = list(requests.values())

    return {
        "total_requests": len(values),
        "pending_requests": sum(1 for req in values if req.get("status") == "pending"),
        "progress_requests": sum(1 for req in values if req.get("status") == "progress"),
        "solved_requests": sum(1 for req in values if req.get("status") == "solved"),
        "rejected_requests": sum(1 for req in values if req.get("status") == "rejected"),
    }


@app.get("/test-email")
def test_email():
    admin_email = os.getenv("ADMIN_EMAIL")

    if not admin_email:
        return {
            "success": False,
            "message": "ADMIN_EMAIL environment variable not found",
        }

    result = send_email(
        admin_email,
        "Test Email - Smart Campus Help Desk",
        "Hello Admin,\n\nThis is a test email from Smart Campus Help Desk backend."
    )

    if result.get("ok"):
        return {
            "success": True,
            "message": "Test email sent successfully",
        }

    return {
        "success": False,
        "message": "Email sending failed",
        "error": result.get("error")
    }
