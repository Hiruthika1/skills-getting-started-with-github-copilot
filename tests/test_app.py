import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test listing activities
def test_list_activities():
    # Arrange: Test client is ready
    # Act: Request the activities endpoint
    response = client.get("/activities")
    # Assert: Response is OK and contains activities
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

# Arrange-Act-Assert: Test signup for activity
def test_signup_for_activity():
    # Arrange: Pick an activity and email
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act: Sign up for the activity
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert: Response is OK and confirms signup
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

# Arrange-Act-Assert: Prevent duplicate signup
def test_prevent_duplicate_signup():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "dupeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

# Arrange-Act-Assert: Test unregister participant
def test_unregister_participant():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

# Arrange-Act-Assert: Test invalid activity name
def test_invalid_activity():
    response = client.post("/activities/invalid_activity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
