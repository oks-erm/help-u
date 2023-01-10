import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# profile form 
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
        user_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#user-name > a"))
        )
        user_name.click()
    except:
        print('something went wrong (user_name)')
    else:
        time.sleep(5)
        try:
            edit = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    # (By.CSS_SELECTOR, "#profile > div > div > div.col-xl-8.col-lg-7 > h2 > a"))
                    (By.CLASS_NAME, "bx-pencil"))
            )
            edit.click()
        except:
            print('something went wrong (edit)')
        else:
            time.sleep(3)
            city = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.ID, "id_city"))
            )
            city.send_keys('+1')
            time.sleep(3)

            save_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "submit-id-save"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", save_button)
            time.sleep(1)
            save_button.click()
            time.sleep(5)

            return_value = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#profile > div > div > div.col-xl-8.col-lg-7 > p"))
            )

            print(f"Success! {return_value.text.split(',')[1]}")

driver.close()
