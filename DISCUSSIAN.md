# NOTES - Discussian points #
This exercise is almost perfect for AWS Lambda and in production - this would make most sense
I initially started with this approach using the "Serverless" - framework (Lambda - multicloud)
however I ran into libraries issues.

From there - I did a regular GoLang version - with no frameworks and after some work - I became
unhappy with minio S3 library.  I ran into issues with resource availeable and it appeared to be
newer version issue.  I circled back later out of curiosity and got past this.

At this point - I switched to Python and Flask - since the Boto3 library is excellent.  However
I realized that I know Python the least well - and unit testing doing mocking on python is a weak 
point for me.

I'm a general advocate of using Libraries when they are good as they are usually more expediant.
However in this case - doing things over - I would have direct calls to Amazon.  This would make testing
easier and allow for Lambda.

This project uses Flask http://flask.pocoo.org/ and python 3+ with pip and a virtualenv to run.

To set up and run - create and initialize a python 3+ with virtualenv and run the two commands
"""""""""""""""""""""""""""""""""""
:~$virtualenv venv --python=python3
:~$source ./venv/bin/activate
"""""""""""""""""""""""""""""""""""

You will likely see (venv) at start of cursor
"""""""""""""""""""""""""""""""""""
(venv) jamesl@james-latitude7370:~/python/datastaxs3$
"""""""""""""""""""""""""""""""""""

In the Virtual Env - install the required libraries with command
"""""""""""""""""""""""""""""""""""
(venv) $pip install -r ./requirements
"""""""""""""""""""""""""""""""""""


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