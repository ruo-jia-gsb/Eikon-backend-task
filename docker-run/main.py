# Migrate the tables first 
import migrate_tables

# Get functions to form connections to postgres 
import services as database

# Get the etl tools 
import etl, pandas as pd 

# Get sqlalchemy tools, along with type checking 
from sqlalchemy import orm, text
from schemas import Experiment_Stats 
from typing import TYPE_CHECKING, List
from models import User_Experiment_Stats

# Now load fastapi library and initialize it 
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

# Simple dummy root function to see if api is even uploaded
@app.get("/", status_code = status.HTTP_202_ACCEPTED)
async def root():
    return {"message": "Hello World! This is the etl_api!"}


# See if the tables have migrated and connection is made
@app.get("/test_connection/", status_code=status.HTTP_200_OK, response_model = dict)
async def test_connection(db: orm.Session = Depends(database.get_db)):

    try:        
        rslt = db.execute(text(f"SELECT * FROM {database.TABLE_NAME}")).fetchall()
        return {"message": f"Connection Succeeded!"}
    except:
        return {"message": "Connection Failed..."}


# ETL to place data into the user_experiment_stats table 
@app.post("/etl/", status_code=status.HTTP_201_CREATED, response_model = dict)
async def etl(csv_data: pd.DataFrame = Depends(etl.generate_data_features), connection: orm.Session = Depends(database.get_connection)):

    # Attempt a data upload via Pandas's to_sql procedure
    try:
        csv_data.to_sql(
            name= database.TABLE_NAME,
            con=connection,
            if_exists="replace",
            chunksize=10_000, #Optimal speed for medium sized loads
            index=False
            )
        return {"message": "Upload Successful!"}
    
    # Flag for lack of a connection...
    except:
#        return {"message": "Unable to upload data..."}
        raise HTTPException(status_code=503, detail=f"Bad connection and/or Unable to upload data...")

# Return the data as a test 
@app.get('/users/', status_code=status.HTTP_200_OK, response_model = List[Experiment_Stats] | dict)
async def get_everything(return_limit: int = 3, db: orm.Session = Depends(database.get_db)):

    # Pull everything, if non-null then map results to Experiment_Stats schema. Otherwise return message 
    try:
        user_stats = db.query(User_Experiment_Stats)

        if user_stats.first():
            return list(map(Experiment_Stats.from_orm, user_stats.limit(min(return_limit, 10)).all()))
        return {'message': 'Nothing found in table!'}
    
    # Flag for lack of a connection...
    except:
#        return {'message': 'Unable to query table...'}
        raise HTTPException(status_code=503, detail=f"Bad connection and/or Unable to query table...") 