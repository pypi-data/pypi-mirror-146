CREATE TABLE IF NOT EXISTS patient_table (
	patient_uid TEXT NOT NULL,
	age TEXT,
	gender TEXT,
	weight INTEGER,
    bmi INTEGER,
    patient_size FLOAT,
    PRIMARY KEY (patient_uid)
);
