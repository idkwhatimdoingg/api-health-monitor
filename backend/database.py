import sqlite3


DATABASE = "health.db"



def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    # Stores API monitoring history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_checks (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            status TEXT,

            status_code TEXT,

            latency INTEGER,

            checked_at TEXT

        )
    """)


    # Stores monitored APIs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_endpoints (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            url TEXT

        )
    """)


    connection.commit()

    connection.close()



def save_check(result):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO api_checks
        (
            name,
            status,
            status_code,
            latency,
            checked_at
        )

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