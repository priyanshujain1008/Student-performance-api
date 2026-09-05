# etl_pipeline.py
import pandas as pd
from database import SessionLocal, Student
from data import raw_data
import json

# ==========================================
# STEP 1: EXTRACT (Read raw data)
# ==========================================
def extract_data():
    print("=" * 50)
    print("STEP 1: EXTRACT")
    print("=" * 50)
    
    # Convert raw JSON-like data to Pandas DataFrame
    df = pd.DataFrame(raw_data)
    print(f"Extracted {len(df)} raw records")
    print(f"Columns: {list(df.columns)}")
    return df

# ==========================================
# STEP 2: TRANSFORM (Clean and enrich the data)
# ==========================================
def transform_data(df):
    print("\n" + "=" * 50)
    print("STEP 2: TRANSFORM")
    print("=" * 50)
    
    # 1. Handle missing names
    df['name'] = df['name'].fillna("Unknown")
    df['name'] = df['name'].replace("", "Unknown")
    
    # 2. Handle missing marks (Replace with average marks)
    avg_marks = df['marks'].mean()
    df['marks'] = df['marks'].fillna(avg_marks)
    
    # 3. Convert marks to integers
    df['marks'] = df['marks'].astype(int)
    
    # 4. Calculate grades based on marks
    def calculate_grade(marks):
        if marks >= 90:
            return 'A'
        elif marks >= 80:
            return 'B'
        elif marks >= 70:
            return 'C'
        elif marks >= 60:
            return 'D'
        else:
            return 'F'
    
    df['grade'] = df['marks'].apply(calculate_grade)
    
    # 5. Remove duplicates (Same student, same subject)
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['name', 'subject'])
    after_dedup = len(df)
    
    print(f"Handled missing values: {df['name'].isna().sum()} missing names, {df['marks'].isna().sum()} missing marks")
    print(f"Added grade column based on marks")
    print(f"Removed {before_dedup - after_dedup} duplicate records")
    print(f"Transformed data now has {len(df)} clean records")
    
    return df

# ==========================================
# STEP 3: LOAD (Insert into SQL Database)
# ==========================================
def load_data(df):
    print("\n" + "=" * 50)
    print("STEP 3: LOAD")
    print("=" * 50)
    
    db = SessionLocal()
    
    # Clear existing data (Optional - for fresh load)
    db.query(Student).delete()
    db.commit()
    
    # Insert cleaned data into SQL
    records_loaded = 0
    for _, row in df.iterrows():
        student = Student(
            name=row['name'],
            subject=row['subject'],
            marks=row['marks'],
            grade=row['grade']
        )
        db.add(student)
        records_loaded += 1
    
    db.commit()
    db.close()
    
    print(f"Successfully loaded {records_loaded} records into SQL Database!")
    print(f"Table: 'students' | Database: 'students.db'")
    
    return records_loaded

# ==========================================
# MAIN ETL EXECUTION
# ==========================================
def run_etl():
    print("\n" + "=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)
    
    # Extract
    raw_df = extract_data()
    
    # Transform
    clean_df = transform_data(raw_df)
    
    # Load
    loaded_count = load_data(clean_df)
    
    print("\n" + "=" * 50)
    print(f"ETL COMPLETED SUCCESSFULLY! Loaded {loaded_count} rows.")
    print("=" * 50)
    
    return clean_df

# Run the ETL pipeline when this file is executed
if __name__ == "__main__":
    run_etl()