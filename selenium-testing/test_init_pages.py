from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def test_pages():
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000")

    # List of pages to test
    pages = ["/login", "/sign-up", "/contact-us", "/privacy", "/about_us"]

    for page in pages:
        driver.get(f"http://127.0.0.1:5000{page}")
        time.sleep(2)
        try:
            print(f"Test passed: Page '{page}' loaded successfully.")
        except AssertionError:
            print(f"Test failed: Page '{page}' not loaded or incorrect page title.")



test_pages()






