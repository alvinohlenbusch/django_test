## Install

	$ sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx
	$ sudo pip install virtualenv
	
## Database setup

	$ sudo service postgresql start
	$ sudo su - postgres
	$ psql
	$ CREATE DATABASE myproject;
	$ CREATE USER myprojectuser WITH PASSWORD 'password';
	$ GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
	$ \q
	$ exit
	
## Virtual environment
	
	$ cd ./myproject
	$ virtualenv myprojectenv
	$ source myprojectenv/bin/activate
	$
	$ pip install django gunicorn psycopg2
	$
	$ python manage.py makemigrations
	$ python manage.py migrate
	$ python manage.py createsuperuser
	$ python manage.py collectstatic
	$
	$ gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
	$ 

## Usage

	$ http://localhost:8000/api/notes/
	
	
	
	
	