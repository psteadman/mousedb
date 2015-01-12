MouseDB
=========

This is a python, r, and sqlite code for managing a database of mice used in experiments. This can help with colony management, tracking mouse behaviour experiments, mouse behaviour data and analysis of the data. It may also include imaging later on.

#### Updates:

- Operational for rotarod data entry. 
- Working on watermaze and fear conditioning

# An user guide to MouseDB

A python and sqlite database for managing your mouse colony

##### Setting up your computer to use MouseDB

Python libraries required

Requires sqlite3 - most computers should have this installed already but if not please go [download](https://sqlite.org/download.html).


##### Setting up your sqlite database

```bash
sqlite3 databasename.db < filename.sql
```

##### mousedb.py usage

```bash
mousedb.py [options] database.db
```

##### To access help run: 

```
mousedb.py --help
```

#### Populating your database

1. Add a new study to your database


2. Add mice to your study
    This is required to tell the database the name of each mouse that will be involved with a study.
    Example: 
    

3. Add a training experiment
    This is required to tell the database that a mouse has undergone a behavioural training experiment and the characteristics of that session. 
    Example:
    

4. Add a training experiment's data
    This is where you upload data from a behaviour experiment, whether it is fear conditioning, rotarod, watermaze, etc. into the database
    Example:

    