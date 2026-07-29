import requests
import time
import sqlite3

from datetime import datetime

from database import create_database, save_check


DATABASE = "health.db"



def get_apis():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT name, url
        FROM api_endpoints
    """)


    rows = cursor.fetchall()


    connection.close()


    return [
        {
            "name": row[0],
            "url": row[1]
        }

        for row in rows
    ]




def check_api(api):

    name = api["name"]

    url = api["url"]


    print(f"\nChecking {name}...")


    try:

        start_time = time.time()


        response = requests.get(
            url,
            timeout=5
        )


        end_time = time.time()


        latency = round(
            (end_time - start_time) * 1000
        )


        status_code = response.status_code



        if status_code < 300:

            status = "Operational ✅"


        elif status_code < 500:

            status = "Reachable but issue ⚠"


        else:

            status = "Server error ❌"



        return {

            "name": name,

            "status": status,

            "status_code": status_code,

            "latency": latency,

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }



    except requests.exceptions.Timeout:


        return {

            "name": name,

            "status": "Slow response ⚠",

            "status_code": "Timeout",

            "latency": ">5000ms",

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }



    except requests.exceptions.RequestException:


        return {

            "name": name,

            "status": "Down ❌",

            "status_code": "No response",

            "latency": "N/A",

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }




def run_monitor():

    print("==========================")

    print("Running API health check")

    print("==========================")


    apis = get_apis()


    if not apis:

        print("No APIs found in database.")

        return



    for api in apis:


        result = check_api(api)


        # Save result into SQLite

        save_check(result)



        print("\n----------------")

        print(result["name"])

        print("Status:", result["status"])

        print("HTTP:", result["status_code"])

        print("Latency:", result["latency"], "ms")

        print("Checked:", result["time"])




def main():

    create_database()

    run_monitor()




if __name__ == "__main__":

    main()