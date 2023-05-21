from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def test_home():
    driver = webdriver.Chrome('selenium-testing\chromedriver.exe')
    driver.get("http://127.0.0.1:5000") 

    try:
        assert 'Intro' in driver.title
        print("Test passed: Page loaded successfully.")
    except AssertionError:
        print("Test failed: Page title does not contain 'Intro'.")

    driver.close()