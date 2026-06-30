import os
import smtplib
from email.message import EmailMessage


SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def send_email(to_email: str, subject: str, body: str):
    try:
        if not SMTP_EMAIL or not SMTP_PASSWORD:
            print("SMTP email/password not configured")
            return False

        msg = EmailMessage()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False


def send_admin_new_request_email(request_data: dict):
    if not ADMIN_EMAIL:
        print("Admin email not configured")
        return False

    subject = "New Student Request - Smart Campus Help Desk"

    body = f"""
Hello Admin,

A new student request has been submitted.

Request ID: {request_data["request_id"]}
Student Name: {request_data["student_name"]}
Enrollment: {request_data["enrollment"]}
Department: {request_data["department"]}
Phone: {request_data["phone"]}
Email: {request_data["email"]}
Request Type: {request_data["request_type"]}
Status: {request_data["status"]}
Submitted At: {request_data["created_at"]}

Problem Message:
{request_data["message"]}

Please login to the Admin Dashboard to solve, reject, or update this request.

Smart Campus Help Desk Portal
"""

    return send_email(ADMIN_EMAIL, subject, body)


def send_student_status_email(request_data: dict):
    subject = "Request Status Updated - Smart Campus Help Desk"

    body = f"""
Hello {request_data["student_name"]},

Your request status has been updated by the admin.

Request ID: {request_data["request_id"]}
Request Type: {request_data["request_type"]}
New Status: {request_data["status"]}

Your Problem:
{request_data["message"]}

Thank you,
Smart Campus Help Desk Portal
"""

    return send_email(request_data["email"], subject, body)