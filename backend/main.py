from fastapi import FastAPI
import sqlite3


app = FastAPI(
    title="API Health Monitor"
)


DATABASE = "health.db"


@app.get("/")
def home():
    return {
        "message": "API Health Monitor running"
    }


@app.get("/api/status")
def get_status():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, status, status_code, latency, checked_at
        FROM api_checks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()


    results = []

    for row in rows:
        results.append({
            "name": row[0],
            "status": row[1],
            "status_code": row[2],
            "latency": row[3],
            "checked_at": row[4]
        })


    return results