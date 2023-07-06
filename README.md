# Eikon-backend-task

There are two folders for the backend task, that have use different infrastructures:

  1. docker-run: This deploys the postgres server, python-api within a single container as a monolith. Testing can be done by entering the container as a bash
     and using ***python -m pytest***. Three tests were created which check for deployment, connection, and finally ETL and accuracy. 
     
  3. docker-compose: This deploys the postgres server, python-api, and also creates pgadmin to inspect the database, as a set of microservices. No testing file
     was created for docker-compose as it wasn't part of the original request. 

The advantage of docker-run is that everything is in one environment. It's disadvantage is that it allows for less dynamic updating and exploration of changes. 

The advantage of docker-compose is that it will scale better as other services are included. It's disadvantage is the potential for a higher burden on resources 
in order to manage these disparate services.

# Deploying docker-run

To deploy **docker-run**, use the following command in terminal within the folder that the docker-run's files have been placed in:

    docker run --name etl_api -p 8000:8000 -d --rm -it $(docker build -q .)

You can type the following address into a web browser to explore the core functions of the API in a GUI setting:

    http://127.0.0.1:8000/docs

Incidentally, if you want to perform the ETL of the data files through CURL use the following in a terminal:

    curl -X 'POST' 'http://127.0.0.1:8000/etl/' -H 'accept: application/json' -d ''

# Deploying docker-compose

To deploy **docker-compose**, use the following command in terminal within the folder that the docker-run's files have been placed in:

    docker-compose up

Like **docker-run**, typing the following address into a web browser allows you to explore the core functions of the API through a GUI:

    http://127.0.0.1:8000/docs

Likewise, performing the ETL of the data files via CURL is also just:

    curl -X 'POST' 'http://127.0.0.1:8000/etl/' -H 'accept: application/json' -d ''

# Unit tests of docker-run

To perform the unit-tests for **docker-run** enter its container after it has been deployed with the following command in terminal:

    docker exec -it etl_api bash

Once in, type in the following:

    python -m pytest

It will deploy 3 unit tests, which check that the API is up, the connection to the postgresdb is made, and that ETL was executed and a sample result was accurate.
The file ***test_api.py*** has these tests. The specific sample result it is looking for is for user 1, aka Alice, who is the only person who has run two experiments 
and the compound she has used the most is Compound B. 

# Required libraries

The main libraries used to build these APIs (also in the requirements.txt) are:

fastapi==0.97.0

httpx==0.24.1

pandas==2.0.2

psycopg2-binary==2.9.6

pydantic==1.10.9

pytest==7.4.0

python-dateutil==2.8.2

python-dotenv==1.0.0

SQLAlchemy==2.0.16

uvicorn==0.22.0

