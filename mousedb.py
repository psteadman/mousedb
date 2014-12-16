#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is to interact with the SQLite database to input new data
#
# Created by Patrick Steadman, Mouse Imaging Centre, Hospital for Sick Children
# Supervised by Dr. Jason Lerch
# Aug 2010 to Dec 2010 - v1
# 

import string
from numpy import *
import sys
import os, glob
import commands
import optparse 
import csv
import sqlite3
import datetime

#---------------------------------------------------------------------------------
#							TO DO
# Think about how options can be put in as lists and then entered in the database as 1 entry in list is 1 row

# Error checking for whether options input data is formated correctly example weight should be ##.# and nothing else and day should be # 
# Write code in R to input behaviour analysis data into BarnesBehaviour table
# Fix DOB entry so it is consistent with other fields should be dd/mm/yy and then update this in all places where it is called or used (includes Update-dates.py and several spots in this program)

# FIXED so that if prior scan doesnt exist for a mouse scanned first time on a day other than 0 it will work...
# SEEMS FINE in R: Question whether the default for trday and rday should be 'NA' or should it be None
# DONE: Add something in add scan and add mouse training and add behaviour trial which checks to make sure that entry doesn't already exist
# DONE: Add function for determining the month in numeric form from input of month in three letter short form
# DONE for all but tracking/video file: Add error statement to not only list required options but also optional options.
# DONE: For the option itself... For option itself optparser checks for option to exist
# DONE Take optparse help and the error checking statements and make them a variable which is called by both so that changes are centralized
# DONE: Remove all conn and create a function for executing with database that just has input of the statement and variables
# DONE: Create new program that updates all days since last scan and nscan and then just run this at the end of the program every time it is run - CALLED Update-dates.py
#---------------------------------------------------------------------------------

# Functions:
def monthnumeric( monthin ):
	if (monthin == 'jan'):
		month = 1
	elif monthin == 'feb':
		month = 2
	elif monthin == 'mar':
		month = 3
	elif monthin == 'apr':
		month = 4
	elif monthin == 'may':
		month = 5
	elif monthin == 'jun':
		month = 6
	elif monthin == 'jul':
		month = 7
	elif monthin == 'aug':
		month = 8
	elif monthin == 'sep':
		month = 9
	elif monthin == 'oct':
		month = 10
	elif monthin == 'nov':
		month = 11
	elif monthin == 'dec':
		month = 12
	return month; 
def yearnumeric( yearin ):
	year = "20%s" %yearin
	year = int(year)
	return year;
def executedb( connection, statement, variables ):
	out = connection.cursor()
	out.execute(statement, variables)
	con.commit()
	out.close();
def fetchdb( connection, statement, variables ):
	out = connection.cursor()
	out.execute(statement, variables)
	out = out.fetchone()
	return out;
#Variables for help
help.scanopts = 'Required options: --mouseid, --image, --day, --weight, --operator, --modality\n \
Optional options: --tday, --scannote, --bill, --quality, --rday, --trday --perfusion (i.e. dd/mm/yyyy), --study (keep consistent for each study)'
help.trainingopts = 'Required options: --mouseid, --condition, --startdate (i.e. dd/mm/yyyy) \n \
Optional options: --trainingid(default: basic), --protocol (default: 1.02), --maze (default: barnes)'
help.mouseopts = 'Required options: --mouseid, --dob (i.e. dd/mm/yyyy), --breeder, --cage\n \
Optional options: --genotype'
help.trialopts = 'Required options: --csvfile, --trainer, --mouseid, \n \
Optional options: --trainingid (default: basic)'
# Below not complete yet
help.videotrackingfile = 'Required options: --mouseid, --mdescript, --trainingid\n \
Optional options: --path'


