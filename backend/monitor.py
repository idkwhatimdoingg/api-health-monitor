import requests
import time
from datetime import datetime
from database import create_database, save_check


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
    },
    {
        "name": "Broken Test API",
        "url": "https://this-does-not-exist-12345.com"
    }
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

        latency = round((end_time - start_time) * 1000)

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
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


    except requests.exceptions.Timeout:

        return {
            "name": name,
            "status": "Slow response ⚠",
            "status_code": "Timeout",
            "latency": ">5000ms",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


    except requests.exceptions.RequestException:

        return {
            "name": name,
            "status": "Down ❌",
            "status_code": "No response",
            "latency": "N/A",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }



def main():

    # Create SQLite database if it does not exist
    create_database()


    print("==========================")
    print(" API Health Monitor ")
    print("==========================")


    for api in APIS:

        result = check_api(api)

        # Save result into SQLite
        save_check(result)


        print("\n----------------")
        print(result["name"])
        print("Status:", result["status"])
        print("HTTP:", result["status_code"])
        print("Latency:", result["latency"], "ms")
        print("Checked:", result["time"])



if __name__ == "__main__":
    main()