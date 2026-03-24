"""
PAGE OBJECT MODEL — InventoryPage (Product Listing)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    PRODUCT_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES     = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTNS   = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE         = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN      = (By.CLASS_NAME, "product_sort_container")
    CART_LINK          = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_product_names(self):
        """Returns a list of all product name strings on the page."""
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self):
        """Returns a list of prices as floats, e.g. [7.99, 15.99, ...]"""
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def add_first_item_to_cart(self):
        """Adds the first product on the page to the cart."""
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        btns[0].click()
        return self

    def add_all_items_to_cart(self):
        """Adds every visible product to the cart."""
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)
        for btn in btns:
            btn.click()
        return self

    def get_cart_count(self):
        """Returns the number shown on the cart badge (0 if empty)."""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    def sort_by(self, option_text):
        """
        Sorts products by the given option.
        option_text options: 'Name (A to Z)', 'Name (Z to A)',
                             'Price (low to high)', 'Price (high to low)'
        """
        dropdown = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        dropdown.select_by_visible_text(option_text)
        return self

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()
