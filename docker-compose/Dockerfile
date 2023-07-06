# Use the official Python base image
FROM python:3

# Allow the python code to print to environment
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container
WORKDIR /app

# Copy the files over
COPY . /app

# Install the Python app dependencies; use --no-cache to ensure clean install
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the local port 
EXPOSE 8000