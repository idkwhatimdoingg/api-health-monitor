from fastapi import FastAPI
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler

from database import create_database
from monitor import run_monitor


app = FastAPI(
    title="API Health Monitor"
)


DATABASE = "health.db"


scheduler = BackgroundScheduler()


@app.on_event("startup")
def startup_event():

    create_database()

    # Run immediately when server starts
    run_monitor()

    # Then repeat every 60 seconds
    scheduler.add_job(
        run_monitor,
        "interval",
        seconds=60
    )

    scheduler.start()



@app.on_event("shutdown")
def shutdown_event():

    scheduler.shutdown()



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