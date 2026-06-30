# Smart Campus Help Desk Portal - Project Report

## 1. Introduction

Smart Campus Help Desk Portal is a full-stack web application designed for college students and administrators. In a college environment, students often face issues related to ID cards, certificates, fees, websites, and other academic or administrative services. This portal provides a simple digital system where students can submit their requests and check their request status.

The admin can log in using a secure admin key and manage all student requests from a professional dashboard. The admin can view student details, update request status, and delete requests when required.

## 2. Objective

The main objective of this project is to create a centralized help desk portal for college-related student problems.

The project aims to:

- Provide an easy request submission system for students
- Allow students to check request status using Request ID
- Help admins view and manage all student requests
- Store request data using JSON file storage
- Use a secure admin key system for admin-only APIs
- Build a clean and responsive frontend interface
- Create a beginner-friendly full-stack internship project

## 3. Technologies Used

### Frontend Technologies

- HTML: Used to create the structure of web pages
- CSS: Used for styling, layout, responsiveness, cards, buttons, and professional design
- JavaScript: Used to connect frontend forms with backend APIs

### Backend Technologies

- Python: Main programming language for backend development
- FastAPI: Used to create REST API endpoints
- Pydantic: Used for data validation
- JSON File Storage: Used to store student requests

### Deployment Technologies

- GitHub: Used for source code hosting
- Render.com: Used for backend and frontend deployment

## 4. Features

### Student Features

- Student can submit a request with full details
- Student can select request type
- Student can enter problem message
- Student can check request status using Request ID
- Student receives success and error messages

### Admin Features

- Admin login using admin key
- Admin dashboard summary cards
- Admin can view all requests
- Admin can view complete student details
- Admin can update request status
- Admin can delete requests
- Admin can manage request records from a clean table

### Backend Features

- REST API using FastAPI
- Pydantic validation for request data
- JSON storage using `json.load()` and `json.dump()`
- Admin key security using request header
- Error handling for duplicate Request ID
- Error handling for request not found
- CORS enabled for frontend connection

## 5. System Flow

### Student Request Flow

1. Student opens the main portal page.
2. Student fills the request form.
3. JavaScript sends a POST request to the backend.
4. Backend validates the data using Pydantic.
5. Backend checks if Request ID already exists.
6. Backend adds default status as `pending`.
7. Backend adds current date and time.
8. Backend saves the request in `requests.json`.
9. Student receives a success message.

### Status Checking Flow

1. Student enters Request ID in the status check section.
2. JavaScript sends a GET request to the backend.
3. Backend searches the request in JSON storage.
4. If request exists, backend returns request details.
5. Frontend displays current status.
6. If request does not exist, backend returns 404 error.

### Admin Flow

1. Admin opens `admin.html`.
2. Admin enters admin key.
3. After login, frontend fetches dashboard data.
4. Frontend fetches all student requests using admin key header.
5. Admin can view details, update status, or delete request.
6. Backend verifies admin key before allowing admin-only actions.

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns API running message |
| POST | `/requests` | Adds a new student request |
| GET | `/requests` | Returns all student requests |
| GET | `/requests/{request_id}` | Returns single request details |
| PUT | `/requests/{request_id}/status` | Updates request status |
| DELETE | `/requests/{request_id}` | Deletes a request |
| GET | `/dashboard` | Returns dashboard summary count |

## 7. Security

The project uses a simple admin key system. Admin-only APIs require the following header:

```text
x-admin-key: campus-admin-123
```

If the admin key is missing or wrong, the backend returns `401 Unauthorized`.

Admin-only APIs are:

- GET `/requests`
- PUT `/requests/{request_id}/status`
- DELETE `/requests/{request_id}`
- GET `/dashboard`

## 8. Data Storage

All student requests are stored in:

```text
backend/data/requests.json
```

Initial content:

```json
{}
```

When a student submits a request, the backend stores the request using Request ID as the key.

Example request data:

```json
{
    "request_id": "1",
    "student_name": "Prince",
    "enrollment": "123456",
    "department": "CSE",
    "phone": "9999999999",
    "request_type": "ID Card Problem",
    "message": "My ID card is not issued yet.",
    "status": "pending",
    "created_at": "2026-06-30 10:30:00"
}
```

## 9. Future Scope

This project can be improved in the future by adding:

- Database support such as SQLite, MySQL, or PostgreSQL
- Admin username and password authentication
- Email or SMS notification system
- Student login system
- File upload for proof or documents
- Search and filter options in admin dashboard
- Department-wise admin access
- Request priority system
- Deployment with environment variables

## 10. Conclusion

Smart Campus Help Desk Portal is a clean and useful full-stack internship project. It solves a real college problem by providing a digital platform for student support requests. The project includes a professional frontend, secure FastAPI backend, JSON storage, admin dashboard, and proper API structure.

This project is beginner-friendly, practical, and suitable for college submission, internship portfolio, and full-stack development learning.
