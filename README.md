# README #
cdr is a python flask application for the cdr recording web service.

This project uses Flask http://flask.pocoo.org/ and python 3+ with pip and a virtualenv to run.

To set up and run - create and initialize a python 3+ with virtualenv and run 

In the Virtual Env - install the required libraries with command
pip install -r ./pip_libs.txt


Fallowing standard microservice standards - this project uses a ".env" file to get it's
variables needed to create.  Since the ".env" file contains sensitive information like
database password - it is NOT checked in and needs to be created.

#Information needed in dot env ".env" file
HTTP_PORT=<YOUR_HTTP_PORT>
DB_CONN=<DB_CONN_STRING>

#Sample .env file
HTTP_PORT="8000"
DB_CONN="host=localhost dbname=databasename user=postgresuser password=password"

#Running to run - type the following.
python application.py

Note:
Gevent is currently set as production wsgi server - unless the env DEVELOPMENT is set to "dev" explicity.

It's possible to run in gunicorn as well - benefits/conns aren't fully understood. It is
believed that gevent is newer/faster and gunicorn is older and more mature.

To Run - gunicorn - run with the following options - note - number of
workers/ip/port are all set as gunicorn command line options
gunicorn --log-level debug -w 2 -b 127.0.0.1:4009 application_gunicorn:app

