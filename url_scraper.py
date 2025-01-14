from dotenv import dotenv_values
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from typing import Generator
import time

class OttaScraper(object):

    def __init__(self):
        self.driver = None
        self.config = None
    
    def initialize(self):
        self.config = dotenv_values(".env")

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # supposedly unnecessary
        options.add_argument("--disable-notifications")
        options.add_experimental_option("detach", True)  # keep open after ending

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5.0)
        self.driver.get("https://app.welcometothejungle.com")

        self._try_login()
    
    def _try_login(self) -> None:
        # log in
        try:
            email_text_box = self.driver.find_element(By.XPATH, "//input[@type='email']")
            email_text_box.send_keys(self.config['OTTA_EMAIL'])
        except NoSuchElementException:
            print(f"Couldn't find email text box.")
            raise
        
        try:
            password_text_box = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_text_box.send_keys(self.config['OTTA_PASSWORD'])
        except NoSuchElementException:
            print(f"Couldn't find password text box.")
            raise
        
        try:
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
        except NoSuchElementException:
            print(f"Couldn't find login button.")
            raise
        
        # Close center pop-up dialog
        try:
            center_dialog_x = self.driver.find_element(By.XPATH, "//div[@role='dialog']//button[1]")
            center_dialog_x.click()
        except NoSuchElementException:
            print(f"Couldn't find center dialog.")
            raise

        time.sleep(5)  # unfortunately necessary; closing the next dialog immediately results in a graphical glitch
        
        try:
            cookie_dialog_x = self.driver.find_element(By.ID, "axeptio_btn_dismiss")
            cookie_dialog_x.click()
        except NoSuchElementException:
            print(f"Couldn't find cookie dialog.")
            # No need to exit if we can't find it.

        try:
            jobs_button = self.driver.find_element(By.XPATH, "//p[@data-title='Jobs']")
            jobs_button.click()
        except NoSuchElementException:
            print(f"Couldn't find jobs button.")
            raise

    def get_urls(self) -> Generator[str, None, None]:

        if self.driver is None:
            raise ValueError("Not initialized.")
        

        
        while True:
            # Deal with "did you apply dialog"
            try:
                modal_element = self.driver.find_element(By.XPATH, "//div[@data-testid='modal']")
                modal_element.find_element(By.XPATH, "//button[1]").click()
                time.sleep(0.5)
            except NoSuchElementException:
                pass

            # Deal with "see another set of matches"
            try:
                see_another_set_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='See more jobs']")
                see_another_set_button.click()
                time.sleep(0.5)
            except NoSuchElementException:
                pass

            apply_button = self.driver.find_element(By.XPATH, "//button[@data-testid='apply-button']")
            apply_button.click()

            # Find the button within the apply dialog with an href
            apply_dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            links = apply_dialog.find_elements(By.TAG_NAME, "a")
            
            url = None 
            for link in links:
                href = link.get_attribute("href")
                if href is not None:
                    url = href
                    break
            
            if url is None:
                raise RuntimeError("Couldn't find an external url.")

            # Now advance to the next page
            try:
                close_dialog_button = self.driver.find_element(By.XPATH, "//button[@aria-label='close']")
                close_dialog_button.click()
            except NoSuchElementException:
                print(f"Couldn't find the close button on the apply dialog.")
                raise

            try:
                next_button = self.driver.find_element(By.XPATH, "//button[@data-testid='next-button']")
                next_button.click()
            except NoSuchElementException:
                print(f"Couldn't find the next page button.")
                raise

            time.sleep(0.5)

            yield url

if __name__ == "__main__":
    # test of functionality
    scraper = OttaScraper()
    scraper.initialize()
    
    urls_generator = scraper.get_urls()
    for i in range(15):
        print(f"url: {next(urls_generator)}")

    


