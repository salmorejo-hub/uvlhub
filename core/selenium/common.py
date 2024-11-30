import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def initialize_driver():
    # Initializes the browser options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Initialise the browser using WebDriver Manager
    service = Service(os.getenv("CHROMEDRIVER_BIN_PATH", ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_driver(driver):
    driver.quit()
