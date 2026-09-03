def test_root_redirects_to_static_index(client):
    # Arrange
    redirect_path = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)
    static_response = client.get(redirect_path)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == redirect_path
    assert static_response.status_code == 200


def test_get_activities_returns_activity_details(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )
    assert activities["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities_response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities_response.json()[activity_name]["participants"].count(email) == 1


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_path = "/activities/Unknown Club/signup"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        activity_path,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_422(client):
    # Arrange
    activity_path = "/activities/Chess Club/signup"

    # Act
    response = client.post(activity_path)

    # Assert
    assert response.status_code == 422
