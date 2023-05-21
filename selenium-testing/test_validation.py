from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service

def test_short_user():
     
    driver = webdriver.Chrome(service=Service('selenium-testing/chromedriver.exe'))
    driver.get("http://127.0.0.1:5000/sign-up")

    email = "broke@gmail.com"
    username = "a"
    password = "a"

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
    try:
        error_message = driver.find_element("class name", "alert-danger")
        if error_message.text == "Username must be between 2 and 15 characters long":
            print("Login failed: User does not exist. Test Passed")
    except Exception:
        print("Login successful. Website allowed a non-registered to the website")
          
    driver.close()
     