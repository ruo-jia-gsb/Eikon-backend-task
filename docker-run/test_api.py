# Use FastAPI's test client 
from fastapi.testclient import TestClient

# Create a client for the app
from main import app
client = TestClient(app)

# Test if we get a simple response from the app, showing it started
def test_root():
    response = client.get("/")
    assert response.status_code == 202
    assert response.json() == {"message": "Hello World! This is the etl_api!"}

# Test if we can make connection to the postgres
def test_connection():
    response = client.get("/test_connection/")
    assert response.status_code == 200
    assert response.json() == {"message": "Connection Succeeded!"}

# Test the etl process and assess the accuracy of a response
def test_upload_and_accuracy():
    client.post("/etl/")
    response = client.get("/users/?return_limit=1")
    assert response.status_code == 200
    assert response.json()[0] == {
        "total_experiments_run": 2,
        "avg_experiment_run_time": 12.5,
        "most_popular_compound_names": "Compound B",
        "most_popular_compound_ids": "2",
        "most_popular_compound_structures": "C21H30O2",
        "user_id": 1,
        "email": "alice@example.com",
        "name": "Alice"
        }