#!/bin/bash

# Start the PostgreSQL service
service postgresql start

# Run the Python app using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

#Two line command to execute everything 
#docker build -t etl_api .
#docker run --name etl_api -p 8000:8000 -p 5432:5432 -d etl_api

#Build and run in one line of command 
#docker run --name etl_api -p 8000:8000 -d --rm -it $(docker build -q .) 
