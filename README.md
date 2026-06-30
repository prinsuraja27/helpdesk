# Smart Campus Help Desk Portal

A complete full-stack internship project for a college help desk system. Students can submit campus-related requests, check request status, and the admin can securely manage all requests from a professional dashboard.

## Features

### Student Side
- Modern responsive landing page
- Student request submission form
- Request status checking by Request ID
- Clean success and error messages

### Admin Side
- Separate admin page
- Simple admin key login
- Dashboard summary cards
- Full request table with student details
- View complete request details in modal
- Update status to progress, solved, or rejected
- Delete requests

### Backend
- FastAPI REST API
- Pydantic validation
- JSON file storage
- Admin-only API protection using `x-admin-key`
- CORS enabled for frontend calls

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Pydantic
- JSON file storage

### Deployment
- GitHub
- Render.com

## Folder Structure

```text
smart-campus-helpdesk/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── storage.py
│   │   └── security.py
│   ├── data/
│   │   └── requests.json
│   ├── requirements.txt
│   └── run.bat
│
├── frontend/
│   ├── index.html
│   ├── admin.html
│   └── assets/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── app.js
│           └── admin.js
│
├── docs/
│   └── PROJECT_REPORT.md
│
├── README.md
└── RUN_PROJECT.txt
```

## How to Run Backend

Open terminal inside the `backend` folder.

```bash
python -m venv venv
```

Activate virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install requirements:

```bash
python -m pip install -r requirements.txt
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## How to Open Frontend

Open this file in your browser:

```text
frontend/index.html
```

For admin page, open:

```text
frontend/admin.html
```

## Admin Key

```text
campus-admin-123
```

Admin-only APIs require this header:

```text
x-admin-key: campus-admin-123
```

## API Endpoints

| Method | Endpoint | Description | Admin Key Required |
|---|---|---|---|
| GET | `/` | API running message | No |
| POST | `/requests` | Add new student request | No |
| GET | `/requests` | Get all requests | Yes |
| GET | `/requests/{request_id}` | Get single request details | No |
| PUT | `/requests/{request_id}/status` | Update request status | Yes |
| DELETE | `/requests/{request_id}` | Delete request | Yes |
| GET | `/dashboard` | Get dashboard counts | Yes |

## Render Deployment Steps

### Backend Render Web Service

Create a new Web Service on Render and connect your GitHub repository.

Use these settings:

```text
Root Directory: backend
Build Command: python -m pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, copy your backend Render URL.

### Frontend Render Static Site

Create a new Static Site on Render and connect the same GitHub repository.

Use these settings:

```text
Root Directory: frontend
Build Command: empty
Publish Directory: .
```

After deployment, replace this line in both frontend JavaScript files:

```javascript
const API_BASE = "http://127.0.0.1:8000";
```

with your deployed backend URL.

Example:

```javascript
const API_BASE = "https://your-backend-name.onrender.com";
```

## Notes

- Initial JSON storage content is `{}`.
- Request status is automatically set to `pending`.
- Submitted date and time are automatically added by the backend.
- This project is beginner-friendly, clean, and suitable for internship or college submission.
