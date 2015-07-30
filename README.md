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
* numpy 
* sys
* optparse
* csv
* sqlite3

Requires sqlite3 - most computers should have this installed already but if not please go [download it](https://sqlite.org/download.html).


##### Setting up your sqlite database

``` sh
sqlite3 databasename.db <  databaseschemafile.sql
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
    mousedb.py -s --studyid CREB-hippocampus --mouseprefix CREBHippo \
    database.db
    ```

2. Add mice to your study

    This is required to tell the database the name of each mouse that will be involved with a study.
    
    Example: 
    ``` sh
    mousedb.py -m --studyid StudyName --sex M --breeder 550540 --dob 20141127 \
    --cage 557884 --genotype WT database.db
    mousedb.py -m --mouseid CREBHippo_0022 --injections='Tamoxifen, 1, 21.9' \
    database.db
    ```
    The --injections option is structured as "drug, # injections, weight at each injection" but the user can use an alternative structure.

3. Add a training experiment

    This is required to tell the database that a mouse has undergone a behavioural training experiment and the characteristics of that session. 
    
    Example:
    ``` sh
    mousedb.py database.db -t --ttype watermaze --startdate 20150217 \
    --protocol='6 trial/dy, 3 days' --trainingid 2015-004 --mouseid CREBHippo_0020 \
    database.db
    ```

4. Add a training experiment's data

    This is where you upload data from a behaviour experiment, whether it is rotarod, watermaze, fear conditioning, etc. into the database. Right now rotarod data upload is operational. The other two are in development. 
    
    Example:
    ``` sh
    mousedb.py database.db -r --trainingid 2014-008 \
    --mouseid CREBHippo_0008 --rodzone 4 --csvfile 141211-WT-Day3.txt --day 3
    mousedb.py database.db -r --mouseid CREBHippo_0014 --nmice 3 \
    --trainingid 2015-001 --day 1 --csvfile ../rotarodfiles/2015-001-Day1.txt
    ```

    