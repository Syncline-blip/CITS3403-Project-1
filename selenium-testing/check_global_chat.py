from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def test_user_interaction():
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/login")

    # Login
    email = "testjohn@example.com"
    password = "testpassword"

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
    try:
        global_chat_button = driver.find_element("css selector", ".chatLink[name='globalChat']")
        global_chat_button.click()
        print("Global Chat button clicked")
        
        # Wait for the global chat to load
        driver.implicitly_wait(5)

        chat_title = driver.find_element("class name", "chatTitle")
        if chat_title.text == "Global Chat":
            print("User successfully entered the Global Chat.")
        else:
            print("Failed to enter the Global Chat.")
    except NoSuchElementException:
        print("Failed to find the Global Chat button.")

    # Perform additional interactions or assertions as needed

    driver.close()

test_user_interaction()
