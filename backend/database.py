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


    # Check if APIs already exist
    cursor.execute("""
        SELECT COUNT(*)
        FROM api_endpoints
    """)


    count = cursor.fetchone()[0]


    # Add default APIs only on first setup
    if count == 0:

        default_apis = [

            (
                "Google API",
                "https://www.google.com"
            ),

            (
                "Discord API",
                "https://discord.com/api/v10"
            ),

            (
                "JSONPlaceholder API",
                "https://jsonplaceholder.typicode.com/posts"
            ),

            (
                "NPM Registry API",
                "https://registry.npmjs.org/"
            )

        ]


        cursor.executemany("""
            INSERT INTO api_endpoints
            (
                name,
                url
            )

            VALUES (?, ?)

        """, default_apis)


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