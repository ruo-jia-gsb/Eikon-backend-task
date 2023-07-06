from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.types import *        

class Experiment_Stats(BaseModel):
    total_experiments_run: int
    avg_experiment_run_time: float
    most_popular_compound_names: str
    most_popular_compound_ids: str
    most_popular_compound_structures: str
    user_id: int
    email: str
    name: str

    class Config:
        orm_mode = True

class All_Facts(Experiment_Stats):
    time_created: datetime
    time_updated: datetime | None