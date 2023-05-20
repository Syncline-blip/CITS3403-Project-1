from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import NoSuchElementException

def test_user_interaction():
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/login")

    # Login
    email = "testjohn@example.com"
    password = "testpassword"

    email_input = driver.find_element("id", "email")
    email_input.send_keys(email)

    password_input = driver.find_element("id", "password")
    password_input.send_keys(password)

    submit_button = driver.find_element("xpath", "//button[@type='submit']")
    submit_button.click()

    # Wait for the login process to complete
    driver.implicitly_wait(5)

    # Enter the global chat
    global_chat_button = driver.find_element("name", "globalChat")
    global_chat_button.click()

    try:
        chat_title = driver.find_element("class name", "chatTitle")
        if chat_title.text == "Global Chat":
            print("User successfully entered the Global Chat.")
        else:
            print("Failed to enter the Global Chat.")
    except Exception:
        print("Failed to find the Global Chat button.")
    # Wait for the global chat to load
    driver.implicitly_wait(5)

    # Perform additional interactions or assertions as needed

    driver.close()

test_user_interaction()
