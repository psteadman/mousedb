#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is to interact with the SQLite database to input new data
#
# Created by Patrick Steadman, Mouse Imaging Centre, Hospital for Sick Children
# Supervised by Dr. Jason Lerch
# Aug 2010 to Dec 2010 - v1
# 

# Modified by Patrick Steadman, Frankland Lab, Hospital for Sick Children
# Supervised by Dr. Paul Frankland
# December 2014 - v1.01
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

# Define training protocols

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
# Variables for help dialogues
help.studyopts = 'Required options: --studyid, --mouseprefix'
help.mouseopts = 'Required options: --dob (i.e. yyyymmdd), \
--breeder, --cage\n \
Optional options: --mouseid, --genotype'
help.trainingopts = 'Required options: --mouseid, --ttype, \
--trainingid, --startdate (i.e. yyyymmdd) \n \
Optional options: --protocol'
help.rotarodopts = 'Required options: --mouseid, --trainingid, --day'

help.watermazeopts = ' Not yet implemented '
help.fcopts = ' Not yet implemented '

# help.trialopts = 'Required options: --csvfile, --trainer, --mouseid, \n \
# Optional options: --trainingid (default: basic)'
# # Below not complete yet
# help.videotrackingfile = 'Required options: --mouseid, --mdescript, --trainingid\n \
# Optional options: --path'
# help.scanopts = 'Required options: --mouseid, --image, --day, --weight, --operator, \
# --modality\n \
# Optional options: --tday, --scannote, --bill, --quality, --rday, --trday --perfusion \
# (i.e. dd/mm/yyyy), --study (keep consistent for each study)'


if __name__ == "__main__":

	usage = "%prog [options] database.db"
	description = "Adds data to a SQLite database based on the input arguments"
	parser = optparse.OptionParser(usage=usage, description=description)
	group0 = optparse.OptionGroup(parser, 'Add Study options')
	group1 = optparse.OptionGroup(parser, 'Add Mouse options')
	group2 = optparse.OptionGroup(parser, 'Add Training options')
	# group4 = optparse.OptionGroup(parser, 'Add Trial data options')
	# group5 = optparse.OptionGroup(parser, 'Add video and tracking file options')
#	Add New Study Options
	parser.add_option("-s","--addstudy", dest="addstudy", #Boolean argument
					 help='Required when adding a study to the database in the Study table;\n\
					 Other %s' %help.studyopts, 
					 default=False, action='store_true')
	group0.add_option("--studyid", dest="studyid",
					 help="StudyID or the name of the study \n \
					 This must be the same for an entire study e.g. NG2-motorlearning \n \
					 This is used for the entire study, so when adding new mice as well",
					 type="string",default=None)
	group0.add_option("--mouseprefix", dest="mouseprefix",
					 help="Naming prefix for mice in this study (e.g. studyprefix_0001)",
					 type="string",default=None)
#	Add New Mouse Options
	parser.add_option("-m","--addmouse", dest="addmouse", #Boolean argument
					 help='Required when adding a mouse to the database in the Mouse table;\n\
					 Other %s' %help.mouseopts, 
					 default=False, action='store_true')
	group1.add_option("--dob", dest="dob",
					 help="Date of birth of a specific animal (i.e. dd/mm/yyyy)",
					 type="string",default=None)
	group1.add_option("--cage", dest="cage",
					 help="Home cage of a specific animal",
					 type="string",default=None)	
	group1.add_option("--breeder", dest="breeder",
					 help="Breeder cage number",
					 type="string",default=None)
	group1.add_option("--genotype", dest="genotype",
					 help="Genotype of a specific animal",
					 type="string", default='WT')
	group1.add_option("--mousenote", dest="mnote",
					 help="Notes on the animal",
					 type="string",default=None)
	group1.add_option("--sex", dest="sex",
					 help="Sex of the animal",
					 type="string",default="M")

	group1.add_option("--mouseid", dest="mouseid",
					 help="MouseID of a specific animal (e.g. studyprefix_####)",
					 type="string",default=None)
	group1.add_option("--injections", dest="injections",
					 help="Type and number of injections then weight of mouse at injection",
					 type="string",default=None)

