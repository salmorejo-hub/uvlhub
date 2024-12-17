from selenium.webdriver.common.by import By
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_dark_without_logging():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.find_element(By.ID, "theme-toggle").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Explore").click()
        
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Team").click()
        
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Explore UVLs").click()
        
        time.sleep(2)
        driver.find_element(By.ID, "clear-filters").click()
        driver.find_element(By.CSS_SELECTOR, ".hamburger").click()
        driver.find_element(By.CSS_SELECTOR, ".sidebar-toggle").click()
        driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(7) .align-middle:nth-child(2)").click()
        driver.find_element(By.ID, "theme-toggle").click()
 
    finally:
        close_driver(driver)

# Call the test functions
test_dark_without_logging()