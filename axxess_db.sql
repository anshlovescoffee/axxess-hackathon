CREATE DATABASE Patients_DB;
USE Patients_DB;
CREATE TABLE Patients (
	PID INT PRIMARY KEY,
    DOB DATE,
    P_Name VARCHAR(50),
    SSN INT,
    Address VARCHAR(50),
    Zipcode INT,
    State_Abv CHAR(2),
    phone_num VARCHAR(10)
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
    Temp INT,
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

