import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

###########################################################################

# The tests are run on BrowserStack.
# To run the test use `browserstack-sdk python3 selenium/seleniumforms.py`

###########################################################################


# contact form
driver = webdriver.Chrome('./chromedriver')
driver.get("https://helpukr.herokuapp.com/")
if "Help U" not in driver.title:
    raise Exception("Unable to load the page!")

try:
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "contact-form"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", form)
except:
    print('something went wrong')
else:
    form_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    form_subject = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "subject"))
    )
    form_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "message"))
    )

    # Sending input
    form_name.clear()
    form_name.send_keys("Selenium Test Name")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_email.clear()
    form_email.send_keys("test@example.com")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_subject.clear()
    form_subject.send_keys("Selenium Test subject")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_message.clear()
    form_message.send_keys("Selenium Test message text")

    # Submitting the form
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#contact > div > div.container-fluid.col-lg-8.mt-5.mt-lg-0 > form > div.text-center > button')))

    submit_button.click()

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sent-message")))
    time.sleep(3)
    print(return_value.text)

driver.close()
