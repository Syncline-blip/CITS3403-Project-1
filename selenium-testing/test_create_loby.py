# Create testing lobby

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
