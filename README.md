# 🎓 Student Performance Analytics API

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy)
![SQLite](https://img.shields.io/badge/SQLite-3+-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas)

### 🚀 End-to-End Data Engineering Project

**ETL Pipeline • SQL Database • REST APIs • Data Analytics**

---

## 📌 Project Overview

**Student Performance Analytics API** is an end-to-end Data Engineering project built using **Python, FastAPI, Pandas, SQLAlchemy and SQLite**.

The project processes student performance data through a complete **ETL (Extract, Transform, Load) pipeline**. Raw student data is extracted, cleaned, transformed, validated, and then stored in a relational SQL database.

The processed data is exposed through **RESTful APIs**, allowing users to manage student records, perform analytics, and export data in CSV format.

---

## 🎯 Project Objectives

- Data extraction
- Data cleaning
- Data transformation
- Data validation
- SQL database storage
- REST API development
- Data aggregation
- Performance analytics
- CSV data export
- Backend and dashboard integration

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔄 ETL Pipeline | Extract, transform and load student performance data |
| 🗄️ SQL Database | Store student records using SQLite |
| 🚀 REST APIs | Backend APIs built using FastAPI |
| 📊 Performance Analytics | Analyze marks, grades and subject performance |
| ➕ Add Student | Add new student performance records |
| 📋 Student Records | Retrieve and display stored student data |
| 📥 CSV Export | Export student records into CSV format |
| ✅ Data Validation | Validate incoming data using Pydantic |
| 📖 API Documentation | Interactive Swagger/OpenAPI documentation |
| 🧮 SQL Aggregations | Calculate statistics using database queries |

---

## 🔄 ETL Pipeline Architecture

```
                 RAW STUDENT DATA
                        │
                        ▼
               ┌─────────────────┐
               │     EXTRACT     │
               │                 │
               │ Read CSV / Raw  │
               │ Student Data    │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │    TRANSFORM    │
               │                 │
               │ • Clean Data    │
               │ • Validate Data │
               │ • Handle Values │
               │ • Process Marks │
               │ • Calculate Grade│
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │      LOAD       │
               │                 │
               │ Store Processed │
               │ Data in SQLite  │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │     FastAPI     │
               │    REST APIs    │
               └────────┬────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │ Student APIs    │     │ Analytics APIs  │
    │                 │     │                 │
    │ Add Student     │     │ Average Marks   │
    │ Get Students    │     │ Grade Analysis  │
    │ Get Student     │     │ Subject Stats   │
    │ Delete Student  │     │ Performance     │
    └─────────────────┘     └─────────────────┘
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/home` | Frontend dashboard |
| GET | `/students` | Get all students |
| GET | `/students/{name}` | Get student by name |
| POST | `/students` | Add new student |
| GET | `/analytics/summary` | Overall statistics |
| GET | `/analytics/top-performers` | Top students |
| GET | `/analytics/subject-average` | Subject-wise average |
| GET | `/export-csv` | Export data as CSV |

---

## 📊 Sample API Response

```json
{
  "total_records": 14,
  "average_marks": 84.5,
  "maximum_marks": 95,
  "minimum_marks": 65,
  "grade_distribution": {
    "A": 5,
    "B": 6,
    "C": 2,
    "D": 1
  }
}
```

---

## 🏃 How to Run

### Prerequisites

- Python 3.9+
- Git

### Installation

```bash
git clone https://github.com/USERNAME/student-performance-api.git
cd student-performance-api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python etl_pipeline.py
uvicorn main:app --reload
```

### Access

- **Dashboard:** http://127.0.0.1:8000/home
- **API Docs:** http://127.0.0.1:8000/docs


## 📁 Project Structure

```
student-performance-api/
│
├── .gitignore
├── requirements.txt
├── data.py
├── database.py
├── etl_pipeline.py
├── main.py
├── static/
│   └── index.html
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License.
