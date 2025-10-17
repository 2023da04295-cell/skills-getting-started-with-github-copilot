def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure known activity present
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    # Use a test email
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already signed up
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    result = resp.json()
    assert "Signed up" in result["message"]

    # Verify participant present
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    result = resp.json()
    assert "Unregistered" in result["message"]

    # Verify participant removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]


def test_unregister_nonexistent_participant(client):
    email = "nonexistent@mergington.edu"
    activity = "Programming Class"

    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
    data = resp.json()
    assert data["detail"] == "Participant not found in activity"


def test_signup_already_signed(client):
    # Use an email already in the activity
    activity = "Chess Club"
    existing = "michael@mergington.edu"
    resp = client.post(f"/activities/{activity}/signup?email={existing}")
    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "Student already signed up for this activity"
