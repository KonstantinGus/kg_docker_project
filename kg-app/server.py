from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
import psycopg


def connect_to_database():
    while True:
        try:
            return psycopg.connect(
                host=os.environ["DB_HOST"],
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"]
            )
        except psycopg.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)


def setup_database():
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    message TEXT NOT NULL
                )
            """)


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return

        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, message FROM messages ORDER BY id"
                )
                rows = cursor.fetchall()

        self.send_json({
            "messages": [
                {"id": row[0], "message": row[1]}
                for row in rows
            ]
        })

    def do_POST(self):
        if self.path != "/":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            message = data.get("message", "").strip()

            if not message:
                self.send_json({"error": "Note cannot be empty"}, 400)
                return

            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO messages (message) VALUES (%s) RETURNING id",
                        (message,)
                    )
                    note_id = cursor.fetchone()[0]

            self.send_json({
                "id": note_id,
                "message": message
            }, 201)

        except (json.JSONDecodeError, ValueError):
            self.send_json({"error": "Invalid request"}, 400)


setup_database()

server = HTTPServer(("0.0.0.0", 5000), RequestHandler)
print("Python server running on port 5000", flush=True)
server.serve_forever()