if __name__ == "__main__":

	usage = "%prog [options] database.db"
	description = "Adds data to a SQLite database based on the input arguments"
	parser = optparse.OptionParser(usage=usage, description=description)
	group1 = optparse.OptionGroup(parser, 'Add Mouse options')
	group2 = optparse.OptionGroup(parser, 'Add Training options')
	group3 = optparse.OptionGroup(parser, 'Add Scan options')
	group4 = optparse.OptionGroup(parser, 'Add Trial data options')
	group5 = optparse.OptionGroup(parser, 'Add video and tracking file options')
#	Add New Mouse Options
	parser.add_option("-m","--addmouse", dest="addmouse", #Boolean argument
					 help='Required when adding a mouse to the database in the Mouse table;\
					 Other %s' %help.mouseopts, 
					 default=False, action='store_true')
	group1.add_option("--mouseid", dest="mouseid",
					 help="MouseID of a specific animal",
					 type="string")
	group1.add_option("--dob", dest="dob",
					 help="Date of birth of a specific animal (i.e. dd/mm/yyyy)",
					 type="string")					 
	group1.add_option("--breeder", dest="breeder",
					 help="Breeder cage number (i.e. C1186964) or provider (i.e. Taconic)",
					 type="string")
	group1.add_option("--cage", dest="cage",
					 help="Home cage of a specific animal",
					 type="string")
	group1.add_option("--genotype", dest="genotype",
					 help="Genotype of a specific animal",
					 type="string", default='C57BL6')
	group1.add_option("--epi", dest="epigenotype",
					 help="Epigenotype of a specific animal",
					 type="string", default='NA')
	group1.add_option("--mousenote", dest="mnote",
					 help="Notes on the animal",
					 type="string",default=None)
	group1.add_option("--study", dest="study",
					 help="Name of study which animal was used for",
					 type="string",default=None)
#	Add New Training Regime Options
	parser.add_option("-t","--addtraining", dest="addtraining", #Boolean argument
					 help='Required when adding a mouse to the database in the Training table;\
					 Other %s' %help.trainingopts,
					 default=False, action='store_true')
	group2.add_option("--condition", dest="condition",
					 help="Condition of training for animal of interest",
					 type="string")
	group2.add_option("--startdate", dest="startdate",
					 help="Start date of training for animal of interest with that TrainingID \
					 (i.e. dd/mm/yyyy)",
					 type="string")
	group2.add_option("--trainingid", dest="trainingid",
					 help="Current training session type for animal of interest \n \
					 Default is 'basic' representing a single-initial training session.",
					 type="string", default="basic")
	group2.add_option("--protocol", dest="protocol",
					 help="Training protocol for animal of interest (e.g. 1.02)",
					 type="string", default='1.02')
	group2.add_option("--maze", dest="maze",
					 help="Maze used to train animal of interest (e.g. barnes)",
					 type="string",default='barnes')
#	Add New Scan Options
	parser.add_option("-s","--addscan", dest="addscan", #Boolean argument
					 help='Required when adding a scan to the database in the Scan table;\
					 Other %s' %help.scanopts, 
					 default=False, action='store_true')
	group3.add_option("--image", dest="image",
					 help="Minc File to be input to database",
					 type="string")
	group3.add_option("--day", dest="day",
					 help="Relative day of scan (0, 1, 5, 15, etc.)",
					 type="int")
	group3.add_option("--weight", dest="weight",
					 help="Weight of animal",
					 type="float")
	group3.add_option("--operator", dest="operator",
					 help="Operator(s) of scan",
					 type="string")
	group3.add_option("--modality", dest="modality",
			                 help="Modality image acquired with (e.g. 'invivoMRI', 'binb', 'OPT', 'DTI')",
			                 type="string")
	group3.add_option("--perfusion", dest="perfusion",
					 help="Date of perfusion ( dd/mm/yyyy ) for image done with modality binb, OPT or DTI",
					 type="string", default='NA')		
	group3.add_option("--tday", dest="TrueDay",
					 help="TrueDay 0 is the Sunday before training\
					 (e.g. day 0 scan friday before training, is true day=-2)",
					 type='string', default=False)
	group3.add_option("--scannote", dest="snote",
					 help="Notes on the scan",
					 type="string",default=None)
	group3.add_option("--bill", dest="bill",
					 help="Enter yes only if this scan has been billed",
					 type="string", default='No')
	group3.add_option("--quality", dest="imgquality",
					 help="Image Quality Metric: 1 - severe artefact, \
					 2 - below average (i.e some motion), 3 - average (DEFAULT), 4 - above average",
					 default=3, type="int")		
	group3.add_option("--rday", dest="reversalday",
					 help="Relative reversal day of scan, if scan is for\
					 mouse during or after reversal training",
					 type="string", default='NA')		
	group3.add_option("--trday", dest="TrueReversalDay",
					 help="True reversal day 0 is Sunday before training\
					 (e.g. rday 0 scan friday before training, is true reversal day=-2",
					 type="string", default=False)					  
