from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from core.selenium.common import initialize_driver


def test_exploreuvl():
    driver = initialize_driver()
    driver.get("http://localhost:5000/")
    driver.set_window_size(1850, 1053)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Explore UVLs')]"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-12:nth-child(1) .row .badge:nth-child(1)"))
        ).click()
        dropdown = driver.find_element(By.ID, "publication_type")
        dropdown.find_element(By.XPATH, "//option[. = 'Software Documentation']").click()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).release().perform()
        driver.find_element(By.ID, "clear-filters").click()
        driver.find_element(By.CSS_SELECTOR, ".col-12:nth-child(1) > .btn").click()
        dropdown = driver.find_element(By.ID, "publication_type")
        dropdown.find_element(By.XPATH, "//option[. = 'Taxonomic Treatment']").click()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element = driver.find_element(By.ID, "publication_type")
        actions = ActionChains(driver)
        actions.move_to_element(element).release().perform()
        driver.find_element(By.ID, "clear-filters").click()

    except NoSuchElementException:
        raise AssertionError('Test failed!')

    except ElementClickInterceptedException:
        raise AssertionError('Element click intercepted!')

    finally:
        # Close the browser
        driver.quit()
