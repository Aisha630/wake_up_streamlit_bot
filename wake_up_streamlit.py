from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from streamlit_app import STREAMLIT_APPS
import datetime
import time

# Set up Selenium webdriver (assuming Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Initialize log file
log_file = open("wakeup_log.txt", "a")

# Log the current date and time
log_file.write("Execution started at: {}\n".format(datetime.datetime.now()))

# Iterate through each URL in the list
for url in STREAMLIT_APPS:
    try:
        # Navigate to the webpage
        driver.get(url)

        # Check if the wake up button is present
        try:
            wakeup_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/div/div/button"))
            )
            not_awake = True
        except TimeoutException:
            not_awake = False

        if not_awake:
            # Find the button element and click it
            wakeup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/div/div/button"))
            )
            wakeup_button.click()
            time.sleep(10) # this is to make sure the workflow stays long enough on the page to wake up the app. streamlit widdle slow

            # Log success
            log_file.write("Successfully woke up app at: {}\n".format(url))
        else:
            # Log app already awake
            log_file.write("App already awake at: {}\n".format(url))

    except NoSuchElementException as e:
        # Log button not found
        log_file.write("Button not found for app at: {}. Error: {}\n".format(url, str(e)))
    except Exception as e:
        # Log any other exceptions
        log_file.write("Error for app at {}: {}\n".format(url, str(e)))

# Close the browser
driver.quit()

# Close the log file
log_file.close()

