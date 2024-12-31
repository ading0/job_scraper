from dotenv import dotenv_values
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

def try_login(driver: webdriver.Chrome) -> None:
    # log in
    try:
        email_text_box = driver.find_element(By.XPATH, "//input[@type='email']")
        email_text_box.send_keys(config['OTTA_EMAIL'])
    except NoSuchElementException:
        print(f"Couldn't find email text box.")
        exit()
    
    try:
        password_text_box = driver.find_element(By.XPATH, "//input[@type='password']")
        password_text_box.send_keys(config['OTTA_PASSWORD'])
    except NoSuchElementException:
        print(f"Couldn't find password text box.")
        exit()
    
    try:
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
    except NoSuchElementException:
        print(f"Couldn't find login button.")
        exit()
    
    # Close center pop-up dialog
    try:
        center_dialog_x = driver.find_element(By.XPATH, "//div[@role='dialog']//button[1]")
        center_dialog_x.click()
    except NoSuchElementException:
        print(f"Couldn't find center dialog.")
        exit()

    time.sleep(5)  # unfortunately necessary; closing the next dialog immediately results in a graphical glitch
    
    try:
        cookie_dialog_x = driver.find_element(By.ID, "axeptio_btn_dismiss")
        cookie_dialog_x.click()
    except NoSuchElementException:
        print(f"Couldn't find cookie dialog.")


if __name__ == "__main__":
    config = dotenv_values(".env")

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # supposedly unnecessary
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)  # keep open after ending

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5.0)
    driver.get("https://app.welcometothejungle.com")

    try_login(driver)

    


