from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.types import *

class Experiment_Stats(BaseModel):
    total_experiments_run: int
    avg_experiment_run_time: float
    most_popular_compound_names: str
    most_popular_compound_ids: str
    most_popular_compound_structures: str

    class Config:
        orm_mode = True

class Stats_by_ID(Experiment_Stats):
    user_id: int

class Stats_by_EMAIL(Experiment_Stats):
    email: str

class Stats_by_NAME(Experiment_Stats):
    name: str

class Upload_Payload(Experiment_Stats):
    user_id: int
    email: str
    name: str
#    time_created: datetime | None
#    time_updated: datetime | None

class Entire_Payload(Experiment_Stats):
    user_id: int
    email: str
    name: str
    time_created: datetime
    time_updated: datetime | None