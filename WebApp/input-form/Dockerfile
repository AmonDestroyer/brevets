FROM python:3
MAINTAINER Adam Case "acase@uoregon.edu"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential python3-arrow
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
