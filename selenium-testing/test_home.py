'''
    Purpose: Testing Field for application
    Note   : Before Running, ensure database is fresh
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service
# Test Score

def test_home():
    driver = webdriver.Chrome(service=Service('selenium-testing/chromedriver.exe'))
    driver.get("http://127.0.0.1:5000")

    try:
        assert 'Intro' in driver.title
        print("Test passed: Page loaded successfully.")
    except AssertionError:
        print("Test failed: Page title does not contain 'Intro'.")

    driver.close()