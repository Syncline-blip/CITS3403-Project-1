'''
    Purpose: Testing Field for application
    Note   : Before Running, ensure database is fresh
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Test Score


'''
    1 Checks the page when first opened, simple test to see if all links
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
    2 Checks to see if the website will login a non-registered user, fail if it does
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

''' 
    3 Checks to see if register works properly
'''
def test_sign_up():
    score = 0
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/sign-up")

    email = "selenium@example.com"
    username = "seleniumautomation"
    password = "tgrpass1"

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

    print("---------- TEST 3: TEST REGISTER ----------")
    # Check if logout was successful
    try:
        login_link = driver.find_element("link text", "Login")
        print("Logout successful, therefore login is successful.")
    except Exception:
        print("Logout failed. may not have been logged on properly")
        return score
    driver.close()
    score +=1
    print("---------- TEST 3: FIN ----------\n")
    return score

''' 
    4: CHECK IF A PUBLIC CHAT CAN BE FOUND:
'''
def pub_chat_access():
    score = 0
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/login")

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
        return score
    print("---------- TEST 4: FIN ----------")
    # Perform additional interactions or assertions as needed
    score += 1
    driver.close()
    return score


''' 
    5: Check if the user can enter into a private DM with first occur
'''
def priv_chat_access():
    score = 0
    driver = webdriver.Chrome('C:/Users/John Lumagbas/Desktop/GITHUB-UWA/CITS3403-Project-1/selenium-testing/chromedriver.exe')
    driver.get("http://127.0.0.1:5000/login")

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
    print("---------- TEST 5: ENTER PRIVATE DM ----------")
    try:
        
        global_chat_button = driver.find_element("css selector", ".chatLink[name='globalChat']")
        global_chat_button.click()
        print("Global Chat button clicked")
        
        # Wait for the global chat to load
        driver.implicitly_wait(5)

        chat_title = driver.find_element("id", "title")
        if chat_title.text == "Chat Room: GLOB":
            print("User successfully entered Private Chat Chat.")
        else:
            print("Failed to enter the Global Chat.")
    except AssertionError:
        print("Failed to find the Global Chat button.")
        return score
    print("---------- TEST 5: FIN ----------")
    # Perform additional interactions or assertions as needed
    score += 1
    driver.close()
    return score



''' Launch All Required tests'''
def main():
    test_score = 0

    # test_score += check_page_on_land()
    # test_score += attempt_non_registered()
    test_score += test_sign_up()
    test_score += pub_chat_access()
    print(f"Test Score: {test_score}")

if __name__ == "__main__":
    main()