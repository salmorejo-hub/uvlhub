from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_average_rating_logged_in():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Log in
        driver.get(f'{host}/login')
        time.sleep(4)
        
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        time.sleep(4)

        # Navigate to the dataset page
        driver.get(f'{host}/doi/10.1234/dataset4/')
        time.sleep(4)

        # Check for "Average Rating"
        assert driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/div[5]/div[1]/span"), \
            'Test failed: "Average Rating" is not visible.'

    finally:
        close_driver(driver)


def test_your_rating_logged_in():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Log in
        driver.get(f'{host}/login')
        time.sleep(4)
        
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        time.sleep(4)

        # Navigate to the dataset page
        driver.get(f'{host}/doi/10.1234/dataset4/')
        time.sleep(4)

        # Check for "Your Rating"
        assert driver.find_element(By.XPATH, "//*[@id='user-rating-section']/div[1]/span"), \
            'Test failed: "Your Rating" is not visible.'

    finally:
        close_driver(driver)


def test_average_rating_not_logged_in():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Navigate to the dataset page
        driver.get(f'{host}/doi/10.1234/dataset4/')
        time.sleep(4)

        # Check for "Average Rating"
        assert driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[3]/div[1]/div[1]/div[1]/div[5]/div[1]/span"), \
            'Test failed: "Average Rating" is not visible.'

    finally:
        close_driver(driver)


def test_rating_options_logged_in():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Log in
        driver.get(f'{host}/login')
        time.sleep(4)
        
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        time.sleep(4)

        # Navigate to the dataset page
        driver.get(f'{host}/doi/10.1234/dataset4/')
        time.sleep(4)

        # Check for the rating select options
        select_element = driver.find_element(By.XPATH, "//*[@id='user-rating']")
        options = select_element.find_elements(By.TAG_NAME, 'option')
        
        # Expected options
        expected_options = [
            "Select rating",
            "1 - Poor",
            "2 - Fair",
            "3 - Good",
            "4 - Very Good",
            "5 - Excellent"
        ]
        
        actual_options = [option.text for option in options]
        assert actual_options == expected_options, \
            f'Test failed: Rating options are incorrect. Expected {expected_options}, but got {actual_options}.'

    finally:
        close_driver(driver)


# Call the test functions
test_average_rating_logged_in()
test_your_rating_logged_in()
test_average_rating_not_logged_in()
test_rating_options_logged_in()
