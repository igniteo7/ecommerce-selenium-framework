"""
PAGE OBJECT MODEL (POM) — LoginPage

Why POM?
  Instead of writing driver.find_element(...) scattered across every test,
  we group all locators and actions for a page into one class.
  If the UI changes, you update ONE place, not 20 tests.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # --- Locators (CSS selectors are faster and more readable than XPath) ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://www.saucedemo.com")
        return self

    def enter_username(self, username):
        field = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)
        return self  # Return self allows method chaining: page.enter_username().enter_password()

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self

    def login(self, username, password):
        """Convenience method: does all steps in one call."""
        return self.enter_username(username).enter_password(password).click_login()

    def get_error_message(self):
        """Returns the error text if login fails, otherwise returns None."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except Exception:
            return None

    def is_logged_in(self):
        """Check we've landed on the inventory page after login."""
        return "/inventory" in self.driver.current_url
