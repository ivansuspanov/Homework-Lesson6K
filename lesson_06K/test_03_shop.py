import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()


def test_shop_checkout(driver):
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.saucedemo.com/")

    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    username_input.send_keys("standard_user")

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("secret_sauce")

    login_btn = driver.find_element(By.ID, "login-button")
    login_btn.click()

    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]

    for item_name in items_to_add:
        item_locator = (
            By.XPATH,
            f"//div[contains(@class, 'inventory_item') "
            f"and .//div[text()='{item_name}']]"
        )
        item_card = wait.until(EC.element_to_be_clickable(item_locator))

        add_btn_locator = (By.XPATH, ".//button[text()='Add to cart']")
        add_btn = item_card.find_element(*add_btn_locator)
        add_btn.click()

        remove_btn_locator = (By.XPATH, ".//button[text()='Remove']")
        wait.until(EC.element_to_be_clickable(remove_btn_locator))

    cart_link = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".shopping_cart_container a"))
    )
    cart_link.click()

    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkout_button"))
    )
    checkout_btn.click()

    first_name = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )
    first_name.send_keys("Иван")

    last_name = driver.find_element(By.ID, "last-name")
    last_name.send_keys("Шушпанов")

    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.send_keys("612990")

    continue_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "continue"))
    )
    continue_btn.click()

    total_element = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".summary_total_label"))
    )
    total_text = total_element.text

    expected_total = "Total: $58.29"
    assert total_text == expected_total, (
        f"Ожидалось '{expected_total}', но получено: '{total_text}'"
    )
