
import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

COOKIE_FILE = "cookies.pkl"
LOGIN_URL = "https://app.prizepicks.com"

def save_cookies(driver, filepath):
    with open(filepath, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filepath):
    with open(filepath, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def login_with_selenium():
    options = uc.ChromeOptions()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    driver = uc.Chrome(options=options)

    driver.get(LOGIN_URL)
    time.sleep(5)

    # If cookies exist, try to reuse them
    if os.path.exists(COOKIE_FILE):
        load_cookies(driver, COOKIE_FILE)
        driver.get(LOGIN_URL)
        time.sleep(5)
        if "login" not in driver.current_url:
            print("Logged in using cookies.")
            return driver

    # Manual login step
    print("Please complete login manually if prompted.")
    time.sleep(45)

    # Save cookies after login
    save_cookies(driver, COOKIE_FILE)
    print("Cookies saved.")
    return driver

if __name__ == "__main__":
    driver = login_with_selenium()
    input("Press Enter to close browser...")
    driver.quit()
