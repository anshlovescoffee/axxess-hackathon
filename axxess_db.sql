CREATE DATABASE Patients_DB;
USE Patients_DB;
CREATE TABLE Patients (
	PID INT PRIMARY KEY,
    P_Name VARCHAR(50),
    SSN INT,
    Address VARCHAR(50),
    Zipcode INT,
    State_Abv CHAR(2)
);
CREATE TABLE Patient_measurements (
	PID INT PRIMARY KEY,
    Age INT,
    Sex TINYINT,
    Weight INT,
    Height INT,  
    FOREIGN KEY (PID) REFERENCES Patients(PID)
);

CREATE TABLE Visitation_log (
	PID INT PRIMARY KEY,
    N_Name VARCHAR(50),
    P_Name VARCHAR(50),
    Date_of_visitation DATE,
    Notes VARCHAR(1500),
    Respiratory_Rate INT,
    Heart_Rate INT,
    bp_systolic INT,
    bp_diastolic INT,
    measurement_time TIMESTAMP,
    CONSTRAINT systolic_check CHECK (bp_systolic BETWEEN 60 AND 250),
    CONSTRAINT diastolic_check CHECK (bp_diastolic BETWEEN 40 AND 180),
    FOREIGN KEY (PID) REFERENCES Patients(PID)
);

CREATE TABLE Med (
	Med_Name CHAR(50) PRIMARY KEY,
    Total_Amount DECIMAL(5,2),
    Unit CHAR(10)
);

CREATE TABLE Patient_Meds (
	PID INT PRIMARY KEY,
    Med_Name CHAR(50),
    Dosage DECIMAL(5.2),
    Unit CHAR(10),
	Remaining DECIMAL(5,2),
    Exp_Date DATE,
    FOREIGN KEY (PID) REFERENCES Patients(PID),
    FOREIGN KEY (Med_Name) REFERENCES Med(Med_Name)
);


INSERT INTO Patients (PID, P_Name, SSN, Address, Zipcode, State_Abv) 
VALUES ( 1, "Jude Joubert", 435762835, "865 Greenside Dr.", 75080, 'TX');
INSERT INTO Patient_measurements (PID, Age, Sex, Weight, Height) 
VALUES (1, 70, 1, 180, 68);
INSERT INTO Visitation_log (PID, N_Name, P_Name, Date_of_visitation, Notes, Respiratory_Rate, Heart_Rate, bp_systolic, bp_diastolic, measurement_time) 
VALUES (1, 'Nurse A', 'John Doe', '2023-10-01', 'Routine checkup', 16, 75, 120, 80, NOW());
INSERT INTO Med (Med_Name, Total_Amount, Unit) 
VALUES ('Morphine', 20.00, 'mg');
INSERT INTO Patient_Meds (PID, Med_Name, Dosage, Unit, Remaining, Exp_Date) 
VALUES (1, 'Morphine', 5.00, 'mg', 10, '2028-10-01');
