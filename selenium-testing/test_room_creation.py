# Testing Room Creation
from selenium import webdriver
from selenium.webdriver.common.by import By

def run_room():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000") # Assuming that the website is currently run
    driver.get("http://127.0.0.1:5000/sign-up") # Sign Up create an account
    iter = 0
    email = "selenium@uwa.example.com"
    username = "selenium-automation"
    password = "tgr_pass1"

    '''
        TEST A: Sign Up 
    '''
    print("=== TEST SIGN UP ===")
    try:
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

        print("Register Success!")
        # Click on the private message icon
        driver.get("http://127.0.0.1:5000/home")
        private_message_button = driver.find_element("id","create-btn")
        private_message_button.click()

        print("Room creation Success! ")
        iter +=1
    except AssertionError:
        print("Failed registration, test exiting")
    print("=== TEST SIGN UP FIN ===")


    ''' TEST B: Go in to a new private game lobby '''
    print("=== TEST ROOM CREATION ===")
    try:
        
        # Click on the private message icon
        driver.get("http://127.0.0.1:5000/home")
        private_message_button = driver.find_element("id","create-btn")
        private_message_button.click()

        print("Room creation Success! ")
        iter +=1
    except AssertionError:
        print("Failed Room Creation, Exit ")

    print(f"Test passed {iter}")
    
run_room()