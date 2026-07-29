import sqlite3


DATABASE = "health.db"


APIS = [

    {
        "name": "GitHub API",
        "url": "https://api.github.com"
    },

    {
        "name": "OpenAI API",
        "url": "https://api.openai.com"
    },

    {
        "name": "Stripe API",
        "url": "https://api.stripe.com"
    }

]



connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()



for api in APIS:

    cursor.execute(
        """
        INSERT INTO api_endpoints (name, url)
        VALUES (?, ?)
        """,
        (
            api["name"],
            api["url"]
        )
    )



connection.commit()

connection.close()


print("Default APIs added!")