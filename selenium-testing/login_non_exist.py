# Test will pass if the login fails as the given user does not exist

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def test_login():
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


    try:
        error_message = driver.find_element("class name", "alert-danger")
        print("Login failed: User does not exist. Test Passed")
    except Exception:
        print("Login successful.")

  

test_login()