#	Add New Trial Information Options
	parser.add_option("-r","--addtrial", dest="addtrial", #Boolean argument
					 help='Required when adding a trial to the database in the BarnesTrial table;\
					 Other %s' %help.trialopts, 
					 default=False, action='store_true')
	group4.add_option("--csvfile", dest="csvfile",
					 help="csv file of a trial or set of trials",
					 type="string") # Not read as a string but as a csv file... must fix this
	group4.add_option("--trainer", dest="trainer",
					 help="Trainer(s) of trial",
					 type="string")
#	Add Tracking and Video File Options
	parser.add_option("-f","--addvideotrackingfile", dest="addfile", #Boolean argument
					 help='Required when adding a video and/or tracking file to the database\
					 in the BarnesTrial table; Other %s' %help.videotrackingfile, 
					 default=False, action='store_true')
	group5.add_option("--path", dest="direct",
					 help="Directory containing the Noldus data\
					 (something like: 14_jun_10_taxibus_barnes)",
					 type="string", default='.')
	group5.add_option("--mdescript", dest="mouse_descriptor",
					 help="For that MouseID's condition the index in the sequence\
					 of training the mice for that condition\
					 (i.e. 2 if 2nd mouse trained in that training session for bus group)",
					 type="string")
	parser.add_option_group(group1)
	parser.add_option_group(group2)
	parser.add_option_group(group3)
	parser.add_option_group(group4)
	parser.add_option_group(group5)
	(opts, args) = parser.parse_args()
###########################
###########################
# 							___Program___		
###########################
###########################
	prog = os.path.basename(sys.argv[0])
	usage = "%s [options] database.db" %prog
# Declare some variables and check boolean options presence
	# database = '/projects/souris/psteadman/LMDatabase/DatabaseLearningAndMemory.db'
	if (args == []):
		database = 'your database'
		print 'Missing database input, please provide a database. \n' + usage + '\n'
	else:
		database = args[0]
		print 'Preparing to enter data into ' + database
		con = sqlite3.connect(database)
	if (opts.addmouse == False and opts.addtraining == False and opts.addscan == False 
	 	and opts.addtrial == False and opts.addfile == False):
	 	print 'No options given... \n' + usage + '\n'
	else:
		print "Attempting to run %s..." %prog
			
# Add Mouse to database			
	if opts.addmouse == 1:
# Check for the correct input options
		if opts.mouseid != None and opts.dob != None and opts.breeder != None and opts.cage != None:
			print 'Adding mouse ' + opts.mouseid + ' to ' + database
			executedb(con, 'INSERT INTO Mouse (MouseID, DOB, Breeder, Cage, Genotype,\
						Epigenotype, Study, Notes) VALUES (?,?,?,?,?,?,?,?)',
					   	(opts.mouseid, opts.dob, opts.breeder, opts.cage, opts.genotype, 
					   	opts.epigenotype, opts.study, opts.mnote))
			print '%s successfully added to %s' % (opts.mouseid,database)
		else:
			print '\nMandatory options for adding a mouse to %s are missing.\n%s\n' % (database, help.mouseopts)

# Current database is designed with foreign keys for the Training table, 
	# so only should be able to add a new training session for mouse that exists in the database already

