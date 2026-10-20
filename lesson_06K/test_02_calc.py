import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_slow_calculator(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    driver.get(url)

    wait = WebDriverWait(driver, 120)

    delay_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#delay"))
    )
    delay_input.clear()
    delay_input.send_keys("45")

    buttons_to_click = [
        "//span[contains(@class, 'btn-outline-primary') and text()='7']",
        "//span[contains(@class, 'operator') and text()='+']",
        "//span[contains(@class, 'btn-outline-primary') and text()='8']",
        "//span[contains(@class, 'btn-outline-warning') and text()='=']",
    ]

    for xpath in buttons_to_click:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()

    wait.until(
        lambda d: d.find_element(
            By.CSS_SELECTOR, "div.screen").text.strip() == "15"
    )

    result_element = driver.find_element(By.CSS_SELECTOR, "div.screen")
    final_text = result_element.text.strip()

    assert final_text == "15", (
        f"Ожидалось '15', но получено: '{final_text}'"
    )
