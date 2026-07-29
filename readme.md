# API Health Monitor

A full-stack API monitoring dashboard built with **FastAPI**, **SQLite**, and **JavaScript**.

API Health Monitor continuously checks API availability, tracks response times, calculates uptime, and provides a simple dashboard for monitoring API health.

The project was built to demonstrate practical backend development, REST API design, database management, frontend-backend communication, and monitoring concepts.

---

## Screenshot

*Add a screenshot of your dashboard here*

Example:

```
[ Dashboard Screenshot ]
```

---

# Features

## API Monitoring

* Automatically checks API availability
* Tracks HTTP response codes
* Measures API response latency
* Records health check timestamps
* Runs scheduled monitoring checks

---

## Dashboard

The frontend dashboard displays:

* API name
* API ID
* Current status
* HTTP response code
* Response latency
* Uptime percentage
* Last successful check time

---

## API Management

Users can:

* Add custom APIs to monitor
* Remove existing APIs
* View all monitored endpoints

Example APIs:

* Google
* Discord
* GitHub
* JSONPlaceholder
* Custom user-defined APIs

---

## Uptime Tracking

The application stores historical health checks and calculates uptime based on successful responses.

Example:

```
API: GitHub API

Total Checks: 500

Successful Checks: 498

Uptime: 99.6%
```

---

## Backend API Documentation

The backend uses FastAPI's automatic Swagger documentation.

After starting the backend, documentation is available at:

```
http://127.0.0.1:8000/docs
```

Swagger UI allows developers to:

* View available endpoints
* Test API requests
* Inspect responses
* Debug backend functionality

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLite
* APScheduler
* Requests
* Pydantic

## Frontend

* HTML
* CSS
* JavaScript
* Fetch API

---

# Project Structure

```
api-health-monitor/

│
├── backend/
│
│   ├── main.py
│   │   └── FastAPI routes and application logic
│   │
│   ├── database.py
│   │   └── SQLite database setup and storage
│   │
│   ├── monitor.py
│   │   └── API health check logic
│   │
│   ├── health.db
│   │   └── Stored monitoring data
│
│
├── frontend/
│
│   ├── index.html
│   │   └── Dashboard layout
│   │
│   ├── style.css
│   │   └── User interface styling
│   │
│   └── app.js
│       └── Frontend API communication
│
│
└── requirements.txt
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/api-health-monitor.git

cd api-health-monitor
```

---

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Start Backend

Navigate to the backend folder:

```bash
cd backend
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

The backend will start at:

```
http://127.0.0.1:8000
```

---

## Open API Documentation

Visit:

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

Open:

```
frontend/index.html
```

in your browser.

The frontend communicates with the FastAPI backend.

---

# API Endpoints

## Health Check

```
GET /
```

Returns application status.

Example:

```json
{
    "message": "API Health Monitor running"
}
```

---

## Get Current API Status

```
GET /api/status
```

Returns the latest health check results.

Example:

```json
[
    {
        "name": "Google API",
        "status": "Operational",
        "status_code": 200,
        "latency": 85,
        "checked_at": "2026-07-30 03:30:00"
    }
]
```

---

## Add API Endpoint

```
POST /api/endpoints
```

Example request:

```json
{
    "name": "GitHub API",
    "url": "https://api.github.com"
}
```

---

## List Monitored APIs

```
GET /api/endpoints
```

Returns all configured APIs.

---

## Delete API Endpoint

```
DELETE /api/endpoints/{id}
```

Removes an API from monitoring.

---

## API History

```
GET /api/history/{api_name}
```

Returns historical health checks.

---

## Uptime Calculation

```
GET /api/uptime/{api_name}
```

Returns uptime statistics.

---

# Database Design

The application uses SQLite with two main tables.

## api_endpoints

Stores monitored APIs.

| Column | Description           |
| ------ | --------------------- |
| id     | Unique API identifier |
| name   | API display name      |
| url    | API endpoint URL      |

---

## api_checks

Stores monitoring results.

| Column      | Description        |
| ----------- | ------------------ |
| id          | Check ID           |
| name        | API name           |
| status      | Health status      |
| status_code | HTTP response code |
| latency     | Response time      |
| checked_at  | Check timestamp    |

---

# Example Monitoring Flow

```
User adds API
        |
        ↓
API stored in SQLite
        |
        ↓
Background scheduler runs health check
        |
        ↓
HTTP request sent
        |
        ↓
Response saved
        |
        ↓
Dashboard updates
```

---

# Future Improvements

Possible improvements:

* Email/Slack downtime notifications
* User authentication
* API response history charts
* Docker deployment
* Cloud hosting
* Automated testing
* CI/CD pipeline
* More detailed monitoring metrics

---

# What This Project Demonstrates

This project demonstrates experience with:

* REST API development
* FastAPI backend development
* Database design
* HTTP communication
* API troubleshooting
* Frontend-backend integration
* Background task scheduling
* Monitoring system concepts
* Developer documentation

---

# License

This project is open-source and available for educational and portfolio purposes.
