import sqlite3


DATABASE_NAME = "health.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            status_code TEXT,
            latency INTEGER,
            checked_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()



def save_check(result):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO api_checks
        (name, status, status_code, latency, checked_at)

        VALUES (?, ?, ?, ?, ?)
    """,
    (
        result["name"],
        result["status"],
        result["status_code"],
        result["latency"],
        result["time"]
    ))

    connection.commit()
    connection.close()