"""
PAGE OBJECT MODEL — CartPage
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    CART_ITEMS      = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BUTTONS  = (By.CSS_SELECTOR, "[data-test^='remove']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_item_names(self):
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_first_item(self):
        btns = self.driver.find_elements(*self.REMOVE_BUTTONS)
        if btns:
            btns[0].click()
        return self

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()
