# Use the official Python base image
FROM python:latest

# Print outputs to the terminal
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container
WORKDIR /app

# Copy the files over
COPY . /app

# Install PostgreSQL server and client, clean out all packages afterwards
RUN apt-get update 
RUN apt-get install -y postgresql
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*

# Install the Python app dependencies; use --no-cache to ensure clean install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables for the PostgreSQL database
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=experiment_db

# Configure PostgreSQL and give the default user, root, advanced privileges
RUN service postgresql start \
    && su - postgres -c "psql -c 'CREATE DATABASE experiment_db;' \
       && psql -c 'CREATE USER root WITH PASSWORD '\''password'\'' SUPERUSER BYPASSRLS Replication;'"

# Expose the necessary ports
EXPOSE 8000

# Give start.sh permissions to execute. Let it start postgres and python api
RUN chmod +x /app/start.sh
CMD ["./start.sh"]