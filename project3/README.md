# E-Commerce UI & API Test Automation Framework

A data-driven test automation framework built with **Python**, **Selenium**, and **Pytest** targeting a real e-commerce web application. Demonstrates the Page Object Model pattern, dynamic locator strategies, REST API testing with chained calls, and HTML report generation.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| Selenium 4 | UI browser automation |
| Pytest | Test runner & fixtures |
| pytest-html | HTML report generation |
| Requests | REST API testing |
| webdriver-manager | Auto-manages ChromeDriver |

---

## Project Structure

```
project3/
├── pages/                  # Page Object Model classes
│   ├── login_page.py       # Login page locators & actions
│   ├── inventory_page.py   # Product listing page
│   └── cart_page.py        # Cart page
├── tests/
│   ├── test_login.py       # Login flows (valid, invalid, data-driven)
│   ├── test_inventory.py   # Product listing, sorting, add-to-cart
│   └── test_api.py         # REST API tests with chained calls
├── data/
│   └── users.csv           # CSV-driven test data for login scenarios
├── reports/                # Auto-generated HTML reports (gitignored)
├── conftest.py             # Shared pytest fixtures (driver setup/teardown)
├── pytest.ini              # Pytest configuration
└── requirements.txt
```

---

## Key Concepts Demonstrated

### Page Object Model (POM)
All locators and page interactions are encapsulated in dedicated classes under `pages/`. If the UI changes, only the relevant page class needs updating — not every test.

```python
# Clean test code — no locators here
def test_valid_login(self, driver):
    page = LoginPage(driver).open()
    page.login("standard_user", "secret_sauce")
    assert page.is_logged_in()
```

### Dynamic Locator Strategy
Uses CSS selectors and explicit waits (`WebDriverWait`) to handle asynchronous page loads and dynamic elements reliably.

### Data-Driven Testing
Login scenarios are driven from `data/users.csv` — adding a new test case requires only a new CSV row, no code change.

```python
@pytest.mark.parametrize("username,password,expected", load_users())
def test_login_data_driven(self, driver, username, password, expected):
    ...
```

### Chained API Testing
The `test_api.py` suite demonstrates create → verify → update → delete flows where each step consumes the output of the previous call — mirroring real enterprise API test patterns.

```python
# Create → capture ID → update with that ID → delete
create_resp = requests.post(f"{BASE}/users", json=payload)
created_id = create_resp.json()["id"]
update_resp = requests.put(f"{BASE}/users/{created_id}", json=update_payload)
delete_resp = requests.delete(f"{BASE}/users/{created_id}")
```

---

## Setup & Run

```bash
# 1. Clone and enter the project
git clone https://github.com/YOUR_USERNAME/ecommerce-selenium-framework
cd ecommerce-selenium-framework

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests (generates HTML report in reports/)
pytest

# 5. Run only UI tests
pytest tests/test_login.py tests/test_inventory.py

# 6. Run only API tests
pytest tests/test_api.py

# 7. Run a specific test by name
pytest -k "test_valid_login"
```

---

## Test Report

After running pytest, open `reports/report.html` in a browser to see a full test execution report with pass/fail status, durations, and failure details.

---

## CI/CD

This project includes a GitHub Actions workflow (`.github/workflows/tests.yml`) that automatically runs the full test suite on every push and pull request.
