from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os, time, pickle

load_dotenv()

USERNAME = os.getenv("PRIZEPICKS_USERNAME")
PASSWORD = os.getenv("PRIZEPICKS_PASSWORD")

COOKIES_FILE = "cookies.pkl"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def save_cookies(driver, location):
    with open(location, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, location):
    with open(location, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

driver.get("https://app.prizepicks.com/")
time.sleep(5)

if os.path.exists(COOKIES_FILE):
    load_cookies(driver, COOKIES_FILE)
    driver.get("https://app.prizepicks.com/")
    time.sleep(5)
else:
    login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Log In")]')
    login_button.click()
    time.sleep(2)

    driver.find_element(By.NAME, "email").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//button[contains(text(), "Login")]').click()

    time.sleep(5)
    save_cookies(driver, COOKIES_FILE)

print("Logged in successfully.")
driver.quit()