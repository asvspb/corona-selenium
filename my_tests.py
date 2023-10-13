import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()
dom_structure = ''
driver = webdriver.Chrome()
url = os.environ['URL']
trainer = os.environ['LOGIN_TRAINER']
user = os.environ['LOGIN_USER']
password = os.environ['PASSWORD']

# Настройка логирования
logging.basicConfig(
    filename='selenium_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def find_element_by_selector(selector):
    """
    Finds and returns an element located by the given CSS selector.

    Parameters:
        selector (str): The CSS selector used to locate the element.

    Returns:
        WebElement: The element located by the CSS selector.

    Raises:
        TimeoutException: If the element is not found within 2 seconds.
    """
    return WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_element_by_name(name):
    """
    Find an element by its name using the given `name` parameter.

    Args:
        name (str): The name of the element to find.

    Returns:
        WebElement: The element found by its name.

    Raises:
        TimeoutException: If the element is not found within 2 seconds.

    """
    return WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.NAME, name))
    )


def log_in(username, password):
    """
    Logs in the user with the given username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    try:
        find_element_by_selector('.user-button__login .block').click()
        find_element_by_name('user_login').clear()
        find_element_by_name('user_login').send_keys(username)
        find_element_by_name('user_password').clear()
        find_element_by_name('user_password').send_keys(password)
        find_element_by_name('user_password').send_keys(Keys.ENTER)

        # Записываем успешный вход в лог
        logging.info(f"Успешный вход: {username}")

    except Exception as e:
        # Записываем ошибку входа в лог
        logging.error(f"Ошибка при входе: {username} - {str(e)}")


def log_out():
    """
    Logs out the user by clicking on the user menu and then the logout button.

    This function does not take any parameters.

    This function does not return any values.

    Raises:
        Exception: If there is an error during the logout process.
    """
    try:
        find_element_by_selector('.user-menu__username').click()
        find_element_by_selector(
            '.row:nth-child(2) > .user-menu__text').click()

        # Записываем успешный выход в лог
        logging.info("Успешный выход")

    except Exception as e:
        # Записываем ошибку выхода в лог
        logging.error(f"Ошибка при выходе: {str(e)}")


def main_page(driver):
    """
    A function that loads the main page in the browser and logs the result.

    Args:
        driver: The driver object for interacting with the browser.

    Returns:
        None.
    """
    try:

        driver.minimize_window()
        driver.get(url)
        logging.info("Успешная загрузка главной страницы")
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, 'body')
        html = body.get_attribute('outerHTML')
        course_element = driver.find_element(
            By.CSS_SELECTOR, ".course-list__courses").get_attribute("outerHTML")
        logging.info(
            f'Список курсов: {course_element}')

    except Exception as e:
        logging.error(f"Ошибка при загрузке главной страницы: {str(e)}")


def main():
    try:
        logging.info("Начало тестирования")

        main_page(driver)
        time.sleep(3)

        # log_in(trainer, password)
        # time.sleep(3)
        # log_out()

        # log_in(user, password)
        # time.sleep(3)
        # log_out()

        time.sleep(3)
        logging.info("Завершение тестирования")

    except Exception as e:
        # Записываем общую ошибку в лог
        logging.error(f"Общая ошибка: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
