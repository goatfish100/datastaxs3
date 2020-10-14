# README #
mainapp is a python flask application with S3 operations per Datastax 
interview test app.

This project uses Flask http://flask.pocoo.org/ and python 3+ with pip and a virtualenv to run.

To set up and run - create and initialize a python 3+ with virtualenv and run the two commands  
"""""""""""""""""""""""""""""""""""\
:~$virtualenv venv --python=python3\
:~$source ./venv/bin/activate\
"""""""""""""""""""""""""""""""""""  

You will likely see (venv) at start of cursor\
"""""""""""""""""""""""""""""""""""\
(venv) jamesl@james-latitude7370:~/python/datastaxs3\
"""""""""""""""""""""""""""""""""""  

In the Virtual Env - install the required libraries with command\
"""""""""""""""""""""""""""""""""""\
(venv) $pip install -r ./requirements\
"""""""""""""""""""""""""""""""""""  

Fallowing standard microservice standards - this project uses a ".env" file to get it's
variables needed to create.  Since the ".env" file contains sensitive information like
database password - it is NOT checked in and needs to be created.

#Information needed in dot env ".env" file
This program uses a "dotenv" ".env" for configuration settings.  This
file IS NOT checked into source control.  to run this program - either
the environmental variables need to be set OR a correct .env file is in main
dir.  Alternatively environmental variables for could be set for the items below.
#Sample .env file
AWS_ACCESS_KEY= # AWS Key  
AWS_SECRET=  # AWS secret  
AWS_BUCKET=  # bucket  


#Running app - dev and test.\
"""""""""""""""""""""""""""""""""""\
(venv) $python3 mainapp.py\
"""""""""""""""""""""""""""""""""""\


#Running app - .
If you wish to run this app in a production setting - please use
a wsgi server like gunicorn or Gevent.  This is not described at
this point in time.

# Helper Script curlopt.sh
curlopt.sh is a bash script to run/test and create curl requests\
"""""""""""""""""""""""""""""""""""\
(venv) $bash curlopt.sh\
"""""""""""""""""""""""""""""""""""\

### Request

`POST /s3post/filename`

curl -v -X post localhost:5000/s3post/hello   

### Response

    HTTP 1.0, assume close after body
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 186
    Server: Werkzeug/1.0.1 Python/3.7.3
    Date: Wed, 14 Oct 2020 19:03:27 GMT
 
    {
    "posturl": "https://goatfish100.s3.amazonaws.com/helloc3cb?AWSAccessKeyId=AKIAW3MYQE35N27V2XXT&Signature=A1gPR9p5i7KgqjxGqB0j3yFd9D8%3D&Expires=1602709407", 
    "uuid": "helloc3cb"
    }

### Request

`POST /s3post/filename`

curl -v -X post localhost:5000/s3post/hello   

### Response

    HTTP 1.0, assume close after body
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 186
    Server: Werkzeug/1.0.1 Python/3.7.3
    Date: Wed, 14 Oct 2020 19:03:27 GMT
 
    {
    "posturl": "https://goatfish100.s3.amazonaws.com/helloc3cb?AWSAccessKeyId=AKIAW3MYQE35N27V2XXT&Signature=A1gPR9p5i7KgqjxGqB0j3yFd9D8%3D&Expires=1602709407", 
    "uuid": "helloc3cb"
    }

### Request

`POST /s3check/resourcename`
### Response

    HTTP 1.0, assume close after body
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 24
    Server: Werkzeug/1.0.1 Python/3.7.3
    Date: Wed, 14 Oct 2020 19:11:18 GMT
    
    {
    "exists": "False"
    }

### Request

`PUT /s3geturl/resourcename`

### Response
    put /s3geturl/jltest HTTP/1.1
    Host: localhost:5000
    User-Agent: curl/7.64.0
    Accept: */*

    HTTP 1.0, assume close after body
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 159
    Server: Werkzeug/1.0.1 Python/3.7.3
    Date: Wed, 14 Oct 2020 19:17:02 GMT

    {
    "url": "https://goatfish100.s3.amazonaws.com/jltest?AWSAccessKeyId=AKIAW3MYQE35N27V2XXT&Signature=S%2F%2F8BVK4Nh9LJGv1W7vcFLcyyHw%3D&Expires=1602706622"
    }
