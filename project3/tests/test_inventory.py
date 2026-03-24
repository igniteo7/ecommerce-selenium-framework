"""
TEST SUITE: Inventory / Product Listing
Covers: product display, sorting, add to cart, cart badge count
"""

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestInventory:

    def test_products_are_displayed(self, logged_in_driver):
        """There should be at least one product on the inventory page."""
        page = InventoryPage(logged_in_driver)
        names = page.get_product_names()
        assert len(names) > 0, "Expected products to be listed on inventory page"

    def test_sort_price_low_to_high(self, logged_in_driver):
        """
        After sorting low→high, each price should be ≤ the next.
        This catches sorting bugs — a common real-world regression.
        """
        page = InventoryPage(logged_in_driver)
        page.sort_by("Price (low to high)")
        prices = page.get_product_prices()
        assert prices == sorted(prices), f"Prices not sorted correctly: {prices}"

    def test_sort_price_high_to_low(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        page.sort_by("Price (high to low)")
        prices = page.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Prices not sorted correctly: {prices}"

    def test_sort_name_a_to_z(self, logged_in_driver):
        page = InventoryPage(logged_in_driver)
        page.sort_by("Name (A to Z)")
        names = page.get_product_names()
        assert names == sorted(names), f"Names not sorted A→Z: {names}"

    def test_add_single_item_updates_cart_badge(self, logged_in_driver):
        """Adding one item should show '1' on the cart badge."""
        page = InventoryPage(logged_in_driver)
        page.add_first_item_to_cart()
        assert page.get_cart_count() == 1, "Cart badge should show 1 after adding one item"

    def test_add_all_items_updates_cart_badge(self, logged_in_driver):
        """Adding all items should reflect the correct total on the cart badge."""
        page = InventoryPage(logged_in_driver)
        names = page.get_product_names()
        page.add_all_items_to_cart()
        assert page.get_cart_count() == len(names), (
            f"Cart badge shows {page.get_cart_count()}, expected {len(names)}"
        )

    def test_cart_contains_added_item(self, logged_in_driver):
        """The item added from inventory should appear by name in the cart."""
        inv = InventoryPage(logged_in_driver)
        product_names = inv.get_product_names()
        first_product = product_names[0]

        inv.add_first_item_to_cart()
        inv.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart_items = cart.get_item_names()
        assert first_product in cart_items, (
            f"Expected '{first_product}' in cart, found: {cart_items}"
        )
