
-- ##############Output Formats:#########
.separator ", "
.mode column
.header on

--##############Tables:############### 

--# Study must be entered first before you can enter mice in it
CREATE TABLE Study (
StudyID TEXT NOT NULL PRIMARY KEY, --# Unique StudyID/study name
MouseIDprefix TEXT NOT NULL, --# Prefix for naming new study mice
DateAdded TEXT
);

--# Mouse must be entered after study is before can add any training or imaging
CREATE TABLE Mouse (
MouseID TEXT NOT NULL PRIMARY KEY, --# Unique name for a mouse
StudyID TEXT NOT NULL, --# StudyID for which this mouse participated in
DOB TEXT, --# Date of birth for mouse --- YYYYMMDD
Breeder TEXT, --# The breeder cage number
Cage TEXT, --# The cage number for mouse
Sex TEXT, --# The sex of the mouse
Genotype TEXT, --# The genotype for mouse
Injections TEXT, --# Type and number of injections if applicable
Notes TEXT,
FOREIGN KEY(StudyID) REFERENCES Study(StudyID)); --# Extra notes

CREATE TRIGGER MouseInsert
before insert on Mouse
for each row begin
select raise(abort, 'Insert on table "Mouse" violates Foreign Key Constraint "MouseInsert" - ensure study is in database')
where (SELECT StudyID FROM Study WHERE StudyID = NEW.StudyID) is null;
end;
CREATE TRIGGER MouseUpdate
before update on Mouse
for each row begin
select raise(abort, 'Update on table "Mouse" violates Foreign Key Constraint "MouseUpdate" - ensure study is in database')
where (SELECT StudyID FROM Study WHERE StudyID = NEW.StudyID) is null;
end;

CREATE TABLE Training (
MouseID TEXT NOT NULL, --# From Mouse table
TrainingID TEXT NOT NULL, --# Training cohort YYYY-### starting at YYYY-001
TrainingType TEXT NOT NULL, --# E.g. FC-Cxt, MWM-spatial, Rotarod, FC-Tone
StartDate TEXT, --# Date of training start --- YYYYMMDD
Protocol TEXT, --# E.g 6 trials per day for 4 days, 3 tones 1 minute apart
FOREIGN KEY(MouseID) REFERENCES Mouse(MouseID));

CREATE TRIGGER TrainingInsert
before insert on Training
for each row begin
select raise(abort, 'Insert on table "Training" violates Foreign Key Constraint "TrainingInsert" - ensure mouse is in database')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;
CREATE TRIGGER TrainingUpdate
before update on Training
for each row begin
select raise(abort, 'Update on table "Training" violates Foreign Key Constraint "TrainingUpdate" - ensure mouse is in database')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;

CREATE TABLE Rotarod (
MouseID TEXT NOT NULL, --# From Mouse table
TrainingID TEXT NOT NULL, --# From Training table
Day INTEGER, --# The day of training
Trial INTEGER, --# The trial of that day (The Subject column is MouseName-TRIAL so extract from there)
Rod REAL, --# This is the Zone field in the exported file
Speed TEXT, --# This is the RPM range 
Duration REAL,
EndSpeed REAL,
FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID),
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID)); 

CREATE TRIGGER RotarodInsert
before insert on Rotarod
for each row begin
select raise(abort, 'Insert on table "Rotarod" violates Foreign Key Constraint "RotarodInsert" - ensure mouse is in database')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;
CREATE TRIGGER RotarodUpdate
before update on Rotarod
for each row begin
select raise(abort, 'Update on table "Rotarod" violates Foreign Key Constraint "RotarodUpdate" - ensure mouse is in database')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;