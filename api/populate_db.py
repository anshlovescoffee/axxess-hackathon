import pandas as pd
import psycopg2
from psycopg2 import errors

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patient_measurements (
            PID BIGINT PRIMARY KEY,
            Age INT,
            Sex INT,
            Weight INT,
            Height INT,  
            FOREIGN KEY (PID) REFERENCES Patients(PID)
        );
    ''')
    conn.commit()

    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS Visitation_log (
    #      PID INT PRIMARY KEY,
    #         N_Name VARCHAR(50),
    #         P_Name VARCHAR(50),
    #         Date_of_visitation DATE,
    #         Notes VARCHAR(1500),
    #         Respiratory_Rate INT,
    #         Heart_Rate INT,
    #         bp_systolic INT,
    #         bp_diastolic INT,
    #         Temp INT,
    #         CONSTRAINT systolic_check CHECK (bp_systolic BETWEEN 60 AND 250),
    #         CONSTRAINT diastolic_check CHECK (bp_diastolic BETWEEN 40 AND 180),
    #         FOREIGN KEY (PID) REFERENCES Patients(PID)
    #     );
    # ''')
    # conn.commit()

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

                cursor.execute(f'''
                    INSERT INTO Patient_measurements 
                        (PID, Age, Sex, Weight, Height) 
                    VALUES 
                        (%s, %s, %s, %s, %s)
                    ON CONFLICT (PID) DO NOTHING  -- Skip duplicates
                ''', ( 
                    row['pid'],
                    row['age'],
                    row['sex'],
                    row['weight'],
                    row['height']
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

