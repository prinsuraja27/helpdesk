import os
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not found")

    return psycopg2.connect(DATABASE_URL)


def load_requests():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
            rows = cur.fetchall()

    # Existing main.py dict format expect karta hai
    return {row["request_id"]: dict(row) for row in rows}


def save_requests(data):
    # JSON version me ye full data save karta tha.
    # Database version me hum upsert karenge.
    with get_connection() as conn:
        with conn.cursor() as cur:
            for request_id, req in data.items():
                cur.execute(
                    """
                    insert into requests (
                        request_id,
                        student_name,
                        enrollment,
                        department,
                        phone,
                        email,
                        request_type,
                        message,
                        status,
                        created_at
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    on conflict (request_id)
                    do update set
                        student_name = excluded.student_name,
                        enrollment = excluded.enrollment,
                        department = excluded.department,
                        phone = excluded.phone,
                        email = excluded.email,
                        request_type = excluded.request_type,
                        message = excluded.message,
                        status = excluded.status,
                        created_at = excluded.created_at
                    """,
                    (
                        req.get("request_id"),
                        req.get("student_name"),
                        req.get("enrollment"),
                        req.get("department"),
                        req.get("phone"),
                        req.get("email"),
                        req.get("request_type"),
                        req.get("message"),
                        req.get("status", "pending"),
                        req.get("created_at"),
                    ),
                )
        conn.commit()
        
