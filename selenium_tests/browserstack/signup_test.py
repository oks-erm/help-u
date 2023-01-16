import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# sign in
driver = webdriver.Chrome('./chromedriver')
driver.get("https://helpukr.herokuapp.com/")
if "Help U" not in driver.title:
    raise Exception("Unable to load the page!")

try:
    try:
        menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#navbar > i"))
        )
        menu.click()
    except:
        pass
    register = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#navbar > ul > li:nth-child(5) > a"))
    )
    register.click()
except:
    print('something went wrong (register)')
else:
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_email"))
    )
    form_email.clear()
    form_email.send_keys(f"test{random.randint(1, 100000)}@test.com")
    form_email.send_keys(Keys.TAB)

    form_fname = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_first_name"))
    )
    form_fname.clear()
    form_fname.send_keys("Sele")
    form_fname.send_keys(Keys.TAB)

    form_lname = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_last_name"))
    )
    form_lname.clear()
    form_lname.send_keys("Nium")
    form_lname.send_keys(Keys.TAB)

    form_pass1 = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_password1"))
    )
    form_pass1.clear()
    form_pass1.send_keys("qazqaz123")
    form_pass1.send_keys(Keys.TAB)

    form_pass2 = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_password2"))
    )
    form_pass2.clear()
    form_pass2.send_keys("qazqaz123")

    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#signup_form > div.d-grid.gap-2 > button"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(1)
    button.click()
    time.sleep(5)

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".login-block > div.row > div > h1")))
    print(f"Success! {return_value.text}")

driver.close()
