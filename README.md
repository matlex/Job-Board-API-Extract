# Job-Board-API-Extract #
This is code that extracts Job and Candidate info using the Workable API

## Prerequisites ##
* Python 3
* Virtual environment also should be created and activated with python 3 interpreter.
* You should have working database server (MySQL or PostgreSQL) with created database.


## How to run? ##
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
to JobBoard API server and obtain all Job and Candidate data and then will save it into DataBase described in **workable_api/remote.py** file.
You can write some .sh file to run that program repeatedly via crontab.

## About project settings for local or production environment ##
There is a statement in setting.py on lines 111-115 where importing additional settings. It depends on 
whether computer's name exists in HOSTS list or not. If your computer name is 'UBUNTU' then
it will import settings from local.py file. It has differences between remote.py settings. For example 
debug mode for local is on, and for remote(production) is false. Also you can use just sqlite3 database
when you're working on local project to simplify manipulating with database. All above means you can
just put your pc name to 'HOSTS' list and the application will use settings from local.py settings file.
Otherwise it will use settings from remote.py file.

Please keep in mind you have to put any other new settings in both places local.py and remote.py.

## Logging ##
There is a parameter 'DEBUG_LEVEL' in both local.py and remote.py files. It must set to be True or False.
Depending on that the main logger will save information into log files. Log files placed in 'logs' directory.
There can be two versions of log files: main.log and main_debug.log. 
It depends on DEBUG(True/False) parameter in local.py or remote.py files.