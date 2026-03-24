"""
TEST SUITE: Login Flows
Covers: valid login, locked user, invalid credentials, empty fields (data-driven from CSV)
"""

import csv
import os
import pytest
from pages.login_page import LoginPage


# ── Helper to load CSV test data ──────────────────────────────────────────────
def load_users():
    """Reads data/users.csv and returns a list of (username, password, expected) tuples."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")
    users = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append((row["username"], row["password"], row["expected_result"]))
    return users


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestLogin:

    def test_valid_login(self, driver):
        """Happy path: standard_user should reach the inventory page."""
        page = LoginPage(driver).open()
        page.login("standard_user", "secret_sauce")
        assert page.is_logged_in(), "Expected to land on /inventory after valid login"

    def test_locked_out_user(self, driver):
        """Locked users should see an error message, not reach inventory."""
        page = LoginPage(driver).open()
        page.login("locked_out_user", "secret_sauce")
        error = page.get_error_message()
        assert error is not None, "Expected an error message for locked user"
        assert "locked out" in error.lower()

    def test_invalid_credentials(self, driver):
        """Wrong username/password should return a credentials error."""
        page = LoginPage(driver).open()
        page.login("wrong_user", "wrong_pass")
        error = page.get_error_message()
        assert error is not None
        assert "username and password do not match" in error.lower()

    def test_empty_username(self, driver):
        """Submitting with no username should prompt for username."""
        page = LoginPage(driver).open()
        page.login("", "secret_sauce")
        error = page.get_error_message()
        assert error is not None
        assert "username is required" in error.lower()

    def test_empty_password(self, driver):
        """Submitting with no password should prompt for password."""
        page = LoginPage(driver).open()
        page.login("standard_user", "")
        error = page.get_error_message()
        assert error is not None
        assert "password is required" in error.lower()

    @pytest.mark.parametrize("username,password,expected", load_users())
    def test_login_data_driven(self, driver, username, password, expected):
        """
        Data-driven test: runs once per row in data/users.csv.
        This is how real automation frameworks handle multiple test scenarios
        without duplicating test code.
        """
        page = LoginPage(driver).open()
        page.login(username, password)

        if expected == "success":
            assert page.is_logged_in(), f"Expected successful login for '{username}'"
        else:
            error = page.get_error_message()
            assert error is not None, f"Expected error for '{username}' but got none"
