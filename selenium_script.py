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
        logging.info(f"Попытка авторизации пользователя {username}...")
        find_element_by_selector('.user-button__login .block').click()
        find_element_by_name('user_login').clear()
        find_element_by_name('user_login').send_keys(username)
        find_element_by_name('user_password').clear()
        find_element_by_name('user_password').send_keys(password)
        find_element_by_name('user_password').send_keys(Keys.ENTER)

        time.sleep(1)
        logging.info(f"Успешный вход: {username}")

    except Exception as e:
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
        logging.info("Попытка деавторизации пользователя...")
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

        # driver.maximize_window()
        logging.info(
            "Загрузка главной страницы...")
        driver.get(url)
        time.sleep(2)
        courses = driver.find_elements(By.CLASS_NAME, "course-card")
        logging.info("Поиск курсов на главной странице...")
        time.sleep(1)
        logging.info(
            f'Количество курсов на главной странице: {len(courses)}')
        courses_titles = driver.find_elements(
            By.CLASS_NAME, 'course-card__title'
        )
        for element in courses_titles:
            logging.info(f'Название курса: {element.text}')
        logging.info("Успешная загрузка главной страницы!")

    except Exception as e:
        logging.error(f"Ошибка при загрузке главной страницы: {str(e)}")


def course_info(driver):
    """
    A function that retrieves information about a course using a webdriver.

    Args:
        driver: An instance of a webdriver.

    Returns:
        None. The function logs information about the course using the logging module.
    """
    try:
        logging.info('Поиск заданного курса на главной странице...')
        course_card = driver.find_elements(By.CLASS_NAME, "course-card")[0]
        course_card_content = course_card.find_element(
            By.CLASS_NAME, "course-card__content")
        course_router = course_card_content.find_element(
            By.CLASS_NAME, "course-card__router")
        course_router.click()
        logging.info('Переход на страницу курса...')
        time.sleep(1)
        page_title_text = driver.find_element(
            By.CLASS_NAME, 'page-title__text')
        author_name = driver.find_element(
            By.CLASS_NAME, 'author__name')
        author_rank = driver.find_element(
            By.CLASS_NAME, 'author__rank')
        lesson_of_a_course__title = driver.find_elements(
            By.CLASS_NAME, 'lesson-of-a-course__title')
        lesson_of_a_course = driver.find_elements(
            By.CLASS_NAME, 'lesson-of-a-course')
        logging.info(f'Заголовок курса: {page_title_text.text}')
        logging.info(f'Автор курса: {author_rank.text} {author_name.text}')
        logging.info(f'Количество уроков в курсе: {len(lesson_of_a_course)}')
        for element in lesson_of_a_course__title:
            logging.info(f'Содержание курса: {element.text}')
        logging.info('Курс успешно найден!')
    except Exception as e:
        logging.error(f"Ошибка при поиске информации о курсе: {str(e)}")


def lesson_info(driver):
    """
    Retrieves information about a specific lesson on the course page.

    Parameters:
        driver (WebDriver): The WebDriver instance used to interact with the web page.

    Returns:
        None
    """
    try:
        logging.info('Поиск заданного урока на странице курса...')
        time.sleep(2)
        lessons = driver.find_elements(
            By.CLASS_NAME, 'lesson-of-a-course')
        number_of_lesson = lessons[1]
        number_of_lesson.click()
        logging.info('Переход на страницу урока...')
        time.sleep(2)
        lesson_title = driver.find_element(
            By.CLASS_NAME, 'page-title__text')
        logging.info('Название урока: ' + lesson_title.text)
        logging.info('Урок успешно загружен!')
        logging.info('Переход на главную страницу...')
        time.sleep(2)
        driver.get(url)
    except Exception as e:
        logging.error(f"Ошибка при поиске информации о уроке: {str(e)}")


def main():
    try:
        main_page(driver)
        time.sleep(3)
        logging.info("->")

        course_info(driver)
        time.sleep(1)
        logging.info("->")

        lesson_info(driver)
        time.sleep(1)
        logging.info("->")

        log_in(trainer, password)
        time.sleep(2)
        log_out()
        logging.info("->")

        log_in(user, password)
        time.sleep(2)
        log_out()
        logging.info("->")

        time.sleep(5)
        logging.info("------------------------------------")

    except Exception as e:
        # Записываем общую ошибку в лог
        logging.error(f"Общая ошибка: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
