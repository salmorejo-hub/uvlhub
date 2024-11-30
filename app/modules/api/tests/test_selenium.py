from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_api_token():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the index page
        driver.get(f'{host}/')

        # Wait a little while to make sure the page has loaded completely
        time.sleep(2)

        try:
            driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(6) .align-middle:nth-child(2)").click()
            driver.find_element(By.ID, "email").click()
            driver.find_element(By.ID, "email").send_keys("user1@example.com")
            driver.find_element(By.ID, "password").send_keys("1234")
            driver.find_element(By.ID, "submit").click()

            driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(10) .align-middle:nth-child(2)").click()
            driver.find_element(By.ID, "token-expiration").click()
            driver.find_element(By.ID, "token-expiration").send_keys("100")

            driver.find_element(By.CSS_SELECTOR, ".btn").click()
            driver.find_element(By.ID, "token-expiration").click()

            print('Test passed!')

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


# Call the test function
test_api_token()
