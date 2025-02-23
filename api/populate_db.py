# import pandas as pd
# import numpy as np
#
# prescriptions = pd.read_csv('prescriptions.csv')
# visits = pd.read_csv('visits.csv')
# patients = pd.read_csv('patients.csv')
#
# def populate_db(conn):
#     cursor = conn.cursor()
#
#     create_table = '''
#         CREATE TABLE Patients (
#             PID INT PRIMARY KEY,
#             DOB DATE,
#             P_Name VARCHAR(50),
#             SSN CHAR(64),
#             Address VARCHAR(50),
#             Zipcode VARCHAR(5),
#             State_Abv VARCHAR(2),
#             phone_num VARCHAR(20)
#     );
#     '''
#
#     cursor.execute(create_table)
#
#     for index, row in patients.iterrows():
#         cursor.execute("""
#             INSERT INTO Patients 
#                 (PID, DOB, P_Name, SSN, Address, Zipcode, State_Abv, phone_num)
#             VALUES 
#                 (%s, %s, %s, %s, %s, %s, %s, %s)
#         """, (
#             row['pid'],
#             row['dob'],
#             row['name'],
#             str(row['ssn']),       
#             row['address'],
#             str(row['zip']),      
#             row['state'],
#             str(row['phone'])    
#         ))
#     conn.commit()
#
import pandas as pd
import psycopg2
from psycopg2 import errors

# def populate_db(conn):
#     cursor = conn.cursor()
#
#     # Create table with proper data types and error handling
#     try:
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS Patients (
#                 PID BIGINT PRIMARY KEY,
#                 DOB DATE,
#                 P_Name VARCHAR(255),
#                 SSN VARCHAR(64),
#                 Address VARCHAR(255),
#                 Zipcode VARCHAR(10),
#                 State_Abv CHAR(2),
#                 phone_num VARCHAR(20)
#             );
#         ''')
#         conn.commit()
#     except Exception as e:
#         print(f"Error creating table: {e}")
#         conn.rollback()
#         return
#
#     # Load data
#     patients = pd.read_csv('patients.csv')
#
#     # Insert data with error handling
#     try:
#         for index, row in patients.iterrows():
#             cursor.execute("""
#                 INSERT INTO Patients 
#                     (PID, DOB, P_Name, SSN, Address, Zipcode, State_Abv, phone_num)
#                 VALUES 
#                     (%s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 row['pid'],
#                 pd.to_datetime(row['dob']).strftime('%Y-%m-%d'),  # Ensure date format
#                 row['name'],
#                 str(row['ssn']).strip(),  # Remove whitespace
#                 row['address'],
#                 str(row['zip']).strip().zfill(5),  # Preserve leading zeros (e.g., "00234")
#                 row['state'],
#                 str(row['phone']).strip()
#             ))
#         conn.commit()
#     except errors.UniqueViolation as e:
#         print(f"Duplicate PID: {row['pid']}. Skipping.")
#         conn.rollback()
#     except Exception as e:
#         print(f"Error inserting data: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()

def populate_db(conn):
    cursor = conn.cursor()
    
    # Create table (IF NOT EXISTS)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            PID BIGINT PRIMARY KEY,
            DOB DATE,
            P_Name VARCHAR(255),
            SSN VARCHAR(64),
            Address VARCHAR(255),
            Zipcode VARCHAR(10),
            State_Abv CHAR(2),
            phone_num VARCHAR(20)
        );
    ''')
    conn.commit()

    patients = pd.read_csv('patients.csv')

    try:
        for index, row in patients.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO Patients 
                        (PID, DOB, P_Name, SSN, Address, Zipcode, State_Abv, phone_num)
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (PID) DO NOTHING  -- Skip duplicates
                """, (
                    row['pid'],
                    pd.to_datetime(row['dob']).strftime('%Y-%m-%d'),
                    row['name'],
                    str(row['ssn']).strip(),
                    row['address'],
                    str(row['zip']).strip().zfill(5),
                    row['state'],
                    str(row['phone']).strip()
                ))
            except errors.UniqueViolation:
                print(f"Skipping duplicate PID: {row['pid']}")
                conn.rollback()  # Reset failed transaction
                continue  # Skip to next row
        conn.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        conn.rollback()
    finally:
        cursor.close()

# Usage
if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost"
    )
    populate_db(conn)
    conn.close()
