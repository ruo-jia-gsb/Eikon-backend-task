import psycopg2, services, models, os

def create_tables():
    return services.Base.metadata.create_all(bind=services.engine)

create_tables()

