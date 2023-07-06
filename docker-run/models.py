from sqlalchemy import Column, DateTime, Integer, Float, String
from sqlalchemy.sql import func 
import services as services

class User_Experiment_Stats(services.Base):
    __tablename__ = services.TABLE_NAME
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    total_experiments_run = Column(Integer)
    avg_experiment_run_time = Column(Float)
    most_popular_compound_ids = Column(String)
    most_popular_compound_names = Column(String)
    most_popular_compound_structures = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())