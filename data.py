# data.py
import json

# ==========================================
# RAW DATA (Intentionally messy to show ETL skills)
# ==========================================
raw_data = [
    {"name": "Aarav", "subject": "Maths", "marks": 85},
    {"name": "Priya", "subject": "Maths", "marks": 92},
    {"name": "Rahul", "subject": "Science", "marks": 78},
    {"name": "Aarav", "subject": "Science", "marks": 88},
    {"name": "Priya", "subject": "English", "marks": 95},
    {"name": "", "subject": "Maths", "marks": 65},           # Missing name
    {"name": "Rohan", "subject": "Hindi", "marks": None},     # Missing marks
    {"name": "Aisha", "subject": "Maths", "marks": 91},
    {"name": "Vikram", "subject": "Science", "marks": 82},
    {"name": "Neha", "subject": "English", "marks": 89},
    {"name": "Aisha", "subject": "Science", "marks": 76},
    {"name": "Rohan", "subject": "Maths", "marks": 70},
    {"name": "Vikram", "subject": "English", "marks": 93},
    {"name": "Neha", "subject": "Maths", "marks": 87},
    {"name": "Aarav", "subject": "English", "marks": 84},
]

# Convert to JSON string (for demonstration)
json_string = json.dumps(raw_data)
print(f"Raw data ready! Total records: {len(raw_data)}")