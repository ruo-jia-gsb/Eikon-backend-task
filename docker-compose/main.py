# Set up API essential libraries 
import services
import etl, pandas, os
from sqlalchemy import orm, text
from schemas import Entire_Payload 
from typing import TYPE_CHECKING, List
from models import User_Experiment_Stats
from datetime import datetime as dt 

from fastapi import FastAPI, Depends, HTTPException, status
app = FastAPI()

TABLE_NAME = User_Experiment_Stats.__tablename__

# Check if the the tables have migrated and connection has been made
@app.get("/connect/", response_model = dict)
async def connect(db: orm.Session = Depends(services.get_db)):

    try:
        rslt = db.execute(text(f"SELECT * FROM {TABLE_NAME}")).fetchall()
        return {"message": f"Connection Succeeded, {rslt}"}
    except:
        return {"message": "Connection Failed..."}

# ETL to place the processed CSVs into the postgres table     
@app.post("/etl/", status_code=status.HTTP_202_ACCEPTED, response_model = dict)
async def etl(csv_data: pandas.DataFrame = Depends(etl.generate_data_features), connection: orm.Session = Depends(services.get_connection)):
    try:
        csv_data.to_sql(
            name=TABLE_NAME,
            con=connection,
            if_exists="replace",
            chunksize=10_000, #Optimal speed for medium sized loads
            index=False
            )
        return {"message": f"Upload Successful!"}
    except:
        return {"message": "Unable to upload data..."}
#        raise HTTPException(status_code=500, detail=f"Unable to upload data...")

# Delete all the rows in the postgres table 
@app.delete("/remove/", response_model = dict)
async def remove_everything(db: orm.Session = Depends(services.get_db)):

    try:
        user_stats = db.query(User_Experiment_Stats)

        if user_stats.first():
            print('Found Entries')
            for user in user_stats.all():
                db.delete(user)
                db.commit()
        return {"message": f"All entries removed!"} 
    except:
        return {"message": f"Unable to remove entries..."}

# Return the data that has been uploaded if it exists
@app.get('/users/', status_code=status.HTTP_202_ACCEPTED, response_model = List[Entire_Payload] | dict)
async def get_everything(return_limit: int = 5, db: orm.Session = Depends(services.get_db)):
    try:
        user_stats = db.query(User_Experiment_Stats)

        if user_stats.first():
            return list(map(Entire_Payload.from_orm, user_stats.limit(min(return_limit, 10)).all()))
        return {'message': 'Nothing found in table!'}
    except:
        return {'message': 'Unable to query table...'}