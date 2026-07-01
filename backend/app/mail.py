import os
import smtplib
from email.message import EmailMessage


SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

LAST_EMAIL_ERROR = None


def get_last_email_error():
    return LAST_EMAIL_ERROR


def clean_value(value):
    if not value:
        return None
    return value.strip()


def clean_password(password):
    if not password:
        return None
    return password.replace(" ", "").strip()


def send_email(to_email: str, subject: str, body: str):
    global LAST_EMAIL_ERROR

    try:
        sender_email = clean_value(SMTP_EMAIL)
        sender_password = clean_password(SMTP_PASSWORD)
        receiver_email = clean_value(to_email)

        if not sender_email:
            LAST_EMAIL_ERROR = "SMTP_EMAIL environment variable not found"
            print("Email Error:", LAST_EMAIL_ERROR)
            return False

        if not sender_password:
            LAST_EMAIL_ERROR = "SMTP_PASSWORD environment variable not found"
            print("Email Error:", LAST_EMAIL_ERROR)
            return False

        if not receiver_email:
            LAST_EMAIL_ERROR = "Receiver email not found"
            print("Email Error:", LAST_EMAIL_ERROR)
            return False

        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        LAST_EMAIL_ERROR = None
        print("Email sent successfully to:", receiver_email)
        return True

    except Exception as e:
        LAST_EMAIL_ERROR = repr(e)
        print("Email sending failed:", repr(e))
        return False


def send_admin_new_request_email(request_data: dict):
    if not ADMIN_EMAIL:
        print("Email Error: ADMIN_EMAIL environment variable not found")
        return False

    subject = "New Student Request - Smart Campus Help Desk"

    body = f"""
Hello Admin,

A new student request has been submitted.

Request ID: {request_data.get("request_id", "-")}
Student Name: {request_data.get("student_name", "-")}
Enrollment: {request_data.get("enrollment", "-")}
Department: {request_data.get("department", "-")}
Phone: {request_data.get("phone", "-")}
Email: {request_data.get("email", "-")}
Request Type: {request_data.get("request_type", "-")}
Status: {request_data.get("status", "-")}
Submitted At: {request_data.get("created_at", "-")}

Problem Message:
{request_data.get("message", "-")}

Please login to the Admin Dashboard to solve, reject, or update this request.

Smart Campus Help Desk Portal
"""

    return send_email(ADMIN_EMAIL, subject, body)


def send_student_status_email(request_data: dict):
    student_email = request_data.get("email")

    if not student_email:
        print("Email Error: Student email not found")
        return False

    subject = "Request Status Updated - Smart Campus Help Desk"

    body = f"""
Hello {request_data.get("student_name", "Student")},

Your request status has been updated by the admin.

Request ID: {request_data.get("request_id", "-")}
Request Type: {request_data.get("request_type", "-")}
New Status: {request_data.get("status", "-")}

Your Problem:
{request_data.get("message", "-")}

Thank you,
Smart Campus Help Desk Portal
"""

    return send_email(student_email, subject, body)
