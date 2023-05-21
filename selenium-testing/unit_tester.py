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
    pages = ["/login", "/sign-up", "/contact_us", "/privacy", "/about_us"]

    print("---------- TEST 1: CHECK INITIAL PAGES ----------")
    for page in pages:
        driver.get(f"http://127.0.0.1:5000{page}")
        time.sleep(2)
        try:
            print(f"Test passed: Page '{page}' loaded successfully.")
        except AssertionError:
            print(f"Test failed: Page '{page}' not loaded or incorrect page title.")
            return score
    print("---------- TEST 1: FIN ----------\n")
    score +=1
    return score

''' 
    Checks to see if the website will login a non-registered user, fail if it does
'''
def attempt_non_registered():
    score = 0
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/login")

    email = "nonexistent@example.com"
    password = "invalidpassword"

    email_input = driver.find_element("id", "email")
    email_input.send_keys(email)

    password_input = driver.find_element("id", "password")
    password_input.send_keys(password)

    submit_button = driver.find_element("xpath", "//button[@type='submit']")
    submit_button.click()

    print("---------- TEST 2: NON-REGISTERED USER ----------")
    try:
        error_message = driver.find_element("class name", "alert-danger")
        print("Login failed: User does not exist. Test Passed")
    except Exception:
        print("Login successful. Website allowed a non-registered to the website")
        return score
    print("---------- TEST 2: FIN ----------\n")

    score +=1
    return score


''' Launch All Required tests'''
def main():
    test_score = 0

    test_score += check_page_on_land()
    test_score += attempt_non_registered()
    print(f"Test Score: {test_score}")

if __name__ == "__main__":
    main()