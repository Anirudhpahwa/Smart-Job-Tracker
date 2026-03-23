# Smart Job Tracker (Backend)

A production-style backend system for tracking job applications and generating analytics insights. Built using Django REST Framework with authentication, filtering, and asynchronous background processing.

---

## Overview

Smart Job Tracker allows users to:

* Track job applications
* Update application status (applied, interview, rejected, offer)
* Filter and search applications
* View analytics such as response rate and interview conversion

This project focuses on building a scalable backend system rather than a user interface.

---

## Tech Stack

* Backend: Django, Django REST Framework
* Database: SQLite (development), PostgreSQL (production-ready)
* Authentication: JWT (SimpleJWT)
* Async Processing: Celery
* Cache / Broker: Redis
* Containerization: Docker

---

## Features

### Authentication

* User registration and login
* JWT-based authentication
* Protected API routes

---

### Job Management APIs

* Create, update, and delete job applications
* Retrieve user-specific job data
* Pagination support

---

### Filtering and Search

* Filter by status
* Search by company name or role
* Filter by applied date range
* Sorting support

---

### Analytics Engine

* Total applications
* Response rate
* Interview conversion rate
* Average response time

---

### Background Processing

* Analytics computed asynchronously using Celery
* Scheduled jobs for periodic updates

---

## Project Structure

```
backend/
│
├── users/         # Authentication and user management
├── jobs/          # Job application APIs
├── analytics/     # Analytics engine and background tasks
├── core/          # Main project configuration
│
├── manage.py
└── requirements.txt
```

---

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/yourusername/smart-job-tracker.git
cd smart-job-tracker/backend
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   (macOS/Linux)
venv\Scripts\activate      (Windows)
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run Migrations

```
python manage.py migrate
```

---

### 5. Start Server

```
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## API Endpoints

### Authentication

* POST /api/v1/auth/register/
* POST /api/v1/auth/login/

---

### Jobs

* GET /api/v1/jobs/
* POST /api/v1/jobs/
* PATCH /api/v1/jobs/{id}/
* DELETE /api/v1/jobs/{id}/

---

### Analytics

* GET /api/v1/analytics/

---

## Example Workflow

1. Register user
2. Login to get JWT token
3. Create job application
4. Fetch jobs
5. View analytics

---

## Example Analytics Output

```
{
  "total_applications": 5,
  "total_responses": 2,
  "response_rate": 0.4,
  "interview_conversion_rate": 0.2
}
```

---

## What This Project Demonstrates

* REST API design
* Authentication and authorization
* Database modeling and relationships
* Query optimization
* Data aggregation and analytics
* Asynchronous background processing

---

## Future Improvements

* Add frontend dashboard (React)
* Deploy to cloud platforms (Render, AWS)
* Add notifications (email or SMS)
* Improve analytics visualization

---

## Author

Your Name

---

## License

This project is for educational purposes.