# Student Management System

🎓 **Student Management System**

## 📌 Description

A full-stack backend system built using FastAPI to manage university students with secure authentication, role-based access control, caching, monitoring, and a real-time dashboard.

This project demonstrates:

* Secure JWT Authentication
* RESTful API Design
* Database Management with SQLAlchemy
* Redis Caching for performance optimization
* Monitoring & Logging Dashboard
* Dockerized deployment

---

# 👨‍💻 Team Responsibilities

## 1️⃣ JWT Authentication

Responsible for:

* User registration & login
* JWT token generation and verification
* Securing API routes using authentication and authorization
* Role-based access control (Admin / Student)

---

## 2️⃣ Database

Responsible for:

* Designing database models using SQLAlchemy
* Database configuration and connection
* Managing relationships between Users and Students
* CRUD database operations

---

## 3️⃣ Validation & Clean Code

Responsible for:

* Creating Pydantic schemas for request/response validation
* Input validation and error handling
* Applying clean architecture principles
* Organizing project structure and reusable code

---

## 4️⃣ Logging & Monitoring

Responsible for:

* Implementing application logging
* Tracking system activities and errors
* Monitoring backend performance and metrics
* Creating monitoring/dashboard support

---

## 5️⃣ Redis Caching & API Testing

Responsible for:

* Integrating Redis caching
* Improving API performance and response speed
* Reducing repeated database queries
* Testing APIs using tools like Postman or Pytest

---

## 6️⃣ Frontend & Docker

Responsible for:

* Building the frontend user interface
* Connecting frontend with backend APIs
* Docker setup and container management
* Deployment preparation and project documentation

---

# 🚀 Features

## 🔐 Authentication

* User Registration & Login
* JWT Token-based Authentication
* Protected Endpoints

## 👥 Roles

* **Admin:** Full control over student records
* **Student:** Access own data only (logic implemented)

## 🎓 Student Management

* Full CRUD operations (Create, Read, Update, Delete)
* Filtering (department, GPA)
* Pagination
* Role-based access control

## ⚡ Caching (Redis)

* Cache `GET /students`
* Cache `GET /students/{id}`
* Cache invalidation on update/delete
* Performance improvement using cache vs DB benchmark

## 📊 Logging & Monitoring Dashboard

* Total API Requests
* Error Count
* Average Response Time
* Recent Errors
* Authentication Logs (login success/failure)
* Alert System

## 🧪 API Testing

* Unauthorized access tests
* Register & Login tests
* CRUD operations tests
* Edge cases:

  * Invalid GPA
  * Duplicate email
  * Invalid login
* All tests passing ✅

## 🖥️ Frontend

* Student Management UI (CRUD)
* Monitoring Dashboard with charts
* Real-time updates (auto refresh)

## 🐳 Docker Support

* Fully containerized application
* FastAPI + Redis services
* Easy setup using Docker Compose

---

# 🛠️ Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* Redis
* JWT (python-jose)
* Chart.js
* Docker & Docker Compose
* Pytest

---

# ⚙️ Setup Instructions

## 🔹 1. Clone Repository

```bash
git clone https://github.com/ModasserAshrafSabry/student-management-system-Backend-Development-with-FastAPI-
cd student-management-system
```

---

# 🐳 Run Using Docker (Recommended)

## 🔹 Build and Run Containers

```bash
docker-compose up --build
```

## 🔹 Access the Application

* Swagger API Docs:
  `http://127.0.0.1:8000/docs`

* Monitoring Dashboard:
  `frontend/dashboard.html`

---

# 💻 Run Locally (Without Docker)

## 🔹 Install Requirements

```bash
pip install -r requirements.txt
```

## 🔹 Run Server

```bash
uvicorn app.main:app --reload
```

---

# 🔐 Authentication Flow

1. Register user → `/register`
2. Login → `/login`
3. Copy access token
4. Click **Authorize** in Swagger
5. Use protected endpoints

---

# 📊 Monitoring Endpoint

## GET `/monitor`

Returns:

* Students count
* Users count
* Request count
* Error count
* Average response time
* Recent errors
* Authentication logs

---

# 🧪 Run Tests

```bash
pytest
```

### Expected Output

```bash
ALL TESTS PASSED ✅
```

---

# 📂 Project Structure

```bash
app/
├── models/
├── routes/
├── schemas/
├── utils/
├── main.py

frontend/
├── index.html
├── dashboard.html

tests/
├── test_students.py
```

---

➡️ Redis significantly improves performance

---

# 🏁 Final Status

| Feature              | Status |
| -------------------- | ------ |
| JWT Authentication   | ✅      |
| Database Integration | ✅      |
| Validation           | ✅      |
| Clean Code Structure | ✅      |
| Logging & Monitoring | ✅      |
| Redis Caching        | ✅      |
| API Testing          | ✅      |
| Frontend             | ✅      |
| Docker               | ✅      |

---

