import time
import uuid
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


TEST_COMMENT = str(uuid.uuid4)


# comment
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

    try:
        post = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#listings > div > div > div:nth-child(1) > div > div > a > h4"))
        )
        post.click()
    except:
        print('something went wrong (post)')
    else:
        time.sleep(2)
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "btn-success"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)
        button.click()
        time.sleep(1)
        publish = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#comment > div > form > div.text-end > button"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", publish)

        try:
            text = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "body"))
            )
            text.send_keys(TEST_COMMENT)
            publish.click()
            time.sleep(2)

            return_value = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#comments-block > div.card.border-0.comment > div > div.col-9 > div > p.card-text.text-muted.mb-1"))
            )

            print(f"Success! {return_value.text}")
        except:
            print("something went wrong (text field)")

driver.close()
