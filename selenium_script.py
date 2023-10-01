import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Настройка логирования
logging.basicConfig(
    filename='selenium_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def login(driver, username, password):
    try:
        driver.find_element(
            By.CSS_SELECTOR, '.user-button__login .block').click()
        driver.find_element(By.NAME, 'user_login').clear()
        driver.find_element(By.NAME, 'user_login').send_keys(username)
        driver.find_element(By.NAME, 'user_password').clear()
        driver.find_element(By.NAME, 'user_password').send_keys(password)
        driver.find_element(By.NAME, 'user_password').send_keys(Keys.ENTER)

        # Записываем успешный вход в лог
        logging.info(f"Успешный вход: {username}")

    except Exception as e:
        # Записываем ошибку входа в лог
        logging.error(f"Ошибка при входе: {username} - {str(e)}")


def logout(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '.user-menu__username').click()
        driver.find_element(
            By.CSS_SELECTOR, '.row:nth-child(2) > .user-menu__text').click()

        # Записываем успешный выход в лог
        logging.info("Успешный выход")

    except Exception as e:
        # Записываем ошибку выхода в лог
        logging.error(f"Ошибка при выходе: {str(e)}")


def main():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://ccq.l.cidious.com/")

        login(driver, '+12345678901', '123123123')
        time.sleep(2)

        logout(driver)
        time.sleep(2)

        login(driver, '+12345678902', '123123123')
        time.sleep(2)

        logout(driver)
        time.sleep(2)

    except Exception as e:
        # Записываем общую ошибку в лог
        logging.error(f"Общая ошибка: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()