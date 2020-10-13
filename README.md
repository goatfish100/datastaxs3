# README #
mainapp is a python flask application with S3 operations per Datastax 
interview test app.

This project uses Flask http://flask.pocoo.org/ and python 3+ with pip and a virtualenv to run.

To set up and run - create and initialize a python 3+ with virtualenv and run 

In the Virtual Env - install the required libraries with command
pip install -r ./requirements


Fallowing standard microservice standards - this project uses a ".env" file to get it's
variables needed to create.  Since the ".env" file contains sensitive information like
database password - it is NOT checked in and needs to be created.

#Information needed in dot env ".env" file
This program uses a "dotenv" ".env" for configuration settings.  This
file IS NOT checked into source control.  to run this program - either
the environmental variables need to be set OR a correct .env file is in main
dir.  
#Sample .env file
AWS_ACCESS_KEY= # AWS Key
AWS_SECRET=  # AWS secret
AWS_BUCKET=  # bucket
HTTP_PORT=   # PORT for App to run on

#Running app - dev and test.
python3 mainapp.py


#Running app - .
If you wish to run this app in a production setting - please use
a wsgi server like gunicorn or Gevent.  This is not described at
this point in time.



