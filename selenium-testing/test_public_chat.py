from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service


''' 
    5 CHECK IF A PUBLIC CHAT CAN BE FOUND:
'''
def test_pub_chat_access():
     
    driver = webdriver.Chrome(service=Service('selenium-testing\chromedriver.exe'))
    driver.get("http://127.0.0.1:5000/sign-up")

    email = "selenium89@example.com"
    username = "smokeweed3w1"
    password = "tgrpass1!"

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


    driver.close()