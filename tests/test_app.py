import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "participants" in data["Tennis Club"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Tennis Club"
    # Remove if already present
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    if response.status_code == 400:
        # Already signed up, remove and try again
        from src.app import activities
        activities[activity]["participants"].remove(email)
        response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    from src.app import activities
    activities[activity]["participants"].remove(email)

def test_signup_for_activity_duplicate():
    email = "alex@mergington.edu"
    activity = "Tennis Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
