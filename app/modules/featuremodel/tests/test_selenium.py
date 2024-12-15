from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def count_featuremodels(driver):
    try:
        amount_featuremodels = len(driver.find_elements(By.CLASS_NAME, "card-body"))
    except Exception:
        amount_featuremodels = 0
    return amount_featuremodels


def test_featuremodel_index():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the index page
        driver.get(f'{host}/featuremodel')

        # Wait a little while to make sure the page has loaded completely
        time.sleep(4)

        try:

            pass

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


def test_featuremodel_list_software_documentation():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the searcher page for featuremodels
        driver.get(f'{host}/exploreuvl')
        wait_for_page_to_load(driver)

        searcher_field = driver.find_element(By.ID, "publication_type")
        time.sleep(1)
        searcher_field.send_keys("softwaredocumentation")
        time.sleep(1)

        n_featuremodels = count_featuremodels(driver)

        assert n_featuremodels == 12, f"Fallo. Debería haberse filtrado solo 12 featuremodels, no {n_featuremodels}"

    except NoSuchElementException:
        raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


def test_featuremodel_list_query():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the searcher page for featuremodels
        driver.get(f'{host}/exploreuvl')
        wait_for_page_to_load(driver)

        searcher_field = driver.find_element(By.ID, "search-uvl-query")
        time.sleep(2)
        searcher_field.send_keys('0000-0000-0000-0005')
        searcher_field.send_keys(Keys.RETURN)
        time.sleep(2)

        n_featuremodels = count_featuremodels(driver)

        assert n_featuremodels == 1, f"Fallo. Debería haberse filtrado solo 1 featuremodel, no {n_featuremodels}"

        searcher_field = driver.find_element(By.ID, "search-uvl-query")
        time.sleep(2)
        searcher_field.send_keys('softwaredocumentation')
        searcher_field.send_keys(Keys.RETURN)
        time.sleep(2)

        n_featuremodels = count_featuremodels(driver)

        assert n_featuremodels == 0, \
            "Fallo. No deberían filtrarse elementos, porque en este campo no se filtra por etiqueta."

    except NoSuchElementException:
        raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)
