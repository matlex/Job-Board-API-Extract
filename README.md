# Job-Board-API-Extract #
This is code that extracts Job and Candidate info using the Workable API

## Prerequisites: ##
* Python 3
* Virtual environment also should be created and activated with python 3 interpreter.
* You should have working database server (MySQL or PostgreSQL) with created database.


## How to install: ##
1. Create a clean virtual environment(with python 3) and activate it.
2. Install MySQLdb Client to a system. 
Run: **sudo apt-get install python-dev libmysqlclient-dev**
3. Run: **sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev**
4. Go to main application's directory and run **pip install -r requirements.txt**
5. Generate a new secret key for Django project - http://www.miniwebtool.com/django-secret-key-generator/
6. Go to the 'secrets' directory and rename "secrets_template.py" file to "secrets.py" file and fill in ALL constants properly.
7. Now we need create new database migrations. 
First run: python3 manage.py makemigrations to create migrations for django internal apps. 
Then you need to create migrations for every app. 
At the moment run: **python3 manage.py makemigrations workable_client_app**
8. Then apply newly created migrations: **python3 manage.py migrate**
9. Create a Django admin by running command: **python3 manage.py createsuperuser**
10. Launch application django-admin panel by running command **python manage.py runserver 0.0.0.0:8000**
11. Open **http://your_server_address:8000/admin** and try to enter to django-admin panel.
12. To start collecting data and save them into DB Run: **python3 manage.py process_workable_api** command. It will connect
to JobBoard API server and obtain all Job and Candidate data and then will save it into DataBase described in **workable_api/remote.py or local.py** file.
 
## About project settings for local or production environment: ##
There is a statement in setting.py on lines 111-115 where importing additional settings. It depends on 
whether computer's name exists in HOSTS list or not. If your computer name is 'UBUNTU' then
it will import settings from local.py file. It has differences between remote.py settings. For example 
debug mode for local is on, and for remote(production) is false. Also you can use just sqlite3 database
when you're working on local project to simplify manipulating with database. All above means you can
just put your pc name to 'HOSTS' list and the application will use settings from local.py settings file.
Otherwise it will use settings from remote.py file.

Settings was divided on 2 different files(local, remote) because developers, customers or anybody else can deploy a 
project locally on their PC's with one set of settings(for example they can use simple sqlite3 database instead mysql), 
but for production environment(DO, AWS or any other server) there could be another set of settings(debug=False etc.). 
It is made for convenient deploying without any settings interferences. It is a common practice.

Please keep in mind you have to put any other new settings in both places local.py and remote.py.

## Logging: ##
There is a parameter 'DEBUG_LEVEL' in both local.py and remote.py files. It must set to be True or False.
Depending on that the main logger will save information into log files. Log files placed in 'logs' directory.
There can be two versions of log files: main.log and main_debug.log. 
It depends on DEBUG(True/False) parameter in local.py or remote.py files.

## Environment on which application was tested: ##
* Python 3.5.2
* MySQL 5.7.18
* Ubuntu 16.04
* PIP 7.1.0

## Requirements: ##
All program requirements listed in requirements.txt

Which includes following python packages:

* Django==1.10.6
* requests==2.13.0
* wheel==0.24.0
* mysqlclient==1.3.10 (if you use MySQL database)

## Sample scheduling of the data download/sync from Workable: ##
There is a sync.sh bash script file. Edit and fill in **path_to_virtual_environment** and then just
add rule to execute that file via cron job.

## How the application works (DB model, what and how is being synched, limitations, etc...) ##
All database structure, tables, fields and properties described in **/workable_client_app/models.py** file. 
Here is used a Django ORM. See Django documentation for details and explanations.

For avoiding duplicating data the database was normalized and divided on different tables to store entities - https://en.wikipedia.org/wiki/Database_normalization 

In **/workable_client_app/admin.py** described what exactly will be showing in Django admin-panel. 
See Django documentation for details and explanations.

All network requests to Workable API endpoints prepared and executed with python 'requests' library.
There no any mentions in Workable API documentation about network requests limitations so the project doesnt handle network request limits.
By default, networks requests to API endpoints do not time out unless a timeout value is set explicitly.

The main data collecting and synchronizing process implemented in **/workable_client_app/management/commands/process_workable_api.py** file.
It fetches data from workable API server, extracts it and saves into database. It checks whether a DB record exists or not for avoiding duplicating data.