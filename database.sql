
-- ##############Output Formats:#########
.separator ", "
.mode column
.header on

-- Training FOREIGN KEY NOT YET IMPLEMENTED!!!!!

--##############Tables:############### 

--# Mouse is the main table and must be updated first before other tables can be updated with a specific
--# 		MouseID's data
CREATE TABLE Mouse (
MouseID TEXT NOT NULL PRIMARY KEY, --# Unique name for a mouse
StudyID TEXT NOT NULL, --# StudyID for which this mouse participated in
DOB TEXT, --# Date of birth for mouse --- YYYYMMDD
Breeder TEXT, --# The breeder cage number
Cage TEXT, --# The cage number for mouse
Genotype TEXT, --# The genotype for mouse
Notes text); --# Extra notes

CREATE TABLE Training (
MouseID TEXT NOT NULL, --# From Mouse table
TrainingID TEXT NOT NULL, --# Training cohort identifier YY-### starting at YY-001
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

CREATE TABLE FC (
MouseID TEXT NOT NULL, --# From Mouse table
TrainingID TEXT NOT NULL, --# From Training table

FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID),
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID)); 

CREATE TABLE MWM (
MouseID TEXT NOT NULL, --# From Mouse table
TrainingID TEXT NOT NULL, --# From Training table

FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID),
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID)); 

CREATE TABLE BarnesTrial (
MouseID TEXT NOT NULL, --# Mouse Name
TrainingID TEXT NOT NULL, --# Mouse's training ID (first, reverse, etc.)
Condition TEXT NOT NULL, --# Mouse's condition for that training
TotalTrial INTEGER, --# Mouse's trail number (1-30 under current protocol)
Day INTEGER, --# Day number
Trial INTEGER, --# Mouse's trial of Day X
DistanceMovedTotalcm REAL, --# Metric of learning
DistanceToTargetMeancm REAL, --# Metric of learning
DistanceToTargetTotalcm REAL, --# Metric of learning
HeadingMean REAL, --# Metric of learning
VelocityMean REAL, --# Metric of learning
DurationInNonTarget REAL, --# Metric of learning
FrequencyInNonTarget REAL, --# Metric of learning
LatencyHeadDirectToTarget REAL, --# Metric of learning
LatencyToTarget REAL, --# Metric of learning
VideoFile TEXT, --# file path
TrackingFile TEXT, --# file path
Trainer TEXT, --# trainer
Protocol TEXT,
FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID),
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID)); --#The Training Protocol utilized

CREATE TRIGGER BarnesTrialInsert
before insert on BarnesTrial
for each row begin
select raise(abort, 'Insert on table "BarnesTrial" violates Foreign Key Constraint "BarnesTrialInsert"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;
CREATE TRIGGER BarnesTrialUpdate
before update on BarnesTrial
for each row begin
select raise(abort, 'Update on table "BarnesTrial" violates Foreign Key Constraint "BarnesTrialUpdate"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;

-- This table may need to be altered as k and beta may not stay and what other columns should be added?
CREATE TABLE BarnesBehaviour (
MouseID TEXT NOT NULL, --# mouse name
TrainingID TEXT NOT NULL, --# Training (first, reverse, etc.)
Beta REAL, --# Beta for a exponential fit of the LatencyToTarget Metric
K REAL,
FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID),
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID));

CREATE TRIGGER BarnesBehaviourInsert
before insert on BarnesBehaviour
for each row begin
select raise(abort, 'Insert on table "BarnesBehaviour" violates Foreign Key Constraint "BarnesBehaviourInsert"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;

CREATE TRIGGER BarnesBehaviourUpdate
before update on BarnesBehaviour
for each row begin
select raise(abort, 'Update on table "BarnesBehaviour" violates Foreign Key Constraint "BarnesBehaviourUpdate"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;

CREATE TABLE Scan (
MouseID TEXT NOT NULL, --# Mouse name
Day TEXT, --# Relative Day of scan (Day 1, 2, 5, 15, etc)
TrueDay TEXT, --# Relative Day of scan (Day 0 = sunday before training)
Coil TEXT, --# Coil mouse was scanned in
Filename TEXT, --# Filename of reconstructed image
nScan TEXT, --# What scan number is it for this mouse?
ScanProtocol TEXT, --# What sequence was used?
Weight TEXT, --# Mouse weight in g
Operator TEXT, --# Who conducted the scan
ScanDate TEXT,
'Image Quality Metric' real, --# added August 26th 2010
Notes text, --# added August 26th 2010
Billed text, --# added August 26th 2010
DaysSinceLastScan text, --# added October 8th 2010
AgeAtScan real, --# added October 8th 2010
ReversalDay text, --# added October 8th 2010
TrueReversalDay real, --# added October 8th 2010
Modality text, --# added June 10th 2011
PerfusionDate text, --# added August 30th 2011
FOREIGN KEY (MouseID) REFERENCES Mouse(MouseID)); --# Date of scan yyyymmdd

CREATE TRIGGER ScanInsert
before insert on Scan
for each row begin
select raise(abort, 'Insert on table "Scan" violates Foreign Key Constraint "ScanInsert"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;
CREATE TRIGGER ScanUpdate
before update on Scan
for each row begin
select raise(abort, 'Update on table "Scan" violates Foreign Key Constraint "ScanUpdate"')
where (SELECT MouseID FROM Mouse WHERE MouseID = NEW.MouseID) is null;
end;

-- Removed this trigger as does not seem to be working correctly - gave error when I tried to delete mouse even though there should have been no other conflict - October 15, 2010
--CREATE TRIGGER MouseDelete
--before delete on Mouse
--for each row begin
--select raise(abort, 'Delete on table "Mouse" violates Foreign Key Constraint "MouseDelete" MouseID for this delete is used in other tables still, remove to proceed.')
--where ((SELECT MouseID FROM Training WHERE MouseID = OLD.MouseID) is null)
--or ((SELECT MouseID FROM Scan WHERE MouseID = OLD.MouseID) is null)
--or ((SELECT MouseID FROM BarnesTrial WHERE MouseID = OLD.MouseID) is null)
--or ((SELECT MouseID FROM BarnesBehaviour WHERE MouseID = OLD.MouseID) is null);
--end;

