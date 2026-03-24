import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(scope="function")
def driver():
    """
    Sets up a Chrome WebDriver before each test and tears it down after.
    scope="function" means a fresh browser is created for every test.
    """
    options = Options()
    options.add_argument("--headless")          # Run without opening a browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Wait up to 10s for elements to appear before failing

    yield driver  # Hand the driver to the test

    driver.quit()  # Always runs after the test, even if it fails


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Reusable fixture: gives you a driver that's already logged in.
    Tests that need authentication use this instead of 'driver'.
    """
    driver.get(BASE_URL)
    driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()
    yield driver
