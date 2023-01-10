import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
    login = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#navbar > ul > li:nth-child(6) > a"))
    )
    login.click()
except:
    print('something went wrong (login)')
else:
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_login"))
    )
    form_email.clear()
    form_email.send_keys("test1@test.com")
    form_email.send_keys(Keys.TAB)
    form_pass = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_password"))
    )
    form_pass.clear()
    form_pass.send_keys("qazqaz123")

    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > form > div.d-grid.gap-2 > button"))
    )
    button.click()
    time.sleep(5)

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "search")))
    print(return_value is not None)

driver.close()
