#Base Image
FROM python:3.7.2-slim

# Install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# add app
COPY src/ /usr/src/app
# set working directory
WORKDIR /usr/src/app

# add and install requirements
RUN pip install -r requirements.txt

# run server
CMD flask run -h 0.0.0.0