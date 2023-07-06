import services, models

def create_table():
    return services.Base.metadata.create_all(bind=services.engine)

create_table()
