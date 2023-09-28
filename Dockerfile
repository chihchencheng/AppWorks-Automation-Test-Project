# install python
FROM ubuntu:22.04

WORKDIR /app

RUN apt update && apt upgrade -y \
	&& apt-get install -y wget \
  	&& rm -rf /var/lib/apt/lists/* \
	&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	&& apt-get install -f ./google-chrome-stable_current_amd64.deb 
	# && apt-get install -y chromium-browser -y\
	# && apt install build-essential checkinstall -y

	# && wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chrome-linux64.zip\
	
RUN apt install python3.11 -y \
	&& apt-get -y install python3-pip



COPY . .

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt


ENV ENV_FILE /app/.env


# CMD ["pytest", "test_web/test_web_login.py"]

# Use an official Python runtime as the base image
# FROM python:3.11.5-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the entire project directory into the container
# COPY . /app

# # Install any system-level dependencies if needed
# # For example, if your project requires additional system packages:
# # RUN apt-get update && apt-get install -y <package-name>

# # Set the ENV_FILE environment variable to the path of the desired .env file
# ENV ENV_FILE /app/.env

# # Install Python dependencies from requirements.txt
# RUN pip install -r requirements.txt

# # Define the command to run when the container starts
CMD ["pytest", "test_web/test_web_login.py"]
# CMD python3 



