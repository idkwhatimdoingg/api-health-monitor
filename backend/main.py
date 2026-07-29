from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler

from database import create_database
from monitor import run_monitor


app = FastAPI(
    title="API Health Monitor"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE = "health.db"

scheduler = BackgroundScheduler()



# -----------------------------
# Startup / Shutdown
# -----------------------------

@app.on_event("startup")
def startup_event():

    create_database()

    # Run first check immediately
    run_monitor()


    scheduler.add_job(
        run_monitor,
        "interval",
        seconds=60
    )


    scheduler.start()



@app.on_event("shutdown")
def shutdown_event():

    scheduler.shutdown()



# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "API Health Monitor running"
    }



# -----------------------------
# Manual Monitor Trigger
# -----------------------------

@app.post("/api/monitor/run")
def manual_monitor():

    run_monitor()

    return {
        "message": "Health checks completed"
    }



# -----------------------------
# Latest API Status
# -----------------------------

@app.get("/api/status")
def get_status():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            api_endpoints.id,
            api_checks.name,
            api_checks.status,
            api_checks.status_code,
            api_checks.latency,
            api_checks.checked_at

        FROM api_checks

        LEFT JOIN api_endpoints

        ON api_checks.name = api_endpoints.name

        WHERE api_checks.id IN (

            SELECT MAX(id)

            FROM api_checks

            GROUP BY name

        )

        ORDER BY api_checks.id DESC
    """)


    rows = cursor.fetchall()


    connection.close()


    return [

        {
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "status_code": row[3],
            "latency": row[4],
            "checked_at": row[5]
        }

        for row in rows

    ]



# -----------------------------
# API History
# -----------------------------

@app.get("/api/history/{api_name}")
def get_history(api_name: str):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT checked_at, latency, status

        FROM api_checks

        WHERE name = ?

        ORDER BY id ASC

    """,
    (api_name,))


    rows = cursor.fetchall()


    connection.close()


    return [

        {
            "time": row[0],
            "latency": row[1],
            "status": row[2]
        }

        for row in rows

    ]



# -----------------------------
# Uptime
# -----------------------------

@app.get("/api/uptime/{api_name}")
def get_uptime(api_name: str):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT status

        FROM api_checks

        WHERE name = ?

    """,
    (api_name,))


    rows = cursor.fetchall()


    connection.close()


    total_checks = len(rows)


    if total_checks == 0:

        return {

            "name": api_name,
            "uptime": "No data",
            "total_checks": 0

        }



    successful_checks = 0


    for row in rows:

        if "Operational" in row[0]:

            successful_checks += 1



    uptime_percentage = round(
        (successful_checks / total_checks) * 100,
        2
    )


    return {

        "name": api_name,
        "uptime": f"{uptime_percentage}%",
        "total_checks": total_checks,
        "successful_checks": successful_checks

    }



# -----------------------------
# API Management
# -----------------------------

class APIEndpoint(BaseModel):

    name: str
    url: str



@app.get("/api/endpoints")
def get_endpoints():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT id, name, url

        FROM api_endpoints

    """)


    rows = cursor.fetchall()


    connection.close()


    return [

        {
            "id": row[0],
            "name": row[1],
            "url": row[2]
        }

        for row in rows

    ]



@app.post("/api/endpoints")
def add_endpoint(api: APIEndpoint):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO api_endpoints
        (
            name,
            url
        )

        VALUES (?, ?)

    """,
    (
        api.name,
        api.url
    ))


    connection.commit()

    connection.close()


    # Immediately check new API
    run_monitor()


    return {

        "message": "API added successfully"

    }



@app.delete("/api/endpoints/{api_id}")
def delete_endpoint(api_id: int):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT name

        FROM api_endpoints

        WHERE id = ?

    """,
    (api_id,))


    result = cursor.fetchone()


    if not result:

        connection.close()

        return {

            "message": "API not found"

        }



    api_name = result[0]


    cursor.execute("""
        DELETE FROM api_endpoints

        WHERE id = ?

    """,
    (api_id,))


    cursor.execute("""
        DELETE FROM api_checks

        WHERE name = ?

    """,
    (api_name,))


    connection.commit()

    connection.close()


    return {

        "message": "API deleted successfully"

    }