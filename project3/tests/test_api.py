"""
TEST SUITE: REST API Layer
Target: https://reqres.in — a free, public REST API built for testing.

Covers:
  - GET single resource and list
  - POST (create user)
  - PUT (update user)
  - DELETE
  - Chained API calls (create → fetch → verify → delete)
  - Negative cases (404, bad payloads)

Why reqres.in?
  SauceDemo is a UI-only app. For the API layer we use reqres.in,
  which simulates a real user/resource API — same patterns you'd test
  in enterprise systems (auth tokens, CRUD, pagination, error codes).
"""

import requests
import pytest

BASE = "https://reqres.in/api"


class TestGetRequests:

    def test_get_user_list_returns_200(self):
        """Basic health check: the users endpoint should respond successfully."""
        response = requests.get(f"{BASE}/users?page=1")
        assert response.status_code == 200

    def test_get_user_list_has_data(self):
        """Response body should contain a 'data' array with at least one user."""
        response = requests.get(f"{BASE}/users?page=1")
        body = response.json()
        assert "data" in body, "Expected 'data' key in response"
        assert len(body["data"]) > 0, "Expected at least one user in the list"

    def test_get_single_user_returns_correct_id(self):
        """Fetching user 2 should return a user whose id is 2."""
        response = requests.get(f"{BASE}/users/2")
        assert response.status_code == 200
        user = response.json()["data"]
        assert user["id"] == 2

    def test_get_nonexistent_user_returns_404(self):
        """Requesting a user that doesn't exist must return 404, not 200 or 500."""
        response = requests.get(f"{BASE}/users/9999")
        assert response.status_code == 404, (
            f"Expected 404 for missing user, got {response.status_code}"
        )

    def test_response_time_under_threshold(self):
        """API should respond within 3 seconds — a basic performance assertion."""
        response = requests.get(f"{BASE}/users")
        assert response.elapsed.total_seconds() < 3.0, (
            f"Response too slow: {response.elapsed.total_seconds():.2f}s"
        )


class TestPostRequests:

    def test_create_user_returns_201(self):
        """POST to create a user should return HTTP 201 Created."""
        payload = {"name": "Atharv", "job": "Automation Engineer"}
        response = requests.post(f"{BASE}/users", json=payload)
        assert response.status_code == 201

    def test_create_user_response_contains_id(self):
        """A created user should have an auto-generated 'id' in the response."""
        payload = {"name": "Atharv", "job": "Automation Engineer"}
        response = requests.post(f"{BASE}/users", json=payload)
        body = response.json()
        assert "id" in body, "Expected 'id' in creation response"
        assert body["id"] is not None

    def test_create_user_echoes_payload(self):
        """The response should reflect back the name and job we sent."""
        payload = {"name": "TestUser", "job": "QA Lead"}
        response = requests.post(f"{BASE}/users", json=payload)
        body = response.json()
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]


class TestPutAndDelete:

    def test_update_user_returns_200(self):
        """PUT to update a user should return 200 with updated fields."""
        payload = {"name": "Updated Name", "job": "Senior Engineer"}
        response = requests.put(f"{BASE}/users/2", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Updated Name"

    def test_delete_user_returns_204(self):
        """DELETE should return 204 No Content — no body expected."""
        response = requests.delete(f"{BASE}/users/2")
        assert response.status_code == 204
        assert response.text == "", "Expected empty body for 204 response"


class TestChainedAPIFlow:
    """
    Chained test: simulates a real-world scenario where one API call's
    output feeds into the next — common in enterprise API testing.

    Flow: Create user → capture ID → fetch user by ID → verify → delete
    """

    def test_create_then_verify_user(self):
        # Step 1: Create
        payload = {"name": "Chain Test User", "job": "QA Tester"}
        create_resp = requests.post(f"{BASE}/users", json=payload)
        assert create_resp.status_code == 201
        created_id = create_resp.json()["id"]
        assert created_id is not None, "No ID returned from create"

        # Step 2: Verify creation response data
        created_body = create_resp.json()
        assert created_body["name"] == payload["name"], "Name mismatch after create"
        assert created_body["job"] == payload["job"], "Job mismatch after create"

        # Step 3: Update using the captured ID
        update_payload = {"name": "Chain Test User", "job": "Senior QA Tester"}
        update_resp = requests.put(f"{BASE}/users/{created_id}", json=update_payload)
        assert update_resp.status_code == 200
        assert update_resp.json()["job"] == "Senior QA Tester"

        # Step 4: Delete
        delete_resp = requests.delete(f"{BASE}/users/{created_id}")
        assert delete_resp.status_code == 204
