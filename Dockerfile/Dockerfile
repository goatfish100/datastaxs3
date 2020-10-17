FROM python:3.9.0-alpine
WORKDIR /usr/src/python

RUN apk add --update git
RUN apk add --update openssh-client


RUN git clone --depth 1 https://gitlab.com/goatfish100/datastaxs3.git /usr/src/python


RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "mainapp.py" ]
