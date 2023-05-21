'''
    Purpose: Testing Field for application
    Note   : Before Running, ensure database is fresh
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service


''' 
    5 CHECK IF A PUBLIC CHAT CAN BE FOUND:
'''
def pub_chat_access():
     
    driver = webdriver.Chrome(service=Service('selenium-testing\chromedriver.exe'))
    driver.get("http://127.0.0.1:5000")

    # Login this assumes that a person with this email is already registered
    email = "selenium@example.com"
    password = "tgrpass1"

    email_input = driver.find_element("id", "email")
    email_input.send_keys(email)
    print("Email entered")

    password_input = driver.find_element("id", "password")
    password_input.send_keys(password)
    print("Password entered")

    submit_button = driver.find_element("xpath", "//button[@type='submit']")
    submit_button.click()
    print("Submit button clicked")

    # Wait for the login process to complete
    driver.implicitly_wait(5)

    # Enter the global chat
    print("---------- TEST 4: ENTER PUBLIC CHAT ----------")
    try:
        
        global_chat_button = driver.find_element("css selector", ".chatLink[name='globalChat']")
        global_chat_button.click()
        print("Global Chat button clicked")
        
        # Wait for the global chat to load
        driver.implicitly_wait(5)

        chat_title = driver.find_element("id", "title")
        if chat_title.text == "Chat Room: GLOB":
            print("User successfully entered the Global Chat.")
        else:
            print("Failed to enter the Global Chat.")
    except AssertionError:
        print("Failed to find the Global Chat button.")
          
    print("---------- TEST 4: FIN ----------")
    # Perform additional interactions or assertions as needed

    driver.close()
      

