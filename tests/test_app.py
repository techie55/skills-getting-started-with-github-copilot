from fastapi.testclient import TestClient
from src import app

client = TestClient(app.app)


class TestGetActivities:
    def test_get_activities_returns_all_activities(self):
        # Arrange / Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data


class TestSignup:
    def test_signup_new_participant_success(self):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_duplicate_participant_fails(self):
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_not_found(self):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRemoveParticipant:
    def test_remove_participant_success(self):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"

    def test_remove_nonexistent_activity_not_found(self):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant_not_found(self):
        # Arrange
        activity_name = "Chess Club"
        email = "notmember@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
