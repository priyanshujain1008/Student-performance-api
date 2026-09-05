# database.py
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ==========================================
# 1. CREATE DATABASE ENGINE
# ==========================================
# SQLite database file will be created as 'students.db'
engine = create_engine("sqlite:///students.db", echo=False)
Base = declarative_base()

# ==========================================
# 2. DEFINE TABLE SCHEMA (SQL Table Structure)
# ==========================================
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    grade = Column(String, nullable=True)  # We will calculate this in ETL
    inserted_at = Column(DateTime, default=datetime.utcnow)  # Timestamp

# ==========================================
# 3. CREATE ALL TABLES
# ==========================================
Base.metadata.create_all(engine)

# ==========================================
# 4. CREATE SESSION FACTORY
# ==========================================
SessionLocal = sessionmaker(bind=engine)
print("Database setup complete!")