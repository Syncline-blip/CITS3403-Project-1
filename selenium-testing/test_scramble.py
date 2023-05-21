# Test the scramble game
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_create_new_room():
    driver = webdriver.Chrome('path/to/chromedriver.exe')
    driver.maximize_window()

    # Navigate to the page where the button exists
    driver.get('http://example.com/your-page')

    # Find the "Create New Room" button and click it
    create_button = driver.find_element(By.ID, 'create-btn')
    create_button.click()

    # Wait for the new room creation process
    driver.implicitly_wait(5)

    # Fill in the required fields and submit the form to create a new room
    room_name_input = driver.find_element(By.ID, 'room-name')
    room_name_input.send_keys('New Room Name')

    description_input = driver.find_element(By.ID, 'room-description')
    description_input.send_keys('This is a new room description')

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Wait for the new room to be created and perform additional assertions or interactions as needed

    # Rest of your test code...

    driver.quit()

test_create_new_room()