#	Add New Training Regime Options
	parser.add_option("-t","--addtraining", dest="addtraining", #Boolean argument
					 help='Required when adding a mouse to the database in the Training table;\n\
					 Other %s' %help.trainingopts,
					 default=False, action='store_true')
	group2.add_option("--ttype", dest="trainingtype",
					 help="Type of training for animal of interest \n \
					 (e.g. FC-Cxt, MWM-spatial, Rotarod, FC-Tone)",
					 type="string",default=None)
	group2.add_option("--startdate", dest="startdate",
					 help="Start date of training for animal of interest with that TrainingID \n \
					 Format is yyyymmdd",
					 type="string",default=None)
	# would be cool to automate this below... increment for each group but how do you define a group?
	group2.add_option("--trainingid", dest="trainingid",
					 help="Current training session type for animal of interest \n \
					 Format is YYYY-###",
					 type="string", default=None)
	group2.add_option("--protocol", dest="protocol",
					 help="Training protocol for animal of interest (default: 1.01)",
					 type="string", default='1.01')

#	Add rotarod training data
	parser.add_option("-r","--addrotarod",dest="rotarod", #Boolean argument
					 help='Required when adding rotarod data to the database; \n\
					 Other %s' %help.rotarodopts,
					 default=False, action='store_true')
	group2.add_option("--day", dest="day",
					 help="Day of data acquisition if a part of a process",
					 type="int")
	group2.add_option("--nmice", dest="nmice",
					 help="Number of mice in the csv file you are adding",
					 default="1", type="int")
	group2.add_option("--csvfile", dest="csvfile",
					 help="csv file of behaviour data",
					 type="string",default=None) 
					 # Not read as a string but as a csv file... must fix this

#	Add fear conditioning training data
	parser.add_option("-f","--addfearconditioning",dest="fearconditioning",
					 help='Required when adding fear conditioning data to the database; \n\
					 Other %s' %help.fcopts,
					 default=False, action='store_true')

#	Add morris watermaze training data
	parser.add_option("-w","--addwatermaze",dest="mwm",
					 help='Required when adding watermaze data to the database; \n\
					 Other %s' %help.watermazeopts,
					 default=False, action='store_true')



	parser.add_option_group(group0)
	parser.add_option_group(group1)
	parser.add_option_group(group2)

	(opts, args) = parser.parse_args()
###########################
###########################
# 							___Program___		
###########################
###########################
	prog = os.path.basename(sys.argv[0])
	usage = "%s [options] database.db" %prog
# Declare some variables and check boolean options presence
	if ((opts.addstudy == False and opts.addmouse == False and opts.addtraining == False \
		and opts.rotarod == False) or (args == [])):
	 	print 'Missing a database or no input options given... \n' + usage + '\n'
	 	sys.exit()
	else:
		print "Attempting to run %s..." %prog
		database = args[0]
		print 'Preparing to enter data into ' + database
		con = sqlite3.connect(database)

# Add Study to database			
	if opts.addstudy == 1:
# Check for the correct input options
		if opts.studyid != None and opts.mouseprefix != None:
			print 'Adding study ' + opts.studyid + ' to ' + database
			executedb(con, 'INSERT INTO Study (StudyID, MouseIDprefix, DateAdded) VALUES (?,?,?)',
					   	(opts.studyid, opts.mouseprefix, datetime.date.today().strftime("%Y%m%d") ))
			print '%s successfully added to %s with MouseIDprefix %s' % (opts.studyid,database, opts.mouseprefix)
		else:
			print '\nMandatory options for adding a study to %s are missing.\n%s\n' % (database, help.studyopts)

# Current database is designed with foreign keys for the Mouse table, 
	# so only should be able to add a new mouse for a study that exists in the database already

# Add Mouse to database			
	if opts.addmouse == 1:
# Check for the correct input options
		if opts.studyid != None and opts.dob != None and opts.breeder != None and opts.cage != None:
			mprefix = fetchdb(con, 'SELECT MouseIDprefix FROM Study where StudyID = ?',(opts.studyid, ) )[0]
			nmice = fetchdb(con, 'SELECT count(*) FROM Mouse where StudyID = ?',(opts.studyid, ))[0]
			if opts.mouseid == None:
				n = int(nmice)+1
				mouseid = mprefix + '_%04d' %n # should be format ####
			else:
				mouseid = opts.mouseid
			print 'Adding mouse ' + mouseid + ' to ' + database
			executedb(con, 'INSERT INTO Mouse (MouseID, StudyID, DOB, Breeder, Cage, Sex, \
						Genotype, Notes) VALUES (?,?,?,?,?,?,?,?)',
					   	(mouseid, opts.studyid, opts.dob, opts.breeder, opts.cage, opts.sex, 
					   	opts.genotype, opts.mnote))
			print '%s successfully added to %s' % (mouseid,database)
		elif opts.injections != None and opts.mouseid != None:
			# This will update even if mouse id is wrong, dbdata is None if mouseid doesnt exist
			# find a better error catcher than this
			executedb(con, 'UPDATE  Mouse SET Injections = ? WHERE MouseID = ?',
					   	(opts.injections, opts.mouseid))
			dbdata = fetchdb(con, 'SELECT * FROM Mouse where MouseID = ?', (opts.mouseid, ))
			for item in dbdata:
				print item,"|",
			print # to get new line for future prints
		else:
			print '\nMandatory options for adding a mouse to %s are missing.\n%s\n' % (database, help.mouseopts)

