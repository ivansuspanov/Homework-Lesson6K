from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_form_corrected():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

    wait = WebDriverWait(driver, 20)

    fields_to_fill = [
        ("first-name", "Иван"),
        ("last-name", "Петров"),
        ("address", "Ленина, 55-3"),
        ("e-mail", "test@skypro.com"),
        ("phone", "+7985899998787"),
        ("city", "Москва"),
        ("country", "Россия"),
        ("job-position", "QA"),
        ("company", "SkyPro"),
    ]

    for name, value in fields_to_fill:
        elem = wait.until(EC.presence_of_element_located((By.NAME, name)))
        elem.clear()
        elem.send_keys(value)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    zip_code_field = wait.until(
        EC.presence_of_element_located((By.ID, "zip-code")))
    assert "alert-danger" in zip_code_field.get_attribute("class"), (
        "Поле zip-code должно иметь класс alert-danger"
    )

    valid_fields_ids = [
        "first-name",
        "last-name",
        "address",
        "e-mail",
        "phone",
        "city",
        "country",
        "job-position",
        "company",
    ]

    for field_id in valid_fields_ids:
        field = wait.until(EC.presence_of_element_located((By.ID, field_id)))
        assert "alert-danger" not in field.get_attribute("class"), (
            f"Поле {field_id} не должно иметь класс alert-danger"
        )

    driver.quit()
