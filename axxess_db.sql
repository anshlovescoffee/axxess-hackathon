CREATE DATABASE Patients_DB;
USE Patients_DB;
CREATE TABLE Patients (
	PID INT PRIMARY KEY,
    P_Name VARCHAR(50),
    SSN INT(9),
    Address VARCHAR(50),
    Zipcode INT(5),
    State_Abv CHAR(2)
);
CREATE TABLE Patient_measurements (
	PID INT PRIMARY KEY,
    Age INT(3),
    Sex TINYINT,
    Weight INT(3),
    Height INT(3),  
    FOREIGN KEY (PID) REFERENCES Patients(PID)
);

CREATE TABLE Visitation_log (
	PID INT PRIMARY KEY,
    N_Name VARCHAR(50),
    P_Name VARCHAR(50),
    Date_of_visitation DATE,
    Notes VARCHAR(1500),
    Respiratory_Rate INT(4),
    Heart_Rate INT(4),
    bp_systolic INT,
    bp_diastolic INT,
    measurement_time TIMESTAMP,
    CONSTRAINT systolic_check CHECK (bp_systolic BETWEEN 60 AND 250),
    CONSTRAINT diastolic_check CHECK (bp_diastolic BETWEEN 40 AND 180)
);

CREATE TABLE Test(
PID INT PRIMARY KEY
);