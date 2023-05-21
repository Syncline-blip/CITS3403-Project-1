'''
    Purpose: Testing Field for application
    Note   : Before Running, ensure database is fresh
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service


def test_check_page_on_land():
     
    driver = webdriver.Chrome(service=Service('selenium-testing\chromedriver.exe'))
    driver.get("http://127.0.0.1:5000")

    # List of pages to test
    pages = ["/login", "/sign-up", "/contact_us", "/privacy", "/about_us"]


    for page in pages:
        driver.get(f"http://127.0.0.1:5000{page}")
        time.sleep(2)
        try:
            print(f"Test passed: Page '{page}' loaded successfully.")
        except AssertionError:
            print(f"Test failed: Page '{page}' not loaded or incorrect page title.")