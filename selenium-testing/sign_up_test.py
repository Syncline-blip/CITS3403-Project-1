from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def test_signup():
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/sign-up")

    email = "selenium@uwa.example.com"
    username = "selenium-automation"
    password = "tgr_pass1"

    # Find the form element
    form = driver.find_element("tag name", "form")

    # Fill out the registration form
    email_input = form.find_element("id", "email")
    email_input.send_keys(email)

    username_input = form.find_element("id", "username")
    username_input.send_keys(username)

    password1_input = form.find_element("id", "password1")
    password1_input.send_keys(password)

    password2_input = form.find_element("id", "password2")
    password2_input.send_keys(password)

    # Submit the form
    submit_button = form.find_element("xpath", "//button[@type='submit']")
    submit_button.click()

    # Wait for the registration process to complete
    driver.implicitly_wait(5)

    # Find the Logout button and click it
    time.sleep(10)
    logout_button = driver.find_element("link text", "Logout")
    logout_button.click()

    # Wait for the logout process to complete
    driver.implicitly_wait(5)

    # Check if logout was successful
    try:
        login_link = driver.find_element("link text", "Login")
        print("Logout successful, there for login is successful.")
    except Exception:
        print("Logout failed. may not have been logged on properly")

    driver.close()

test_signup()