# Current database is designed with foreign keys for the Training table, 
	# so only should be able to add a new training session for mouse that exists in the database already

# Add training session to database			
	if opts.addtraining == 1:
		try: # may already be defined if adding mouse and training at the same time
			mouseid
		except NameError:
			mouseid = opts.mouseid
# Check for the correct input options
		if mouseid != None and opts.trainingtype != None and \
		opts.startdate != None and opts.trainingid != None:
			print 'Adding new training session for %s' %mouseid
# Checking to see if entry already exists based on MouseID and starting date of training
			(d, ) = fetchdb(con, 'Select count(*) from Training where MouseID = ? and StartDate = ?', 
							(mouseid, opts.startdate))
			if d == 0:
				executedb(con, 'INSERT INTO Training (MouseID, TrainingID, TrainingType, StartDate,\
							Protocol) values (?,?,?,?,?)',
							(mouseid, opts.trainingid, opts.trainingtype, opts.startdate, 
							opts.protocol))
				print '%s %s training session has been added' % (mouseid, opts.trainingid)
			else:
				print 'Training Session already exists'
		else:
			print '\nMandatory options for adding a training session to %s are missing.\n%s\n' % (database, help.trainingopts)

# Add rotarod data to the database
	if opts.rotarod == 1:
		try:
			mouseid 
		except NameError:
			mouseid = opts.mouseid 
# Check for correct input options
	# Perhaps assume mice trained in sequence so then ask for n mice and take first mouse + n for csvdata
		if opts.csvfile != None and opts.trainingid != None and mouseid != None and opts.day != None:
			if opts.nmice == 1 or opts.nmice == None: # we are adding many mice :)
				print "Entering %s mouse" %opts.nmice
			elif opts.nmice > 1:
				print "Entering %s mice" %opts.nmice
			elif opts.nmice < 1:
				print "Dude, less than 1 mouse given - are you sure you did this right?"
				sys.exit()
			# add data
			trial_csv = open(opts.csvfile, 'r')
			trial_csv.readline() # header line
			entries = trial_csv.readlines()
			for entry in entries:
				items = entry.split("\t") #split each line based on ,
				items = [x.strip() for x in items] # strip spaces
				trial = items[4][2:] # assume first 2 characters are mouse and a dash
				# if items[4][0] == items[3]:
				# 	subject = items[3]
				# else:
				# 	print "WARNING! using zone to determine subject because:"
				# 	print "Zone: "+items[3]+" != SubjectID: "+items[4][0]
				# 	subject = items[3]
				try:
					subject = items[4][0]
				except IndexError:
					print "Skipping zone %s - must've been empty" % (items[3])
					continue
				if int(subject) == 1:
					mouseid = opts.mouseid 
				elif int(subject) > 1 and opts.nmice >= int(subject):
					n = int(opts.mouseid[-4:])
					prefix = mouseid[:-4]
					mouseid = prefix+'%04d' %(n+int(subject)-1)
				elif opts.nmice < int(subject):
					print "nmice is less than %s" %subject
					break # exit this iteration of the for loop
			# Checking to see if entry already exists based on MouseID and starting date of training
				(d, ) = fetchdb(con, 'Select count(*) from Rotarod where MouseID = ? \
					and TrainingID = ? and Day = ? and Trial = ?', (mouseid, opts.trainingid, opts.day, trial))
				if d == 0:
					executedb(con, 'INSERT INTO Rotarod (MouseID, TrainingID, Day, Trial,\
								Rod, Speed, Duration, EndSpeed) values (?,?,?,?,?,?,?,?)',
								(mouseid, opts.trainingid, opts.day, trial, items[3], items[2],  
								items[5], items[6].strip(' RPM')))
					print "Added %s for %s on day %s in trial %s" % (mouseid, opts.trainingid, opts.day, trial)
					print "Data added: Rod Speed Duration EndSpeed "
					print items[3]+" "+items[2]+" "+items[5]+" "+items[6].strip(' RPM')
				else:
					print "This mouse, trial and day already exist in the %s" %database
		else:
			print '\nMandatory options for adding rotarod session to %s are missing.\n%s\n' % (database, help.rotarodopts)		

# # Update the dates	
# 	if opts.mouseid != None:
# 		command_str = "/home/psteadman/bin/Update-dates.py %s -m %s" % (database, opts.mouseid)
# 		os.system(command_str)
	