# Add training session to database			
	if opts.addtraining == 1:
# Check for the correct input options
		if opts.mouseid != None and opts.condition != None and opts.startdate != None:
			print 'Adding new training session for %s' %opts.mouseid
# Checking to see if entry already exists based on MouseID and starting date of training
			(d, ) = fetchdb(con, 'Select count(*) from Training where MouseID = ? and StartDate = ?', 
							(opts.mouseid, opts.startdate))
			if d == 0:
				executedb(con, 'INSERT INTO Training (MouseID, TrainingID, Condition, StartDate,\
							Protocol, Maze, Condition2) values (?,?,?,?,?,?,?)',
							(opts.mouseid, opts.trainingid, opts.condition, opts.startdate, 
							opts.protocol, opts.maze, opts.condition2))
				print '%s %s training session has been added' % (opts.mouseid, opts.trainingid)
			else:
				print 'Training Session already exists'
		else:
			print '\nMandatory options for adding a training session to %s are missing.\n%s\n' % (database, help.trainingopts)

# Add Scan to database
	if opts.addscan == 1:
# Check for correct input options
		if opts.mouseid != None and opts.image != None and opts.day != None and opts.weight != None and opts.operator != None and opts.modality != None:
			print 'Adding %s' %opts.image
# Checking to see if entry already exists based on Filename
			(d, ) = fetchdb(con, "Select count(*) from scan where Filename = ?", [opts.image])
			if d == 0: # d should be 0 if no prior entry of same Filename in database
			  	if opts.modality == 'binb' or 'MRI' or 'mri' or 'DTI' or 'dti' or 'invivoMRI':
# Using mincinfo to get the coil, date of scan and the sequence name from the image header				
					coil_str = 'mincinfo -attval vnmr:coil %s' %opts.image
					Coil = commands.getoutput(coil_str)
					ScanDate_str = 'mincinfo -attval vnmr:datestr %s' %opts.image # (e.g. ddmmmyy = 09oct10)
					ScanDate = commands.getoutput(ScanDate_str)
					Protocol_str = 'mincinfo -attval vnmr:seqfil %s' %opts.image
					Protocol = commands.getoutput(Protocol_str)
			  	elif opts.modality == 'opt' or 'OPT':
					Coil = 'NA'
					Protocol = 'Not implemented for OPT'
					ScanDate = 'Not implemented for OPT'
# Determining value for trueday and reversal true day based on whether user used either option
				if opts.TrueDay == False:
					TrueDay = opts.day
				else:
					TrueDay = opts.TrueDay	
				if opts.TrueReversalDay == False:
					TrueRD = opts.reversalday
				else:
					TrueRD = opts.TrueReversalDay
# Reformating the ScanDate, then fetching the mouse's date of birh and reformating that date as well				
				year = yearnumeric ( ScanDate[+5:] )
				month = monthnumeric( ScanDate[+2:-2] )
				ScanDateReformatted = datetime.date(year,int(month),int(ScanDate[:-5]))
				(age, ) = fetchdb(con, "SELECT DOB FROM Mouse WHERE MouseID=?", [opts.mouseid]) # mm/dd/yy
				age = str(age)
				#year = yearnumeric( age[-2:] )
				year = int(age[-4:]) # dd/mm/yyyy
				#dob = datetime.date(year,int(age[:-6]),int(age[+3:-3]))
				dob = datetime.date(year,int(age[+3:-5]),int(age[:-8])) # dd/mm/yyyy
# Using date of birth and scan date, determine here the age at scan
				AgeAtScan = ScanDateReformatted - dob
				print "AgeAtScan %s" %AgeAtScan
# Determining the number of scans for this mouse which previously exist ini the databse
				(numscan, ) = fetchdb(con, "SELECT count(*) FROM Scan WHERE MouseID = ?\
								AND CAST(Day as INTEGER) < ?", (opts.mouseid, opts.day)) 
				numscan = str(numscan)
				numscan = int(numscan)
				print 'numscan %s' %numscan
				# If previous scans exist then add 1 for current scan number
				if opts.TrueDay == False and numscan != 0:	 			
					nscan = numscan + 1
					print 'nscan %s' %nscan
