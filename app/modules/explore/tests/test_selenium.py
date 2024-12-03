from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

from core.selenium.common import initialize_driver, close_driver


def test_explore_index():
    driver = initialize_driver()
    driver.get("http://localhost:5000/explore")

    try:
        # Wait for the element to be visible and enabled
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "max_size"))
        ).send_keys("3")

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "size_unit"))
        )
        dropdown.find_element(By.XPATH, "//option[. = 'KB']").click()

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "size_unit"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(element).click_and_hold().perform()
        actions.move_to_element(element).release().perform()

        dropdown.find_element(By.XPATH, "//option[. = 'MB']").click()
        dropdown.find_element(By.XPATH, "//option[. = 'GB']").click()

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "day"))
        )
        dropdown.find_element(By.XPATH, "//option[. = '5']").click()
        dropdown.find_element(By.XPATH, "//option[. = 'Any']").click()

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "month"))
        )
        dropdown.find_element(By.XPATH, "//option[. = 'February']").click()
        dropdown.find_element(By.XPATH, "//option[. = 'June']").click()

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "year"))
        )
        dropdown.find_element(By.XPATH, "//option[. = '2016']").click()
        dropdown.find_element(By.XPATH, "//option[. = '2021']").click()

        clear_filters_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "clear-filters"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", clear_filters_btn)
        driver.execute_script("arguments[0].click();", clear_filters_btn)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "max_number_of_models"))
        ).send_keys("46")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "min_number_of_features"))
        ).send_keys("13")

        clear_filters_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "clear-filters"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", clear_filters_btn)
        driver.execute_script("arguments[0].click();", clear_filters_btn)

    except NoSuchElementException:
        raise AssertionError('Test failed!')

    except ElementClickInterceptedException:
        raise AssertionError('Element click intercepted!')

    finally:
        # Close the browser
        close_driver(driver)