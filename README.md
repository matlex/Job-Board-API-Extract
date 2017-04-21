# Job-Board-API-Extract #
This is code that extracts Job and Candidate info using the Workable API

## Prerequisites ##
You should have working database server (MySQL or PostgreSQL) with created database.


## How to run? ##
1. Create a clean virtual environment and activate it.
2. Install MySQLdb Client to a system. 
Run: **sudo apt-get install python-dev libmysqlclient-dev**
3. Run: **sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev**
4. Go to main application's directory and run **pip install -r requirements.txt**
5. Generate a new secret key for Django project - http://www.miniwebtool.com/django-secret-key-generator/
6. Go to the 'secrets' directory and rename "secrets_template.py" file to "secrets.py" file and fill in ALL constants properly.
7. Now we need create new database migrations. 
First run: python manage.py makemigrations to create migrations for django internal apps. 
Then you need to create migrations for every app. 
At the moment run: **python manage.py makemigrations workable_api**
8. Then apply newly created migrations: **python manage.py migrate**
9. Create a Django admin by running command: **python manage.py createsuperuser**
10. Launch application django-admin panel by running command **python manage.py runserver 0.0.0.0:8000**
11. Open **http://your_server_address:8000/admin** and try to enter to django-admin panel.
12. To start collecting data and save them into DB Run: **python manage.py process_workable_api** command. It will connect
to JobBoard API server and obtain all Job and Candidate data and then will save it into DataBase described in **workable_api/remote.py** file.
You can write some .sh file to run that program repeatedly via crontab.