# Here we are retrieving scan date from the previous scan and 
# reformating it then determining the number of days since last scan
					Datelastscan = fetchdb(con, "SELECT ScanDate FROM Scan WHERE\
										MouseID = ? AND nScan = ?", (opts.mouseid, numscan)) 
					Datelastscan = str(Datelastscan[0])
					year = yearnumeric( Datelastscan[+5:] )
					month = monthnumeric( Datelastscan[+2:-2] )
					lastdate = datetime.date(year,int(month),int(Datelastscan[:-5]))
					DaysSinceLastScan = ScanDateReformatted - lastdate
					DaysSinceLastScan = DaysSinceLastScan.days
				else: # If this is the first scan then do this
					nscan = 1
					DaysSinceLastScan = 0
				if opts.modality == 'binb' or 'OPT' or 'DTI' and opts.perfusion == None:
					print 'To add an image from modality: binb, OPT, or DTI you must provide --perfusion dd/mm/yy'
				if opts.modality == 'binb' or 'MRI' or 'mri' or 'DTI' or 'dti' or 'invivoMRI' or 'opt' or 'OPT':
					executedb(con, "INSERT INTO Scan (MouseID, Day, TrueDay, Coil, Filename,\
					nScan, ScanProtocol, Weight, Operator, ScanDate, 'Image Quality Metric',\
					Notes, Billed, DaysSinceLastScan, AgeAtScan, ReversalDay, TrueReversalDay,\
					Modality, PerfusionDate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
					(opts.mouseid, opts.day, TrueDay, Coil, opts.image, nscan, Protocol, opts.weight,
					opts.operator, ScanDate, opts.imgquality, opts.snote, opts.bill, DaysSinceLastScan,
					AgeAtScan.days, opts.reversalday, TrueRD, opts.modality, opts.perfusion))
					print "%s successfully added to %s" % (opts.image,database)
				else:
					print 'Scan not added'
			else:
				print 'Scan already exists in %s' %database
		else:
			print '\nMandatory options for adding a scan to %s are missing.\n%s\n' % (database, help.scanopts)

# Add Barnes Trial to Database	
	if opts.addtrial ==1:
# Check for correct input options
		if opts.csvfile != None and opts.trainer != None and opts.mouseid != None and opts.trainingid != None:
			print 'Adding %s for mouse %s with training id %s' %(opts.csvfile, opts.mouseid, opts.trainingid)
# Retrieve from Training table in database the mouse's training condition and training protocol			
			friend = fetchdb(con, "select Condition, Protocol from Training where MouseID = ? and TrainingID = ?",(opts.mouseid, opts.trainingid)) 
			print friend
			Condition = friend[0]
			Protocol = friend[1]
			videotrack="soon" #for right now but may change in future; applies to video and tracking file columns
			trial_csv = open(opts.csvfile, 'r') 
# remove headers in the txt/csv file - first 4 lines
			trial_csv.readline()
			trial_csv.readline()
			trial_csv.readline()
			trial_csv.readline()
			entries = trial_csv.readlines() # move csv data to variable entries
			for entry in entries:
				items = entry.split(",") #split each line based on ,
				items = [x.strip() for x in items] # strip spaces
				items = [x.strip('""') for x in items] # strip quotations
				totaltrial = (int(items[2])-1)*6+int(items[3]) # determine # for total trials (1 to 30 with protocol 1.01)
				if items[12] == '-': #If mouse never found target change latency to 180 seconds 
					items[12] = 180.0
