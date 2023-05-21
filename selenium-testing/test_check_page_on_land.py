from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import os

def test_check_page_on_land():
    score = 0
    driver = webdriver.Chrome(service=Service('selenium-testing\chromedriver.exe'))
    driver.get("http://127.0.0.1:5000")

    # List of pages to test
    pages = ["/login", "/sign-up", "/contact_us", "/privacy", "/about_us"]

    print("---------- TEST 1: CHECK INITIAL PAGES ----------")
    for page in pages:
        driver.get(f"http://127.0.0.1:5000{page}")
        time.sleep(2)
        try:
            assert page in driver.current_url
            print(f"Test passed: Page '{page}' loaded successfully.")
            score +=1
        except AssertionError:
            print(f"Test failed: Page '{page}' not loaded or incorrect page title.")
    print("---------- TEST 1: FIN ----------\n")
    
    driver.quit()  # add this line at the end
    return score
    