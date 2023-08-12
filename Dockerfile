FROM python:3.11
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get clean && apt-get update -y
RUN apt-get install -y libzbar0
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install pyzbar
RUN pip3 install pyzbar[scripts]
RUN chmod 755 .
COPY . .