# Check to see if entry already exists  
				(d, ) = fetchdb(con, "Select count(*) from BarnesTrial where MouseID = ? and TrainingID = ? and TotalTrial = ?", (opts.mouseid, opts.trainingid, totaltrial))
				if d == 0:
					executedb(con, "INSERT INTO BarnesTrial (MouseID, TrainingID, Condition, TotalTrial, Day, Trial, DistanceMovedTotalcm, DistanceToTargetMeancm, DistanceToTargetTotalcm, HeadingMean, VelocityMean, DurationInNonTarget, FrequencyInNonTarget, LatencyHeadDirectToTarget, LatencyToTarget, VideoFile, TrackingFile, Trainer, Protocol) Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(opts.mouseid, opts.trainingid, Condition, totaltrial, items[2], items[3], items[4], items[5], items[6], items[7],items[8],items[9],items[10],items[11],items[12], videotrack,videotrack, opts.trainer, Protocol))
					print 'Successfully added %s data for %s training total trial %s to the database' %(opts.mouseid, opts.trainingid, totaltrial)
				else:
					print 'Data from %s already exists in the database' %opts.csvfile
		else:
			print '\nMandatory options for adding behavioural data to %s are missing.\n%s\n' % (database, help.trialopts)
			
# Add video file and tracking file paths to database
	if opts.addfile == 1:	
# Check for correct input options
		if opts.mouse_descriptor != None and opts.mouseid != None and opts.trainingid != None:
			(d, ) = fetchdb(con, "select Condition from Training where MouseID = ? and TrainingID = ?",(opts.mouseid, opts.trainingid)) 
			Condition = d
			print "Adding tracking and video files for %s as a %s" % (opts.mouseid, Condition)	
			if Condition == 'bus':
				os.chdir(opts.direct) # changing working directory if --path option used
				for name in glob.glob('busmice_?_?'): # Should this be changed?
					day = name[+8:-2]
					trial = name[+10:]
					command_str = "find $PWD/%s/Media\ Files -name 'Trial* %s.mpg'" % (name, opts.mouse_descriptor)
					video = commands.getoutput(command_str)
					command_str = "find $PWD/%s/Data\ Files -name 'Track filet000%sa0000o0000_0001.trk'" % (name, int(opts.mouse_descriptor) - 1)
					track = commands.getoutput(command_str)
					executedb(con, "Update BarnesTrial set VideoFile = ?, TrackingFile = ? where MouseID = ? AND Condition = ? AND Day = ? AND Trial = ?",(video, track, opts.mouseid, Condition, day, trial))
			elif Condition == 'taxi':
				if opts.direct != '.': os.chdir(opts.direct) # used for custom named taximice folders
				os.chdir( glob.glob('taximice*')[0])
				n = commands.getoutput('ls Media\ Files/Trial*.mpg').split('\n')
				n = len(n)
				nmice = n/30
				for i in range(30):
					TotalTrial = i + 1
					if i == 0:
						count = i + int(opts.mouse_descriptor)
					elif i != 0:
						count = count + nmice
					command_str = "find $PWD/Media\ Files -name 'Trial* %s.mpg'" %count
					video = commands.getoutput(command_str)
					print(video)
					if (count-1) >= 10: command_str = "find $PWD/Data\ Files -name 'Track filet*%sa0000o0000_0001.trk'" %(count-1)
					if (count-1) < 10: command_str = "find $PWD/Data\ Files -name 'Track filet*0%sa0000o0000_0001.trk'" %(count-1)
					track = commands.getoutput(command_str)
					print(track)
					executedb(con, "Update BarnesTrial set VideoFile = ?, TrackingFile = ? where MouseID = ? AND Condition = ? AND TotalTrial = ? AND TrainingID = ?",(video, track, opts.mouseid, Condition, TotalTrial, opts.trainingid)) # will give error if reversal training was the same condition again: fix this
			else:
				print 'error with condition'
				print Condition
			print 'Success!'
		else:
			print '\nMandatory options for adding tracking and video file to %s are mising.\n%s\n' % (database, help.videotrackingfile)
# Update the dates	
	if opts.mouseid != None:
		command_str = "/home/psteadman/bin/Update-dates.py %s -m %s" % (database, opts.mouseid)
		os.system(command_str)
	
