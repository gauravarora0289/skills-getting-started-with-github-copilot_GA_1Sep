def test_unregister_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in response.json()["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_path = "/activities/Chess Club/participants/not-found@mergington.edu"

    # Act
    response = client.delete(activity_path)

    # Assert
    assert response.status_code == 404
