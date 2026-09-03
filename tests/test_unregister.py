def test_unregister_participant_from_activity(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in response.json()["participants"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants/not-found@mergington.edu")

    assert response.status_code == 404
