import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver

from selenium.common.exceptions import NoSuchElementException


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def count_datasets(driver, host):
    driver.get(f"{host}/dataset/list")
    wait_for_page_to_load(driver)

    try:
        amount_datasets = len(driver.find_elements(By.XPATH, "//table//tbody//tr"))
    except Exception:
        amount_datasets = 0
    return amount_datasets


def test_upload_dataset():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Count initial datasets
        initial_datasets = count_datasets(driver, host)

        # Open the upload dataset
        driver.get(f"{host}/dataset/upload")
        wait_for_page_to_load(driver)

        # Find basic info and UVL model and fill values
        title_field = driver.find_element(By.NAME, "title")
        title_field.send_keys("Title")
        desc_field = driver.find_element(By.NAME, "desc")
        desc_field.send_keys("Description")
        tags_field = driver.find_element(By.NAME, "tags")
        tags_field.send_keys("tag1,tag2")

        # Add two authors and fill
        add_author_button = driver.find_element(By.ID, "add_author")
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        name_field0 = driver.find_element(By.NAME, "authors-0-name")
        name_field0.send_keys("Author0")
        affiliation_field0 = driver.find_element(By.NAME, "authors-0-affiliation")
        affiliation_field0.send_keys("Club0")
        orcid_field0 = driver.find_element(By.NAME, "authors-0-orcid")
        orcid_field0.send_keys("0000-0000-0000-0000")

        name_field1 = driver.find_element(By.NAME, "authors-1-name")
        name_field1.send_keys("Author1")
        affiliation_field1 = driver.find_element(By.NAME, "authors-1-affiliation")
        affiliation_field1.send_keys("Club1")

        # Obtén las rutas absolutas de los archivos
        file1_path = os.path.abspath("app/modules/dataset/uvl_examples/file1.uvl")
        file2_path = os.path.abspath("app/modules/dataset/uvl_examples/file2.uvl")

        # Subir el primer archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file1_path)
        wait_for_page_to_load(driver)

        # Subir el segundo archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file2_path)
        wait_for_page_to_load(driver)

        # Add authors in UVL models
        show_button = driver.find_element(By.ID, "0_button")
        show_button.send_keys(Keys.RETURN)
        add_author_uvl_button = driver.find_element(By.ID, "0_form_authors_button")
        add_author_uvl_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        name_field = driver.find_element(By.NAME, "feature_models-0-authors-2-name")
        name_field.send_keys("Author3")
        affiliation_field = driver.find_element(By.NAME, "feature_models-0-authors-2-affiliation")
        affiliation_field.send_keys("Club3")

        # Check I agree and send form
        check = driver.find_element(By.ID, "agreeCheckbox")
        check.send_keys(Keys.SPACE)
        wait_for_page_to_load(driver)

        upload_btn = driver.find_element(By.ID, "upload_button")
        upload_btn.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        time.sleep(2)  # Force wait time

        assert driver.current_url == f"{host}/dataset/list", "Test failed!"

        # Count final datasets
        final_datasets = count_datasets(driver, host)
        assert final_datasets == initial_datasets + 1, "Test failed!"

        print("Test passed!")

    finally:

        # Close the browser
        close_driver(driver)


def test_file_previsualize():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Navigate to the dataset page
        driver.get(f'{host}/doi/10.1234/dataset4/')
        time.sleep(4)

        # Click the button to open the file content
        try:
            button = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/div[3]/div[2]/div/div[2]/div/div[2]/button")
            button.click()
            time.sleep(2)
        except NoSuchElementException:
            raise AssertionError('Test failed: Button to open file content is not visible.')

        # Check that the file content is displayed
        try:
            file_content_element = driver.find_element(By.XPATH, "//*[@id='fileContent']")
            file_content_text = file_content_element.text

            # Expected content
            expected_content = """features
    Chat
        mandatory
            Connection
                alternative
                    "Peer 2 Peer"
                    Server
            Messages
                or
                    Text
                    Video
                    Audio
        optional
            "Data Storage"
            "Media Player"

constraints
    Server => "Data Storage"
    Video | Audio => "Media Player\""""

            # Verify content matches expected
            assert file_content_text.strip() == expected_content.strip(), (
                f'Test failed: File content does not match expected content.\n'
                f'Expected:\n{expected_content}\n'
                f'Got:\n{file_content_text}'
            )
        except NoSuchElementException:
            raise AssertionError('Test failed: File content is not visible.')

    finally:
        close_driver(driver)


test_upload_dataset()
test_file_previsualize()
