import os
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not found")

    return psycopg2.connect(DATABASE_URL)


def create_table_if_not_exists():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS requests (
                    request_id TEXT PRIMARY KEY,
                    student_name TEXT NOT NULL,
                    enrollment TEXT NOT NULL,
                    department TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    request_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT NOT NULL
                );
                """
            )
        conn.commit()


def load_requests():
    create_table_if_not_exists()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
            rows = cur.fetchall()

    return {row["request_id"]: dict(row) for row in rows}


def save_requests(data):
    create_table_if_not_exists()

    with get_connection() as conn:
        with conn.cursor() as cur:
            for request_id, req in data.items():
                cur.execute(
                    """
                    INSERT INTO requests (
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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (request_id)
                    DO UPDATE SET
                        student_name = EXCLUDED.student_name,
                        enrollment = EXCLUDED.enrollment,
                        department = EXCLUDED.department,
                        phone = EXCLUDED.phone,
                        email = EXCLUDED.email,
                        request_type = EXCLUDED.request_type,
                        message = EXCLUDED.message,
                        status = EXCLUDED.status,
                        created_at = EXCLUDED.created_at
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


def delete_request_from_db(request_id):
    create_table_if_not_exists()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM requests WHERE request_id = %s", (request_id,))
        conn.commit()
