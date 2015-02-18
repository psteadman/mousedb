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

``` sh
sqlite3 databasename.db < filename.sql
```

##### mousedb.py usage

``` sh
mousedb.py [options] database.db
```

##### To access help run: 

``` sh
mousedb.py --help
```

#### Populating your database

1. Add a new study to your database
    This is used to add a new study within the mouse database
    Example:
    ``` sh
    mousedb.py -s --studyid CREB-hippocampus --mouseprefix CREBHippo
    ```

2. Add mice to your study
    This is required to tell the database the name of each mouse that will be involved with a study.
    Example: 
    ``` sh
    mousedb.py -m --studyid StudyName --sex M --breeder 550540 --dob 20141127 --cage 557884 --genotype WT mydatabase.db
    mousedb.py -m --mouseid Study1_0022 --injections='Tamoxifen, 1, 21.9' (drug, # injections, weight at each injection)
    ```

3. Add a training experiment
    This is required to tell the database that a mouse has undergone a behavioural training experiment and the characteristics of that session. 
    Example:
    ``` sh
    mousedb.py franklandpsteadman.db -t --ttype watermaze --startdate 20150217 --protocol='6 trial/dy, 3 days' --trainingid 2015-004 --mouseid Study1_0020
    ```

4. Add a training experiment's data
    This is where you upload data from a behaviour experiment, whether it is fear conditioning, rotarod, watermaze, etc. into the database
    Example:

    