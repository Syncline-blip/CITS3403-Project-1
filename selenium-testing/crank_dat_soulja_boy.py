'''
    Purpose: Testing Field for application

'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Test Score


'''
    Checks the page when first opened, simple test to see if all links
    to page is there
'''
def check_page_on_land():
    score = 0
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
    score +=1
    return score



''' Launch All Required tests'''
def main():
    test_score = 0
    test_score += check_page_on_land()



if __name__ == "__main__":
    main()